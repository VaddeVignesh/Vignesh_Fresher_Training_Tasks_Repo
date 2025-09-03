# Titanic Survival Prediction (Classification Task)

##  Objective
The goal of this project was to build a **classification model** that predicts whether a passenger on the RMS Titanic survived or not.  
This task covered the **complete machine learning workflow** — from data cleaning and exploratory analysis to feature engineering, model building, hyperparameter tuning, and evaluation.

---

##  Methodology and Workflow

### 1. Data Cleaning and Preprocessing
**Datasets:** `train.csv` and `test.csv`

- **Initial Assessment:**  
  Checked structure, data types (`.info()`), and missing values (`.isna().sum()`).
- **Handling Missing Values:**  
  - `Age`: Filled missing values with the mean.  
  - `Embarked`: Filled missing values with the mode.  
  - `Fare`: In the test set, a missing fare was filled with the median.  

---

### 2. Feature Engineering & EDA

**Feature Creation**
- Extracted **Title** (Mr, Mrs, Miss, etc.) from the `Name` column. Rare titles were grouped under `"Rare"`.  
- Created **FamilySize** = `SibSp + Parch + 1`  
- Derived **IsAlone** (1 if travelling alone, 0 otherwise).  

**Analysis**
- Generated a **correlation heatmap** to see feature-target relationships.  
- Plotted distributions: confirmed higher survival for **women** and **1st class passengers**.  

---

### 3. Model Preparation
- **Features (X)** and **Target (y = Survived)** separated.  
- **Categorical Encoding:** Applied `pd.get_dummies` for `Sex`, `Embarked`, and `Title`.  
- **Scaling:** Used `StandardScaler` on `Pclass`, `Age`, `Fare`, and `FamilySize`.  
- **Dropped unnecessary columns:** `Name`, `Ticket`, `Cabin`, `PassengerId`.  

---

### 4. Modeling and Hyperparameter Tuning

**Models Tested**
- Logistic Regression  
- K-Nearest Neighbors  
- Decision Tree  
- Random Forest  
- Support Vector Machine (SVC)  
- Gaussian Naive Bayes  
- Gradient Boosting  

**Tuning**
- Focused on **RandomForestClassifier** and **GradientBoostingClassifier**.  
- Applied `RandomizedSearchCV` and `GridSearchCV` for hyperparameter optimization.  
- Final model: **Gradient Boosting Classifier** (best accuracy and generalization).  

---

### 5. Model Evaluation
- **Accuracy Score:** Overall correctness of predictions  
- **Precision & Recall:** Balanced trade-off between survivors correctly identified and misclassifications  
- **F2-Score:** More weight on recall (important to minimize false negatives)  
- **Confusion Matrix:** Visualized TP, TN, FP, FN  

**Final Model:** Tuned **Gradient Boosting Classifier** was the top performer.  

---

##  Key Learnings
- **Feature Engineering** added strong predictive power (`Title`, `FamilySize`, `IsAlone`).  
- **EDA** helped confirm historical assumptions (gender and class had the biggest impact).  
- **Ensemble Models** (Gradient Boosting, Random Forest) outperformed simpler models.  
- **Hyperparameter Tuning** was crucial to improve performance beyond default settings.  

---

