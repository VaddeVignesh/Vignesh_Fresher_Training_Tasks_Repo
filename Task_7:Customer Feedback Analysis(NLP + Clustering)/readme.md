# Task_7 : Customer Feedback Analysis using NLP and Unsupervised Clustering

## Task Overview

This Task performs an in-depth analysis of customer feedback data.  
The primary goal is to move beyond simple sentiment analysis and use **Natural Language Processing (NLP)** and **unsupervised machine learning** to discover *hidden topics* and *themes* within the feedback.

The workflow begins with raw text data, processes it through an NLP pipeline, and converts it into numerical features using **TF-IDF**.  
To overcome the "curse of dimensionality," these features are reduced to a 2D space using **UMAP**.

The core of the Task is a  comparing **nine different clustering algorithms** to find the optimal model for grouping the feedback.  
Finally, the best model is used for a deeper analysis connecting identified text-based topics to their underlying sentiments.

---

## Workflow & Methodology

This Task follows a structured, sequential data science pipeline.

### 1. Data Loading & Exploration
- Loaded the `ssentiiment_analysis.csv` file into a pandas DataFrame.  
- Conducted initial **Exploratory Data Analysis (EDA)** using `.info()`, `.head()`, and `.isnull().sum()` to understand the data and check for missing values.  
- Examined the distribution of the original `cluster` column, which serves as the sentiment/category label.

---

### 2. Text Preprocessing (NLP)
Defined a robust NLP preprocessing function to clean the raw **‘Answer’** text column.

The pipeline includes:
- Converting text to lowercase.  
- Removing all punctuation.  
- Removing standard English stopwords using `nltk`.  
- **Lemmatization** to reduce words to their root form (e.g., *running → run*).  

The cleaned text was stored in a new column named `lemmatized_answer`.

---

### 3. Feature Engineering (TF-IDF)
- Transformed the cleaned, lemmatized text into a high-dimensional numerical matrix using **TfidfVectorizer**.  
- This TF-IDF representation weighs words based on their importance in a document relative to the entire corpus, providing strong numerical features for clustering.

---

### 4. Dimensionality Reduction (UMAP)
- Applied **Uniform Manifold Approximation and Projection (UMAP)** to the sparse TF-IDF matrix.  
- Reduced the data from thousands of dimensions to a dense **2-dimensional space (`X_umap`)**.  

This step is crucial because:
1. It enables clear 2D visualization of inherent data structure.  
2. It boosts performance and accuracy for density-based clustering algorithms like **DBSCAN**.

---

### 5. Clustering Model Comparison
A comprehensive comparison ("bake-off") of **nine clustering algorithms** was conducted on the 2D UMAP data.

| Algorithm | Description |
|------------|--------------|
| **K-Means** | Tuned using the *Elbow Method* to find the optimal number of clusters (k). |
| **DBSCAN** | Tuned using a *K-Distance Plot* to find the optimal `eps = 0.6`, validated for high-quality clusters. |
| **HDBSCAN** | Hierarchical version of DBSCAN. |
| **Agglomerative Clustering (Hierarchical)** | Traditional linkage-based clustering. |
| **Gaussian Mixture Model (GMM)** | Probabilistic model assuming data is generated from multiple Gaussian distributions. |
| **Affinity Propagation** | Message-passing based clustering method. |
| **Mean Shift** | Density-based algorithm that doesn’t require predefined cluster numbers. |
| **Spectral Clustering** | Graph-based approach leveraging eigen decomposition. |
| **BIRCH** | Efficient hierarchical clustering for large datasets. |

---

### 6. Quantitative Model Evaluation
A final evaluation script collected performance metrics for all models into one table.

**Metrics Used:**
- **Silhouette Score** (Higher = Better)  
- **Calinski-Harabasz Score** (Higher = Better)  
- **Davies-Bouldin Score** (Lower = Better)  

Noise points (`-1` labels) from DBSCAN and HDBSCAN were properly handled, ensuring a fair comparison by scoring only on valid clusters.

---

### 7. In-Depth Cluster Analysis (Topic–Sentiment Modeling)
This final stage delivered the most insightful outcomes.

The **best-performing model (DBSCAN)** was used to connect text-based clusters with sentiment labels.

- **The "What":**  
  A crosstab and stacked bar chart showed the sentiment distribution (from the `cluster` column) across each of the **7 discovered clusters**.  

- **The "Why":**  
  Extracted the **top 10 TF-IDF keywords** for each cluster to uncover its dominant topic or theme — explaining *why* certain feedbacks were grouped together and *why* they shared specific sentiments.

---

## Key Tools & Libraries

- **Data Manipulation:** `pandas`, `numpy`  
- **NLP:** `nltk` (stopwords, lemmatization), `scikit-learn` (`TfidfVectorizer`)  
- **Machine Learning:** `scikit-learn`, `umap-learn`, `hdbscan`  
- **Visualization:** `matplotlib`, `seaborn`

---

## Key Findings & Conclusion

### Final Model Performance Metrics

The quantitative bake-off identified a clear winner: **Tuned DBSCAN**, manually optimized using the K-Distance plot.  
It outperformed all other algorithms, including auto-tuning models like **HDBSCAN**.

| Model | Silhouette Score | Calinski-Harabasz Score | Davies-Bouldin Score |
|--------|------------------|--------------------------|----------------------|
| **DBSCAN** | **0.879** | **5826.2** | **0.135** |
| Mean Shift  | 0.862 | 417.4 | 0.159 |
| Affinity Prop. | 0.809 | 1309.1 | 0.165 |
| HDBSCAN  | 0.793 | 545.6 | 0.306 |
| K-Means  | 0.752 | 548.7 | 0.388 |
| Agglomerative  | 0.752 | 548.7 | 0.388 |
| GMM  | 0.752 | 548.7 | 0.388 |
| Birch | 0.726 | 248.7 | 0.417 |
| Spectral | 0.172 | 26.5 | 4.748 |

*(Scores are rounded for clarity.)*

---

### Analysis of Findings

#### **Best Model: Tuned DBSCAN**
- The **DBSCAN** model with parameters `eps = 0.6` and `min_samples = 5` delivered the best overall clustering performance.  
- It outperformed all eight competing models across all evaluation metrics.

#### **High-Quality Clusters**
- Identified **7 distinct clusters** from **75 data points**, labeling only **4 points** as noise.  
- This shows excellent fit and structure for the UMAP-projected feature space.

#### **Actionable Insights (Topics + Sentiment = Insight)**
The final analysis bridged topics and sentiment, moving beyond binary sentiment labels to **explain the reason behind each sentiment**.  

- Clusters containing keywords like *“error, failed, broken”* aligned strongly with **negative feedback**.  
- Clusters with keywords like *“helpful, easy, recommend”* were strongly tied to **positive feedback**.  

This level of interpretability enables businesses to directly target root causes of satisfaction or dissatisfaction.


## How to Run

1.  Ensure you have Python 3 and Jupyter Notebook installed.
2.  Install the required libraries:
    ```bash
    pip install pandas numpy nltk scikit-learn umap-learn hdbscan matplotlib seaborn
    ```
3.  In your Python environment, download the NLTK components:
    ```python
    import nltk
    nltk.download('stopwords')
    nltk.download('wordnet')
    ```

4.  Run the `Task_7_Customer_Feedback_Analysis(NLP_+_Clustering).ipynb` notebook from the first cell to the last.
