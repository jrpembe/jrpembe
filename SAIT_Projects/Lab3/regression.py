# %% read data
import pandas as pd

train = pd.read_csv(
    "house-prices-advanced-regression-techniques/train.csv"
)
test = pd.read_csv(
    "house-prices-advanced-regression-techniques/test.csv"
)

# %% checkout out first few rows
train.head()

# %% checkout out dataframe info
train.info()

# %% describe the dataframe
train.describe(include="all")

# %% SalePrice distribution
import seaborn as sns

sns.distplot(train["SalePrice"])

# %% SalePrice distribution w.r.t CentralAir / OverallQual / BldgType / etc
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

# SalePrice distribution w.r.t CentralAir
ax = sns.boxplot(
    data=train,
    x = "CentralAir",
    y = "SalePrice",
)

ax.set_xticklabels(ax.get_xticklabels(), fontsize=6, rotation=30)

# SalePrice distribution w.r.t OverallQual
ax = sns.boxplot(
    data=train,
    x = "OverallQual",
    y = "SalePrice",
)

ax.set_xticklabels(ax.get_xticklabels(), fontsize=6, rotation=30)

# SalePrice distribution w.r.t BldgType
ax = sns.boxplot(
    data=train,
    x = "BldgType",
    y = "SalePrice",
)

ax.set_xticklabels(ax.get_xticklabels(), fontsize=6, rotation=30)

# %% SalePrice distribution w.r.t YearBuilt / Neighborhood

# plt.figure(figsize=(12,6))

ax = sns.boxplot(
    data=train,
    x = "YearBuilt",
    y = "Neighborhood",
)

ax.set_xticklabels(ax.get_xticklabels(), rotation=30)

# %%
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_log_error
import numpy as np

def evaluate(reg, x, y):
    pred = reg.predict(x)
    result = np.sqrt(mean_squared_log_error(y, pred))
    return f"RMSLE score: {result:.3f}"

dummy_reg = DummyRegressor()

dummy_selected_columns = ["MSSubClass"]
dummy_train_x = train[dummy_selected_columns]
dummy_train_y = train["SalePrice"]

dummy_reg.fit(dummy_train_x, dummy_train_y)
print("Training Set Performance")
print(evaluate(dummy_reg, dummy_train_x, dummy_train_y))

truth = pd.read_csv("truth_house_prices.csv")
dummy_test_x = test[dummy_selected_columns]
dummy_test_y = truth["SalePrice"]

print("Test Set Performance")
print(evaluate(dummy_reg, dummy_test_x, dummy_test_y))

print("Can you do better than a dummy regressor?")

# %% your solution to the regression problem

from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

reg = LinearRegression()

cat_cols=["Neighborhood"]
num_cols=["YearBuilt", "1stFlrSF"]

ct = ColumnTransformer(
    [
        ("ohe", OneHotEncoder(), cat_cols),
        ("fillna", SimpleImputer(), num_cols),
    ],
    remainder="passthrough"
)

selected_columns = cat_cols + num_cols
train_x = train[selected_columns]
train_y = train["SalePrice"]

train_x = ct.fit_transform(train_x)

reg.fit(train_x, train_y)
print("Training Set Performance")
print(evaluate(reg, train_x, train_y))

truth = pd.read_csv("truth_house_prices.csv")
test_x = test[selected_columns]
test_y = truth["SalePrice"]

test_x = ct.transform(test_x)

# %%
