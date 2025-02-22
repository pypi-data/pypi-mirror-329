"""
Module: textstrata
Provides functions to convert DataFrame samples to formatted text strings.
"""

def generate_sample_strings(strata_dict, text_column, max_tokens=None):
    """
    Convert samples to concatenated text strings with '#' as a separator.
    
    Parameters:
        strata_dict (dict): Mapping {stratum_id: [sample_df, ...]}.
        text_column (str): Name of the column containing text.
        max_tokens (int, optional): Maximum number of words in the output.
    
    Returns:
        dict: Mapping from stratum_id to a list of formatted text samples.
    """
    text_strata = {}
    for stratum_id, samples in strata_dict.items():
        stratum_texts = []
        for i, sample_df in enumerate(samples):
            processed_rows = []
            for raw_text in sample_df[text_column].astype(str):
                cleaned_text = " ".join(raw_text.split())
                processed_rows.append(cleaned_text)
            sample_text = "#".join(processed_rows)
            if max_tokens is not None:
                words = sample_text.split()
                if len(words) > max_tokens:
                    sample_text = " ".join(words[:max_tokens])
            final_sample = f"{stratum_id}R{i+1}::{sample_text}"
            stratum_texts.append(final_sample)
        text_strata[stratum_id] = stratum_texts
    return text_strata
