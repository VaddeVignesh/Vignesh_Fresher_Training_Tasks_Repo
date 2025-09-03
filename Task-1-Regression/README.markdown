## Used Car Price Prediction

## TASK Objective

This task was assigned to me as a data science trainee to build a regression model that accurately predicts the selling price of used cars. The goal was to go through the complete machine learning lifecycle, from data cleaning and analysis to model building and evaluation.

## Methodology and Workflow

I followed a systematic approach to tackle this problem. Below are the steps I took to process the data and build the predictive models.

## 1. Data Cleaning and Preprocessing
My first priority was to understand and clean the raw Car.csv dataset.

**Initial Data Assessment** :  I began by examining the dataset's structure, data types (.info()), and missing values (.isna().sum()). This revealed that several columns containing numerical data (e.g., mileage, engine) were incorrectly typed as objects, and there were null values across multiple features.

**Data Type Correction:** To make the data usable for modeling, I performed the following conversions:

Removed units like "kmpl", "CC", and "bhp" from the mileage, engine, and max_power columns and converted them to numeric types.

For the torque column, which had inconsistent text formats, I used a regular expression to extract the primary numerical value and convert the column to a numeric type.

**Handling Missing Values:**

For mileage and engine, I filled the missing entries with the column's mean.

For max_power and seats, I opted to use the median. I chose the median because it is less sensitive to outliers, which seemed more appropriate for these features.

**2. Feature Engineering and Exploratory Data Analysis (EDA)**

After cleaning, I explored the data to find patterns and create more effective features.

**Feature Creation:** The name column contained the full model name. I extracted the car's brand (e.g., "Maruti", "Hyundai") into a new column, as the brand is a significant factor in pricing. The original name column was then dropped.

**Correlation Analysis**: I generated a correlation heatmap for the numerical features. This helped me visually confirm the relationships between features and the selling_price. As expected, max_power and engine showed a strong positive correlation with the price.

**Distribution Analysis:** I examined the distribution of the target variable, selling_price, and found it was highly right-skewed. Several other features also showed skewed distributions. This observation was critical for the next step.

**3. Data Transformation**
To address the skewed data distributions, which can negatively impact the performance of many regression models, I applied a logarithmic transformation (np.log1p) to the selling_price target variable and other skewed numerical features. This helps to normalize the distributions and generally leads to better model performance.

**4. Model Preparation**

Feature and Target Separation: I defined my feature set (X) and the log-transformed target (y).

**Categorical Encoding:** I used one-hot encoding (pd.get_dummies) to convert categorical features like fuel_type, seller_type, and transmission into a numerical format that the models can process.

**Data Scaling:** I scaled the feature set using StandardScaler. This standardizes the features to have a mean of 0 and a standard deviation of 1, which is important for distance-based models and those using regularization (like Ridge and Lasso).

**Train-Test Split:** I divided the processed data into training (80%) and testing (20%) sets.

**5. Modeling and Hyperparameter Tuning**

I experimented with several regression algorithms to find the best performer.

**Baseline Models:** I started with simpler models like Linear Regression, Ridge, and Lasso to establish a baseline performance.

**Advanced Models:** I then trained more complex ensemble models: Random Forest, Gradient Boosting, and LightGBM.

**Hyperparameter Tuning:** For the advanced models, I used RandomizedSearchCV to find the optimal combination of hyperparameters. This process helps in tuning the model to achieve better accuracy and avoid overfitting.

**6. Model Evaluation**

I evaluated the models based on their performance on the unseen test data. The log-transformed predictions were converted back to their original scale before calculating the error metrics.

**R-squared (R²)**: Measures the proportion of the variance in the selling price that is predictable from the features.

**Mean Absolute Error (MAE):** This was the primary metric, as it represents the average absolute difference between the predicted price and the actual price, measured in Rupees.

The tuned Random Forest and LightGBM models were the top performers, achieving an R² score of over 0.96 and an MAE of approximately ₹68,000 - ₹70,000.

**Key Learnings**

1.This project reinforced the principle that data cleaning and preprocessing are foundational to building a successful model.

2.Log transformation proved to be a very effective technique for handling skewed data and improving model accuracy.

3. Ensemble models like Random Forest and LightGBM significantly outperformed simpler linear models for this dataset.
  
4. Hyperparameter tuning is a crucial step to unlock the full potential of complex models.
