import re
import requests
from requests import Session
from bs4 import BeautifulSoup
import json
import pandas as pd

# %% Initialize.
session = Session()
session.trust_env = False
with open("data/header_interest_co_nz_categories.json") as f:
    header_categories = json.load(f)
with open("data/header_interest_co_nz_csv.json") as f:
    header_csv = json.load(f)

# %% Get categories.
summary_url = "https://www.interest.co.nz/charts/interest-rates/fixed-mortgage-rates"
header_categories['Referer'] = summary_url
header_csv['Referer'] = summary_url
response = session.get(url=summary_url, headers=header_categories)
response_text = BeautifulSoup(response.text, features="html.parser")
series_names = response_text.find("select", {"class": "chart-selector"})
categories = [option.text for option in series_names.find_all("option")]

# %% Get index.
chart_block = response_text.find("div", {"class": "chart-block"})
node_id = re.findall(r"\d+", chart_block['id'])[0]
response = requests.post(
    url="https://www.interest.co.nz/chart-data/get-csv-data",
    headers=header_csv,
    data={"nids[]": node_id}
)
response_json = response.json()[node_id]['csv_data']

# %% Match index with city.
index_df = []
for category, index_per_cat in zip(categories, response_json):
    index_per_cat_df = pd.DataFrame(index_per_cat)
    index_per_cat_df = index_per_cat_df.iloc[:, :3]
    index_per_cat_df.columns = ['Timestamp', f"{category} fixed rate",
                             f"{category} floating rate"]
    index_per_cat_df['Timestamp'] = pd.to_datetime(index_per_cat_df['Timestamp'] * 1e6)
    index_per_cat_df['Timestamp'] = index_per_cat_df['Timestamp'].dt.date
    index_per_cat_df.set_index('Timestamp', inplace=True)
    index_df.append(index_per_cat_df)
index_df = pd.concat(index_df, axis=1)

# %% Fix cells that are at wrong position.
index_df.loc[pd.to_datetime('2010-02-25').date(), [
    '4 years % fixed rate', '4 years % floating rate']] = index_df.loc[
    pd.to_datetime('2010-02-24').date(), [
        '4 years % fixed rate', '4 years % floating rate']]
index_df.drop(labels=pd.to_datetime('2010-02-24').date(), axis=0, inplace=True)

# %% Export.
index_df.to_csv("results/nz_fixed_mortgage_rates.csv", index_label="date")
