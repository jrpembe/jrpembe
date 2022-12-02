# %% Import excel to dataframe
import pandas as pd

df = pd.read_excel("Online Retail.xlsx")

# %%  Show the first 10 rows
df.head(10)

# %% Generate descriptive statistics regardless the datatypes
df.describe(include="all")

# %% Remove all the rows with null value and generate stats again
df = df.dropna()
df.describe(include="all")

# %% Remove rows with invalid Quantity (Quantity being less than 0)
df = df[df["Quantity"] >= 0]

# %% Remove rows with invalid UnitPrice (UnitPrice being less than 0)

df = df[df["UnitPrice"] >= 0]

# %% Only Retain rows with 5-digit StockCode

is_number = df["StockCode"].astype(str).str.isdigit()

has_5_chars = df["StockCode"].astype(str).str.len() == 5

df = df[ is_number & has_5_chars ]
df

# %% strip all description

df["Description"] = df["Description"].str.strip()

# %% Generate stats again and check the number of rows

df.describe(include="all")

# %% Plot top 5 selling countries
import matplotlib.pyplot as plt
import seaborn as sns

top5_selling_countries = df["Country"].value_counts()[:5]
ax = sns.barplot(x=top5_selling_countries.index, y=top5_selling_countries.values)
plt.xlabel("Country")
plt.ylabel("Amount")
plt.title("Top 5 Selling Countries")

# %% Plot top 20 selling products, drawing the bars vertically to save room for product description
import seaborn as sns
import matplotlib.pyplot as plt

summary = (
    df.groupby("Description")
    .sum()
    .reset_index()
    .sort_values("Quantity",ascending=False)
    .head(20)
)

summary

ax = sns.barplot(
    data=summary,
    x="Quantity",
    y="Description",
    palette="flare"
)

plt.xlabel("Amount")
plt.ylabel("Products")
plt.title("Top 20 Selling Products")

# %% Focus on sales in UK

df_uk = df[df["Country"] == "United Kingdom"]

summary = (
    df_uk.groupby("Description")
    .sum()
    .reset_index()
    .sort_values("Quantity",ascending=False)
    .head(20)
)

summary

ax = sns.barplot(
    data=summary,
    x="Quantity",
    y="Description",
    palette="flare"
)

plt.xlabel("Amount")
plt.ylabel("Products")
plt.title("Top 20 Selling Products in the UK")

#%% Show gross revenue by year-month
from datetime import datetime

df["YearMonth"] = df["InvoiceDate"].apply(
    lambda dt: datetime(year=dt.year, month=dt.month, day=1)
)

df["GrossRevenue"] = df['Quantity']*df['UnitPrice']

ax = sns.lineplot(
    data=df.groupby("YearMonth").sum().reset_index(),
    x="YearMonth",
    y="GrossRevenue"
)

plt.title("Gross Revenue by Year-Month")
plt.show()

# %% save df in pickle format with name "UK.pkl" for next lab activity
# we are only interested in InvoiceNo, StockCode, Description columns
import pickle

df[["InvoiceNo", "StockCode", "Description"]].to_pickle("UK.pkl")