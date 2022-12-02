# %% import dataframe from pickle file
import pandas as pd

df = pd.read_pickle("UK.pkl")

df.head()

# %% convert dataframe to invoice-based transactional format

dataset=[]
for key, subset in df.groupby("InvoiceNo"):
    dataset.append(subset["Description"].tolist())
dataset

# %% apply apriori algorithm to find frequent items and association rules

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

import seaborn as sns

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
table = pd.DataFrame(te_ary, columns=te.columns_)

sns.displot(table.sum()/table.shape[0])

frequent_itemsets = apriori(table, min_support=0.02, use_colnames=True)
rules = association_rules(frequent_itemsets, min_threshold=0.1)

# %% count of frequent itemsets that have more then 1/2/3 items,
# and the frequent itemsets that has the most items

length = frequent_itemsets["itemsets"].apply(len)
frequent_itemsets["length"] = length
frequent_itemsets

print((frequent_itemsets["length"]>1).sum())
print((frequent_itemsets["length"]>2).sum())
print((frequent_itemsets["length"]>3).sum())

max_length = frequent_itemsets["length"].max()
print(frequent_itemsets[frequent_itemsets["length"]==max_length])

# %% top 10 lift association rules

rules.sort_values("lift",ascending=False).head(10)

# %% scatterplot support vs confidence
import matplotlib.pyplot as plt

sns.scatterplot(x=rules["support"],y=rules["confidence"], alpha=0.5)

# plt.xlabel("Support")
# plt.ylabel("Confidence")
# plt.title("Support vs Confidence")

# %% scatterplot support vs lift

sns.scatterplot(x=rules["support"],y=rules["lift"], alpha=0.5)

# plt.xlabel("Support")
# plt.ylabel("Lift")
# plt.title("Support vs Lift")