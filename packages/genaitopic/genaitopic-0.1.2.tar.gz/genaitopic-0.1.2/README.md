# genaitopic 

We introduce a novel approach to auto topic modeling that integrates stratified sampling, bootstrap aggregation, and generative artificial intelligence (GenAI) to produce robust, human‐interpretable topic themes. The resulting document serves as a knowledge base for a Retrieval-Augmented Generation (RAG) module to predict the topic of unseen texts, thereby marrying unsupervised discovery with supervised predictive capabilities. 

## Installation

Install the package using pip:

```bash
pip install genaitopic

---

## Usage

### Loading the Generative AI Model

```python
# Import necessary libraries
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os
import pandas as pd

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = "your_api_key"

# Initialize the Gemini LLM and embeddings
gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Test if the model is working
response = gemini_llm.invoke("Hi there!").content
print(response)
```

### Preparing Your Data

Ensure your dataset have at least two columns: `'text'` and `'demographics'`.

```python
# Set the path to your data file
data_path = "./datatest.csv"

# Load the data
data = pd.read_csv(data_path)
```

### Importing Required Modules

```python
# Import modules for sampling and theme generation
from genaitopic.sampling import stratoboost, stratobooststring
from genaitopic.listthemes import finalthemes, stratoboostthemes, stratoboostthemes_domain
```

### Stratified Sampling with Bootstraps

Create an ensemble sampling by setting `n` (number of strata) and `k` (number of bootstraps) as per your requirements.

```python
# Perform stratified sampling with bootstraps
stratas = stratoboost.stratified_sampling_with_bootstraps(
    data=data, 
    demographics_col='demographics',
    n=3, 
    k=1, 
    fraction=0.2, 
    replacement=True
)

# Convert the sampled data into strings for processing
text_string = stratobooststring.convert_stratas_to_strings(
    stratified_samples=stratas,
    text_column='text'
)
```

### Generating Initial Themes

Generate initial themes for each of the `n*k` samples using the LLM within the specified domain (e.g., "Travel and Tourism").

```python
# Generate initial themes with the LLM
initial_themes, initial_themes_df = stratoboostthemes_domain.generate_themes_with_llm_domain(
    strata_dict=text_string,
    llm=gemini_llm,
    n_themes=20,
    prompt_template=None,
    domain="Travel and Tourism"
)
```

### Combining Final Themes

Review and modify the theme names in the generated themes file if needed to have more control over the predictions.

```python
# Combine themes to get the final themes
final_themes = finalthemes.combine_themes(
    final_doc=initial_themes,
    llm=gemini_llm,
    prompt_template=None
)
```

Displaying Final Themes
You can display the first few themes using pandas:

```python
import pandas as pd

# Display the first few themes
pd.DataFrame(final_themes).head(3)
Output:

```python
[
 {'Theme': 'Hotel Room Quality',
  'Definition': 'Condition, cleanliness, comfort, size, and layout of hotel rooms, including bed comfort, bathroom amenities, and overall room maintenance.'},
 {'Theme': 'Hotel Amenities and Services',
  'Definition': "Features and services offered by hotels beyond rooms, such as pools, restaurants, bars, spas, kids' clubs, room service, breakfast, and other recreational facilities, including their quality and availability."},
 {'Theme': 'Hotel Staff Performance',
  'Definition': 'Friendliness, helpfulness, professionalism, and responsiveness of hotel staff (reception, concierge, housekeeping, restaurant staff), including handling of complaints and requests.'},
  ...
]



### Making Predictions

Use the `ChromaRagPredict` module to classify new texts based on the generated themes.

```python
# Import the prediction module
from genaitopic.predict import ChromaRagPredict

# Checking a few sample predictions 
df_sample = data.sample(5)

# Add predictions to the DataFrame
df_sample["predicted_theme"], df_sample["retrievals"] = ChromaRagPredict.rag_classifier(
    data=df_sample,
    text_column="text",
    theme_csv_path="stratoboostdf_final_themes_20250220_2227.csv",
    k=3,
    persist_path="./theme_db_gemini3",
    llm=gemini_llm,
    embedding_model=gemini_embeddings,
    include_retrievals=True
)

# Display predictions
```python
for index, row in df_sample.iterrows():
    print(f"""Theme: {row['predicted_theme']}
    
Text: {row['text']}\n""")
```

### Example Output (Data Source-  https://www.kaggle.com/datasets/andrewmvd/trip-advisor-hotel-reviews )

```plaintext

Theme: Travel Agent Issues, Safety and Security, Hotel Management & Problem Resolution

Text: Ocean Blue security issues with items stolen from room. Ocean Blue Gulf Beach Resort visited Thanksgiving week 2007 and stayed in the honeymoon suite. Property setting beautiful but trip seriously marred by items stolen from room and resort's handling of the theft. Checked in to find room safe not working; valuables like cell phone and cash disappeared. Reported theft to resort management and security. They were unable to determine who came into the room via keycard entry. Talked to maids and unauthorized telephone repairman who reported phone issue; all denied participation in theft. Security concluded no theft happened and treated us like we fabricated the issue. Met other couples in the lobby who had thefts that week. In one instance, a couple said their safe door was pried open. Security told these couples they were lying and that thefts were not problems at the resort. Lack of acknowledgment and treatment made a bad situation worse. Not offered complementary dinner or massage for our trouble. Asked for a letter to present to Verizon for unauthorized calls; they refused. In the end, they did provide a letter stating it could not be used for legal purposes. Note: Safe was not fixed when we checked out.
```
