import pandas as pd
import datetime
from langchain.prompts import PromptTemplate

def generate_themes_with_llm_domain(strata_dict, llm, prompt_template=None, n_themes=20, domain=None):
    """
    Generate initial themes using an LLM and save the results in a clean Pandas DataFrame.

    This function takes a dictionary of text samples, processes each sample through a provided
    language model (LLM) using a prompt template, and extracts the most discussed topics along with
    their definitions. The output is returned both as a list of results and as a CSV file saved locally.

    Parameters:
        strata_dict (dict):
            A dictionary where each key is a stratum ID (e.g., "S1", "S2", etc.) and each value
            is a list of strings. Each string should be in the format:
                "S1R1::actual text goes here..."
        llm:
            A LangChain LLM instance with an .invoke() method that accepts a prompt string.
        prompt_template (str or PromptTemplate, optional):
            A custom prompt template (either as a string or a LangChain PromptTemplate). If not provided,
            a default template is used.
        n_themes (int, optional):
            The number of topics to extract from each text sample. Defaults to 20.
        domain (str, optional):
            Domain-specific context (e.g., "hospitality and tourism domain") to tailor the theme extraction.
            If not provided, a general template is used.

    Returns:
        tuple: A tuple containing:
            - stratoboostresults (list): A list of tuples in the format (sample_id, themes_dict),
              where themes_dict maps theme names to their definitions.
            - stratoboostdf (pd.DataFrame): A DataFrame with columns ["Sample ID", "Theme", "Definition"],
              containing the extracted themes.
    """
    # If no prompt_template is provided, build a default one using LangChain's PromptTemplate.
    if prompt_template is None:
        base_template = (
            "Analyze the text provided in triple backticks and identify the {n_themes} most discussed important topics on overall text. "
            "Ensure the topics are distinct, avoiding overlap or duplication. Group related subtopics under broader themes"
            "and provide concise definitions for each. Do not retunrn topic name specific to any entity, focus on overall most discussed topics\n\n"
            "e.g If the text mentions 'long wait times,' 'shortage of specialists,' and 'delayed test results,' group them under a theme like 'Healthcare System Efficiency' defined as 'Issues related to prolonged wait times for appointments, limited availability of medical specialists, and delays in receiving diagnostic test results.'\n\n"
            "If the text is short or lacks explicit subtopics, reduce the number of themes to avoid redundancy. Keep positive/Negative/Neutral aspects for same topic under same topic name and defination"
            "{domain_specific_guidance}\n\n"
            "Format your response as (strictly return only ouput and in same format as): Theme Name | Definition"
            "Example:\n"
            "Healthcare System Efficiency | Issues related to prolonged wait times for appointments, limited availability "
            "of medical specialists, and delays in receiving diagnostic test results.\n\n"
            "Text: ```{text}```" 
        )

        if domain:
            domain_specific_guidance = (
                f"The text belongs to the {domain} domain, so focus on themes relevant to {domain}. Ensure themes are grouped based on domain-specific context. "
            )
        else:
            domain_specific_guidance = ""

        # Create the PromptTemplate without prematurely formatting the {text} placeholder.
        prompt_template = PromptTemplate(
            input_variables=["text"],
            template=base_template,
            partial_variables={
                "n_themes": str(n_themes),
                "domain_specific_guidance": domain_specific_guidance,
            }
        )

    print(f"GenAI Prompt: {prompt_template}")

    # Flatten strata_dict into a list of text samples (sample_id, text).
    text_samples = []
    for stratum_id, sample_list in strata_dict.items():
        for sample_str in sample_list:
            parts = sample_str.split("::", 1)
            sample_id = parts[0] if len(parts) == 2 else f"{stratum_id}_unknown"
            text_samples.append((sample_id, sample_str))

    # Process each sample with the LLM.
    stratoboostresults = []
    for sample_id, text in text_samples:
        print(f"Processing Sample ID: {sample_id}")
        # Extract the clean text after the delimiter.
        if "::" in text:
            _, clean_text = text.split("::", 1)
        else:
            clean_text = text

        # Format the prompt using the provided prompt_template.
        if isinstance(prompt_template, PromptTemplate):
            formatted_prompt = prompt_template.format(text=clean_text)
        else:
            formatted_prompt = prompt_template.format(text=clean_text)

        # Invoke the LLM with the formatted prompt.
        response = llm.invoke(formatted_prompt)
        response_text = response.content if hasattr(response, 'content') else response

        # Parse the response to extract themes and definitions.
        themes = {}
        for line in response_text.split("\n"):
            if "|" in line:
                theme, definition = map(str.strip, line.split("|", 1))
                themes[theme] = definition

        stratoboostresults.append((sample_id, themes))

    # Convert the results to a Pandas DataFrame.
    stratoboostdf = pd.DataFrame(
        [
            {"Sample ID": sid, "Theme": theme, "Definition": definition}
            for sid, theme_dict in stratoboostresults
            for theme, definition in theme_dict.items()
        ]
    )

    # Save the DataFrame to CSV files with a timestamp.
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"stratoboostdf_initial_themes_{timestamp}.csv"
    stratoboostdf.to_csv(filename, index=False)
    stratoboostdf.to_csv("generated_themes.csv", index=False)
    print(f'Saved "{filename}" with {len(stratoboostdf)} entries')

    return stratoboostresults, stratoboostdf
