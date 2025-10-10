**Stock Price Forecasting Project**

**Project Overview:**

This project uses two distinct forecasting models, Prophet and Long Short-Term Memory (LSTM), to predict future stock prices. The goal is to compare the performance of a traditional time-series model (Prophet) against a deep learning approach (LSTM) and provide a multi-stock forecasting tool. The analysis includes a comprehensive evaluation of model accuracy, a 30-day forecast, and a comparison of historical trends.

**Key Features:**

**Dual-Model Approach:** The project trains both Prophet (from Meta) and a custom-built LSTM neural network. This allows for a robust comparison of different forecasting methodologies.

**Automated Model Selection:** The code automatically selects the best-performing model for each stock based on a combined score of R², MAPE, and Directional Accuracy.

**Comprehensive Evaluation:** Models are evaluated using key metrics like Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), R² Score, Mean Absolute Percentage Error (MAPE), and Directional Accuracy, providing a complete picture of performance.

**Visualizations:** The project generates insightful plots to visualize historical trends, compare model performance, and display the future forecast against actual data.

**30-Day Forecast:** The best-performing model for each stock is used to generate a 30-day price forecast, including a summary of expected changes and trends.

**Methodology:**

**Data Loading & Preprocessing:** The script automatically loads stock data from a CSV file, handles missing values, and ensures the data is in the correct format for time-series analysis.

**Exploratory Analysis:** The script analyzes historical trends for each stock, including price changes, volatility, and overall trend (Bullish/Bearish/Neutral).

**Model Training:** Both Prophet and LSTM models are trained on the historical data. The LSTM model uses a MinMaxScaler and a sequential architecture with LSTM layers and Dropout to prevent overfitting.

**Performance Comparison:** The models' performance on the training data is evaluated and compared. The results are summarized in a table and visualized in comparison plots.

**Forecasting:** The selected best model for each stock is used to predict the next 30 days' prices.

**Results & Summary:** A summary of the 30-day forecast is printed, detailing the expected price changes and trends. Key results, including model metrics and forecasts, are saved to CSV files.

**Results:**

The analysis showed that Prophet consistently outperformed the LSTM model across all five stocks in terms of R² score and other key metrics.

**Top 3 Performers (by R² score):**

Stock_2: Prophet R² = 0.9912

Stock_1: Prophet R² = 0.9736

Stock_3: Prophet R² = 0.9715

The final output provides a clear, actionable 30-day forecast for each stock, identifying upward, downward, or stable trends based on the model's predictions.

