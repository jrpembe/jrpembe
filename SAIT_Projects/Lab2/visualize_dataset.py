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
sns.barplot(x=top5_selling_countries.index, y=top5_selling_countries.values)
plt.xlabel("Country")
plt.ylabel("Amount")
plt.title("Top 5 Selling Countries")


# %% Plot top 20 selling products, drawing the bars vertically to save room for product description
import seaborn as sns
import matplotlib.pyplot as plt

top20_selling_Products = df["Description"].value_counts()[:20]

sns.barplot(x=top20_selling_Products.values, y=top20_selling_Products.index, )

plt.xlabel("Amount")

plt.ylabel("Products")

plt.title("Top 20 Selling Products")

# %% Focus on sales in UK

df_uk = df[df["Country"] == "United Kingdom"]
top20_selling_Products = df_uk["Description"].value_counts()[:20]

sns.barplot(x=top20_selling_Products.values, y=top20_selling_Products.index, )

plt.xlabel("Amount")

plt.ylabel("Products")

plt.title("Top 20 Selling Products in the UK")
#%% Show gross revenue by year-month
from datetime import datetime

df["GrossRevenue"] = df['Quantity']*df['UnitPrice']

df["YearMonth"] = df["InvoiceDate"].apply(
    lambda dt: datetime(year=dt.year, month=dt.month, day=1)
)

ax = sns.lineplot(x="YearMonth", y="GrossRevenue", data=df)

plt.title("Gross Revenue by Year-Month")
plt.show()


# %% save df in pickle format with name "UK.pkl" for next lab activity
# we are only interested in InvoiceNo, StockCode, Description columns
import pickle

df_out = df[["InvoiceNo", "StockCode", "Description"]]
df_out
# output = open('UK.pkl', 'wb')
# pickle.dump(df_out, output)
# output.close()
# %%
