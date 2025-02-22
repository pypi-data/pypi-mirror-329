import pandas as pd
import datetime

"""
Module: stratoboostthemes
Provides functions for generating initial themes using an LLM,
then saving them in a clean Pandas DataFrame.
"""

def generate_themes_with_llm(strata_dict, llm, prompt_template=None, n_themes=20):
    """
    Generate initial themes using the provided LLM, then save results to a clean Pandas DataFrame.

    Parameters:
        strata_dict (dict):
            A dictionary where each key is a stratum ID (e.g. "S1", "S2", etc.) 
            and the value is a list of strings, each string in the format:
                "S1R1::actual text goes here..."
            Example:
                {
                    "S1": [
                        "S1R1::just ok, place just ok arrived no problem desk ...",
                        "S1R2::some other text...",
                    ],
                    "S2": [
                        "S2R1::another text ...",
                        ...
                    ],
                    ...
                }

        llm:
            A LangChain LLM instance with an .invoke() method 
            that accepts a prompt and returns an LLM response.

        prompt_template (str, optional):
            A custom prompt template. If None, a default prompt is used.

        n_themes (int, optional):
            The number of most discussed important topics to extract. 
            Defaults to 20.

    Returns:
        tuple:
            (1) stratoboostresults: 
                A list of (sample_id, themes) where 'themes' is a dict {Theme: Definition}.
            (2) stratoboostdf: 
                A pandas DataFrame with columns ["Sample ID", "Theme", "Definition"].
                Also saved as "generated_themes.csv" in the current directory.
    """
    # 1) Provide a default prompt if none is given
    if prompt_template is None:
        default_prompt = f"""Act as topic modeler and Analyze the following text provided in triple backticks. Your task is to identify and extract the {n_themes} most significant and frequently discussed topics( if less found only retrun those to avoide redundancy), 
ensuring that any overlapping or duplicate subjects are consolidated under broader themes. 
For each theme, provide a concise definition that captures the core ideas expressed in the text. 
For example, rather than listing issues such as 'frequent app crashes,' 'laggy performance,' and 'slow response times' as separate topics, group them under a single theme like 'Application Performance,' defined as 'Concerns about the software's reliability and speed, including instances of crashes, delays, and sluggish responses.
'Additionally, do not reference or discuss specific entities mentioned in the text; focus solely on the overall text presented."


Format your response as: `Theme Name | Definition.`
Example:
    Location and Accessibility | hotel's proximity to attractions, public transportation, and other amenities.

```Text: {{text}}```"""
        prompt_template = default_prompt
        print(f"GenAI Prompt: {prompt_template}")
    # 2) Flatten strata_dict into a list of (sample_id, full_text) pairs
    #    e.g. [("S1R1", "S1R1::just ok..."), ("S1R2", "S1R2::some other text..."), ...]
    text_samples = []
    for stratum_id, sample_list in strata_dict.items():
        for sample_str in sample_list:
            parts = sample_str.split("::", 1)
            if len(parts) == 2:
                sample_id = parts[0]  # e.g. "S1R1"
                full_text = sample_str
            else:
                # Fallback if somehow "::" is missing
                sample_id = stratum_id + "_unknown"
                full_text = sample_str
            
            text_samples.append((sample_id, full_text))

    # 3) Now process each (sample_id, text) pair with the LLM
    stratoboostresults = []
    for sample_id, text in text_samples:
        print(f"Prossesing Sample ID :{sample_id}")
        # Remove sample identifier (everything before "::") to get the "clean" text
        # e.g. "S1R1::the actual text" -> "the actual text"
        _, clean_text = text.split("::", 1)

        # Send the clean text to the LLM with the given prompt
        response = llm.invoke(prompt_template.format(text=clean_text))
        response_text = response.content if hasattr(response, 'content') else response

        # Parse the LLM's response to extract themes
        themes = {}
        for line in response_text.split("\n"):
            if "|" in line:
                theme, definition = line.split("|", 1)
                themes[theme.strip()] = definition.strip()

        stratoboostresults.append((sample_id, themes))

    # 4) Convert the stratoboostresults into a clean Pandas DataFrame
    final_records = []
    for sample_id, theme_dict in stratoboostresults:
        for theme, definition in theme_dict.items():
            final_records.append({
                "Sample ID": sample_id,
                "Theme": theme,
                "Definition": definition
            })

    stratoboostdf = pd.DataFrame(final_records)

    # 5) Save the DataFrame to a versioned CSV file with the date/time
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M")  # e.g., 20250219_1532
    filename = f"stratoboostdf_intial_generated_themes_{timestamp_str}.csv"
    stratoboostdf.to_csv(filename, index=False)
    print(f'Saved "{filename}" with columns ["Sample ID", "Theme", "Definition"].')

    # 6) Also save to "generated_themes.csv" (unversioned)
    stratoboostdf.to_csv("generated_themes.csv", index=False)

    return stratoboostresults, stratoboostdf
