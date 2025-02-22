import datetime
import pandas as pd

"""
Module: finalthemes
Provides functions for combining and finalizing themes using an LLM,
then saving them as a 2-column CSV (Theme, Definition).
"""

def combine_themes(final_doc, llm, prompt_template=None):
    """
    Combine and refine themes using the provided LLM. Automatically saves
    the final 2-column CSV as 'stratoboostdf_final_themes_YYYYMMDD_HHMM.csv'.

    The CSV and the returned list will have exactly two columns/keys:
    "Theme" and "Definition".

    Parameters:
        final_doc:
            EITHER a list of (sample_id, {Theme: Definition, ...}) tuples
            OR a list of dicts, each with keys "Theme" and "Definition".
            Example 1 (tuples):
                [
                    ("S1R1", {
                        "Location": "Hotel's proximity...",
                        "Room Quality": "Comfort and cleanliness...",
                        ...
                    }),
                    ("S2R1", {
                        "Staff Attitude": "Friendliness of staff...",
                        ...
                    })
                ]
            Example 2 (flattened):
                [
                    {"Theme": "Location", "Definition": "Hotel's proximity..."},
                    {"Theme": "Room Quality", "Definition": "Comfort and cleanliness..."},
                    ...
                ]

        llm:
            A LangChain LLM instance with an .invoke() method.

        prompt_template (str, optional):
            Custom prompt. If None, a default prompt is used that requests
            lines in the exact format:
                Theme: <some theme>
                Definition: <some definition>

    Returns:
        list of dict:
            Final list of distinct themes with their definitions, e.g.:
            [
                {"Theme": "Location", "Definition": "Hotel's proximity..."},
                {"Theme": "Room Quality", "Definition": "Comfort and cleanliness..."},
                ...
            ]
    """

    # 1) Flatten final_doc into a list of dicts with "Theme" and "Definition".
    flattened_doc = []
    for item in final_doc:
        # Case A: item is a tuple like ("S1R1", {"Theme1": "Def1", ...})
        if (
            isinstance(item, tuple)
            and len(item) == 2
            and isinstance(item[1], dict)
        ):
            sample_id, theme_dict = item
            for theme, definition in theme_dict.items():
                flattened_doc.append({
                    "Theme": theme,
                    "Definition": definition
                })

        # Case B: item is already a dict with "Theme" and "Definition"
        elif (
            isinstance(item, dict)
            and "Theme" in item
            and "Definition" in item
        ):
            flattened_doc.append(item)

        else:
            print(f"Skipping unrecognized item format: {item}")

    # 2) Build the combined text for the LLM, 
    #    requesting a 2-line pattern per theme (Theme:, Definition:).
    combined_text = ""
    for doc in flattened_doc:
        combined_text += f"Theme: {doc['Theme']}\nDefinition: {doc['Definition']}\n"

    # 3) Default prompt ensures lines are strictly "Theme:" and "Definition:" 
    #    so we can parse them into a 2-column format.
    default_prompt = (
        """You are provided with a list of themes and their definitions enclosed in triple backticks below. Some themes may be exact duplicates (identical in both name and definition) or overlapping (conveying the same or very similar concepts despite different wording). Your task is to:

1) Identify and merge overlapping themes into single entries, combining their definitions to include the key points of each original definition.
2) For exact duplicates, include only one instance to avoid redundancy.
3) Ensure the final theme names are distinct and clear, Do not return unclear names, rename if required based on defination.
4) Ensure the definitions are clear, concise, and non-overlapping in meaning.Strictly Do not mention about specific entity in theme name and defination insted focus on overall topic.

example:
if given
Theme: Telemedicine
Definition: Providing healthcare services remotely using technology.
Theme: Remote Healthcare
Definition: Delivering medical care from a distance via digital platforms.
Output final theme based on above 2 themes and definition
Theme: Telemedicine
Definition: Providing healthcare services remotely using technology, including telecommunication for clinical services.

Return the resulting themes and definitions strictly as pairs of lines in this exact format:
Theme: <theme text>
Definition: <definition text>

Do not include bullet points, numbering, or any additional text beyond the specified format.


```List:
{combined_text}
```"""
    )
    prompt_template = prompt_template or default_prompt
    print(f"GenAI Prompt: {prompt_template}")
    # 4) Invoke the LLM
    response = llm.invoke(prompt_template.format(combined_text=combined_text))
    response_text = response.content if hasattr(response, 'content') else response

    # 5) Parse the LLM response
    lines = [line.strip() for line in response_text.split("\n") if line.strip()]
    final_themes = []
    current_theme = None

    for line in lines:
        # If line starts with "Theme:", parse out the theme
        if line.lower().startswith("theme:"):
            current_theme = line.split(":", 1)[1].strip()
        # If line starts with "Definition:", parse out definition and create a row
        elif line.lower().startswith("definition:") and current_theme:
            definition = line.split(":", 1)[1].strip()
            final_themes.append({
                "Theme": current_theme,
                "Definition": definition
            })
            current_theme = None  # reset

    # 6) Save to CSV with date/time versioning
    now = datetime.datetime.now()
    version_str = now.strftime("%Y%m%d_%H%M")
    filename = f"stratoboostdf_final_themes_{version_str}.csv"

    df = pd.DataFrame(final_themes, columns=["Theme", "Definition"])
    df.to_csv(filename, index=False)
    print(f'Saved final combined themes to "{filename}" with {len(final_themes)} rows.')

    # Return the list of dicts
    return final_themes
