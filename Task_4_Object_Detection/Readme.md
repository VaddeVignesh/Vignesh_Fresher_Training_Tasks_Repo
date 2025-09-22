#  Task_4_Object_Detection (Cows & Buffalos)

This repository contains the complete workflow for detecting **Cows and Bulls** using **YOLOv8**.  
The work spans from **dataset exploration (EDA)** to **data preprocessing, augmentation, model training, evaluation, and visualization of results**.  

---

## Overview
The goal of this project is to build a robust object detection pipeline to distinguish between cows and bulls (and their sub-classes).  
Key steps include:
- Dataset loading and inspection.
- Exploratory Data Analysis (EDA) of class distribution, bounding boxes, and co-occurrence.
- Dataset filtering, augmentation, and preparation.
- Training YOLOv8 for object detection.
- Evaluating the trained model using multiple metrics and visualizations.

---

##  Dataset Description
- **Source:** Custom dataset stored in Google Drive.  
- **Format:** YOLO annotation format (`.txt` files with class and normalized bounding box coordinates).  
- **Classes:** 12 numeric classes (mapped to Cow/Bull subcategories).  

---

##  Methodology

### 1. Data Loading & Setup
- Mounted Google Drive in Colab.  
- Defined paths for images and labels.  
- Validated counts to ensure all images had corresponding label files.  

### 2. Exploratory Data Analysis (EDA)
- **Class Distribution:** Visualized the number of samples for each class.  
- **Bounding Box Analysis:** Explored width, height, and aspect ratio distributions.  
- **Co-occurrence Matrix:** Checked which classes often appear together in the same image.  
- **Image Samples:** Visualized sample images with bounding boxes drawn.  
- **CNN Embeddings:** Used ResNet50 + UMAP to visualize feature embeddings of the dataset.

### 3. Data Preparation
- **Filtering:** Removed under-represented classes.  
- **Splitting:** Stratified split into train, validation, and test sets.  
- **Augmentation:** Applied transformations (flip, rotation, scaling, etc.) to handle class imbalance.  
- **Config Update:** Modified `data.yaml` for YOLOv8 training.  

---

##  Model Training & Evaluation

### YOLOv8 Training
- Framework: [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics).  
- Used **mosaic** and **mixup** augmentations.  
- Trained on filtered and balanced dataset.  
- Model checkpoints saved for best validation performance.  

### CNN Embeddings (Feature Exploration)
- Extracted embeddings with **ResNet50** (ImageNet pretrained).  
- Reduced dimensions with **UMAP** for clustering visualization.  

### Evaluation
- Metrics: **mAP (mean Average Precision), Precision, Recall, F1-score**.  
- Visualizations:  
- Class-wise AP  
- Confusion Matrix  
- Precision-Recall (PR) Curves  

---

##  Results

### Class Distribution
- Showed imbalance (e.g., class 0 had significantly more samples).  
- After augmentation, minority classes were balanced for training.  

### Visualizations
- Bounding box size histograms.  
- UMAP embedding plots showing clear separation between classes.  
- Co-occurrence heatmaps to highlight overlapping categories.  

#### YOLOv8 Variant Comparison
Below is the performance comparison across different YOLOv8 variants trained on the dataset:

| Model Variant | mAP@0.5 | mAP@0.5:0.95 |
|---------------|---------|--------------|
| YOLOv8n       | 0.006   | 0.003        |
| YOLOv8s       | 0.009   | 0.004        |
| YOLOv8m       | 0.008   | 0.003        |
| YOLOv8l       | 0.008   | 0.003        |

 **Observations:**
- YOLOv8s achieved the highest **mAP@0.5** (0.009), slightly outperforming other variants.  
- All models showed **very low mAP scores**, indicating dataset challenges (class imbalance, noise, or insufficient training epochs).  
- Larger models (m/l) did not yield significant improvements compared to smaller variants.  

#### Confusion Matrix
- Minor confusion observed between visually similar categories.  

#### Precision-Recall Curves
- Clear separation for dominant classes.
- Minority classes improved after augmentation.    

---
## Conclusion

In this project, I explored building a pipeline to detect cows and bulls using YOLOv8, starting from dataset exploration to training and evaluating the model. I faced challenges like class imbalance and limited data, but I learned a lot about **data preprocessing, augmentation, and preparing the dataset properly**.

The models didn’t get very high mAP scores, but looking at embeddings and visualizations helped me understand the dataset better. Next, I think adding more data, trying longer training, and experimenting with bigger YOLOv8 models could improve results.

Overall, this was a great learning experience in **object detection**, and it gave me a good foundation to build more robust models for real-world use.

##  Usage

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/cows-bulls-detection.git
cd cows-bulls-detection

