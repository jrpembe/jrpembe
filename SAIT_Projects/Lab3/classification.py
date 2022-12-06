# Visualizing Titanic Dataset

# %% read data
import pandas as pd

train = pd.read_csv("titanic/train.csv")
test = pd.read_csv("titanic/test.csv")

# %% checkout out first few rows
train.head()

# %% checkout out dataframe info
train.info()

# %% describe the dataframe
train.describe(include="all")

# %% visualize the dataset, starting with the Survied distribution
import seaborn as sns

sns.countplot(x="Survived", data=train)
sns.countplot(x="Sex", data=train)
sns.countplot(x="Pclass", data=train)
sns.countplot(x="Embarked", data=train)

# %% Survived w.r.t Pclass / Sex / Embarked ?

sns.countplot(x="Survived", hue="Sex", data=train)

# %% Age distribution ?

sns.displot(data=train,x="Age").set(title="Age Distribution")

# %% Survived w.r.t Age distribution ?
sns.displot(data=train,x="Age", hue="Survived").set(title="Survival by Age")

# %% SibSp / Parch distribution ?

# %% Survived w.r.t SibSp / Parch  ?

# %% Dummy Classifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import f1_score

def evaluate(clf, x, y):
    pred = clf.predict(x)
    result = f1_score(y, pred)
    return f"F1 score: {result:.3f}"

dummy_clf = DummyClassifier(
    random_state=2020,
    strategy="uniform"
    )

dummy_selected_columns = ["Pclass"]
dummy_train_x = train[dummy_selected_columns]
dummy_train_y = train["Survived"]

dummy_clf.fit(dummy_train_x, dummy_train_y)
print("Training Set Performance")
print(evaluate(dummy_clf, dummy_train_x, dummy_train_y))

truth = pd.read_csv("truth_titanic.csv")
dummy_test_x = test[dummy_selected_columns]
dummy_test_y = truth["Survived"]

print("Test Set Performance")
print(evaluate(dummy_clf, dummy_test_x, dummy_test_y))

print("Can you do better than a dummy classifier?")


# %% Your solution to this classification problem
from sklearn.neighbors import KNeighborsClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

clf = KNeighborsClassifier()
ct = ColumnTransformer(
    [
        ("ohe", OneHotEncoder(), ["Sex"]),
        ("fillna", SimpleImputer(), ["Age"]),     
    ],
    remainder="passthrough"
)

selected_columns = ["Age", "Sex"]
train_x = train[selected_columns]
train_y = train["Survived"]

train_x = ct.fit_transform(train_x)

clf.fit(train_x, train_y)
print("Training Set Performance")
print(evaluate(clf, train_x, train_y))

truth = pd.read_csv("truth_titanic.csv")
test_x = test[selected_columns]
test_y = truth["Survived"]

test_x = ct.transform(test_x)

print("Test Set Performance")
print(evaluate(clf, test_x, test_y))
# %%
