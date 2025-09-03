README – Used Cars Price Prediction (Regression Task)
Task Overview

This Task is about predicting the selling price of used cars using regression models.
The dataset I worked with had details like mileage, engine capacity, max power, and more.
The main goal was to clean the data properly, explore important features, and then train different regression models to see which one works best.

I tried to keep my steps clear and logical, starting from data understanding, cleaning, and then moving to model building and evaluation.

Steps I Followed
1. Importing Libraries

I started by importing common libraries like pandas, numpy, matplotlib, seaborn for data handling and visualization, and scikit-learn/lightGBM for machine learning.

2. Loading the Dataset

I used the dataset Car.csv.
At first, I just looked at the top rows (head()), checked the column types (info()), and counted missing values.

3. Data Cleaning

Some columns had values stored as text instead of numbers. For example:

Mileage had values like "18.5 kmpl", so I removed the text part and converted it to numeric.

Engine had values like "1197 CC", so I extracted the number.

Max Power had values like "74 bhp", so again I cleaned it into numbers.

Torque was a bit tricky because it had text. I extracted just the numeric values.

After cleaning, I also checked again for null values and handled them with simple imputation where needed.

4. Exploring the Data

I created a correlation heatmap to see which features are strongly related to the target column (selling_price).
This helped me understand which features might matter more when predicting prices.

5. Splitting the Data

I separated the dataset into:

Features (X): things like mileage, engine, max power, etc.

Target (y): the selling price.

Then I split into training and testing sets.

6. Building Models

I tried different regression models to compare results:

Linear Regression

ElasticNet

Random Forest Regressor

Gradient Boosting Regressor

LightGBM Regressor

For some models, I also used cross-validation to make sure the performance was consistent.

7. Model Evaluation

I checked each model using:

R² score (how well the model explains variance in prices)

Mean Absolute Error (MAE) (average difference between predicted and actual)

Root Mean Squared Error (RMSE) (penalizes larger errors more)

This gave me a clear idea of which model performed best overall.

Learnings

Cleaning the data properly was the most important step.

Some features like mileage and max power had a strong influence on the selling price.

Ensemble models (Random Forest, Gradient Boosting, LightGBM) gave better accuracy compared to simple Linear Regression.

Evaluation metrics helped me understand not just how accurate the model was, but also how big the errors were.


Conclusion

This task helped me understand the complete flow of a regression problem:

Start with raw data, clean and prepare it,

Explore patterns,

Train different models,

Compare their performance.

As a fresher, this was a good hands-on learning experience in handling real-world data and applying regression techniques.
