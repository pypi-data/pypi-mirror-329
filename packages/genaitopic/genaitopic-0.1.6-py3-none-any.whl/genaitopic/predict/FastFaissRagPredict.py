import pandas as pd
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from typing import List, Optional, Union, Tuple, Dict
import os

def fast_faiss_rag_classifier(
    data: pd.DataFrame,
    text_column: str,
    theme_csv_path: str,
    k: int = 3,
    prompt: Optional[str] = None,
    persist_path: str = "./faiss_db",
    llm: Optional[any] = None,
    embedding_model: Optional[any] = None,
    include_retrievals: bool = False,
    persist: bool = False,
) -> Union[List[str], Tuple[List[str], List[List[Dict[str, str]]]]]:
    """
    Perform retrieval-augmented classification (RAG) of text data into predefined themes using FAISS.
    This function loads (or creates) a FAISS vector database from a CSV file containing theme definitions,
    then uses a language model (LLM) to classify each text sample in the provided DataFrame into the most appropriate theme.
    Optionally, it can also return the top-k retrieved definitions for transparency.
    
    Args:
        data (pd.DataFrame): A pandas DataFrame containing the text samples to classify.
        text_column (str): The name of the column in `data` that holds the text to be classified.
        theme_csv_path (str): File path to the CSV containing theme definitions. Must include columns "Theme" and "Definition".
        k (int, optional): Number of top matching definitions to retrieve from the vectorstore. Default is 3.
        prompt (str, optional): A custom classification prompt for the LLM. If None, a default prompt is used.
        persist_path (str, optional): Directory path for persisting/loading the FAISS database. Default is "./faiss_db".
        llm (any, optional): A language model instance compatible with LangChain (e.g., OpenAI, HuggingFace).
        embedding_model (any, optional): An embedding model instance (e.g., OpenAIEmbeddings). Required to build or query the vectorstore.
        include_retrievals (bool, optional): If True, returns both the predicted themes and the top-k retrieved definitions for each sample.
        If False, returns only the predicted themes.
        persist (bool, optional): If True, persists the FAISS database to disk. Default is False.

    Returns:
        Union[List[str], Tuple[List[str], List[List[Dict[str, str]]]]]: 
        - If `include_retrievals` is False: A list of predicted theme names for each row in the DataFrame.
        - If `include_retrievals` is True: A tuple of:
            1) A list of predicted theme names.
            2) A list (one per row) of the top-k retrieved theme definitions, each represented as a list of dicts with keys "theme_name" and "definition".
    
    Raises:
        ValueError: If `llm` or `embedding_model` is not provided.
    """
    # Validate required components
    if not llm or not embedding_model:
        raise ValueError("Both llm and embedding_model must be provided")

    # Create or load FAISS DB
    index_path = os.path.join(persist_path, "index.faiss")
    if os.path.exists(index_path):
        faiss_db = FAISS.load_local(persist_path, embedding_model,allow_dangerous_deserialization=True)
    else:
        theme_df = pd.read_csv(theme_csv_path)
        # Use itertuples for faster document creation
        docs = [
            Document(
                page_content=row.Definition,
                metadata={"theme_name": row.Theme}
            )
            for row in theme_df.itertuples()
        ]
        faiss_db = FAISS.from_documents(docs, embedding_model)
        if persist:
            os.makedirs(persist_path, exist_ok=True)
            faiss_db.save_local(persist_path)

    # Configure retriever and common components
    retriever = faiss_db.as_retriever(search_kwargs={"k": k})
    texts = data[text_column].tolist()

    # Default prompt template
    default_prompt = (
        "Act as a topic modeling expert to assign one or more relevant topics to the text enclosed in "
        "triple backticks. Use the provided 'context and topic definitions' to guide your decision. "
        "Carefully analyze both the content of the text and the context to ensure accurate topic assignment.\n\n"
        "Rules:\n\n"
        "1) Assign only topics explicitly and repeatedly mentioned in the text.\n"
        "2) Exclude themes that require assumptions, indirect links, or external knowledge.\n"
        "3) Rank themes from most to least discussed based on text frequency and detail.\n"
        '4) Never infer unstated connections (e.g., "travel agent issues" if no agent is mentioned).\n\n'
        "Context:{context}\n\n"
        "Criteria for Inclusion:\n"
        "1) Topic is directly named, described, or exemplified with specific incidents.\n"
        "2) Topic has multiple mentions or detailed discussions in the text.\n\n"
        "Output Format (ONLY themes meeting criteria) (Only return output):\n\n"
        "Theme_name1, Theme_name2, ...\n\n"
        "```Text: {query}```"
    )
    classification_prompt = ChatPromptTemplate.from_template(prompt or default_prompt)

    # Formatting function remains the same
    format_docs = lambda docs: "\n\n".join(
        f"Theme: {doc.metadata['theme_name']}\nDefinition: {doc.page_content}"
        for doc in docs
    )

    # Batch processing implementation
    if include_retrievals:
        # Chain that returns both response and retrieved documents
        retrieval_chain = (
            RunnableParallel(
                context=retriever | format_docs,
                retrieved_docs=retriever,
                query=RunnablePassthrough()
            )
            | RunnablePassthrough.assign(
                response=classification_prompt | llm | StrOutputParser()
            )
        )
        # Process all texts in single batch
        results = retrieval_chain.batch(texts)

        # Extract components from batch results
        predictions = [res['response'].strip() for res in results]
        retrievals = [
            [
                {"theme_name": doc.metadata["theme_name"], "definition": doc.page_content}
                for doc in res['retrieved_docs']
            ]
            for res in results
        ]
        return (predictions, retrievals)
    else:
        # Optimized batch processing for base case
        base_chain = (
            {"context": retriever | format_docs, "query": RunnablePassthrough()}
            | classification_prompt
            | llm
            | StrOutputParser()
        )
        predictions = [res.strip() for res in base_chain.batch(texts)]
        return predictions
