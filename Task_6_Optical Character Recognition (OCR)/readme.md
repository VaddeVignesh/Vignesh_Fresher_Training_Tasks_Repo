#  Task 6: Optical_Character_Recognition(OCR)_With_DocLayNet

This repository demonstrates a complete Optical Character Recognition (OCR) workflow — starting from traditional OCR models like **Pytesseract** and **EasyOCR**, extending to **Transformer-based TrOCR**, and finally incorporating **document layout detection** using **YOLOv10s** with **PaddleOCR** for end-to-end text extraction.

The Task integrates multiple techniques to extract both textual and tabular information from structured and unstructured documents.

---

##  Overview

The goal is to build a **multi-model OCR and layout analysis pipeline** that can:
- Detect document regions (text, tables, images) using **YOLOv10s**
- Extract and recognize text using **Pytesseract**, **EasyOCR**, **TrOCR**, and **PaddleOCR**
- Handle tabular data extraction via **Tabula**
- Evaluate model performance with metrics like **CER**, **WER**, and **Similarity**

---

##  Dataset Description

- **Source:** Custom document dataset (images and PDFs)
- **Contents:** Scanned documents, tables, and structured layouts
- **Format:** JPEG/PNG images and PDF files
- **Annotations:** JSON/YOLO format (bounding boxes for layout detection)

---

## ⚙️ 1. Data Loading & Setup

- Downloaded The Dataset from Hugging Face  
- Defined paths for images, annotations, and labels  
- Verified image–annotation consistency and counts  

---

##  2. Exploratory Data Analysis (EDA)

Explored dataset statistics such as:
- Number of images and annotations  
- Class/category distributions  
- Examples of bounding boxes and text regions  
- Visualized sample images with annotated text boxes to understand layout complexity  

---

## 3. Data Preprocessing

- Created helper functions to load image–annotation pairs into Pandas DataFrames  
- Parsed JSON annotation files to extract:
  - Text labels  
  - Bounding box coordinates  
  - Category names  
- Cleaned missing values and ensured correct image–label mapping  

---

##  OCR Models & Implementation

###  4. OCR Model 1 – Pytesseract
- Used **Tesseract OCR (Google’s engine)** for baseline text extraction  
- Applied OpenCV preprocessing (grayscale + thresholding)  
- Extracted text and compared outputs with ground truth  

###  5. OCR Model 2 – EasyOCR
- Loaded **EasyOCR** reader with multilingual support  
- Extracted text from the same document set  
- Compared with Pytesseract for speed and accuracy  
- Visualized detected text regions  

###  6. OCR Model 3 – TrOCR (Transformer-based)
- Implemented **Microsoft’s TrOCR** using **Hugging Face Transformers**  
- Utilized `TrOCRProcessor` and `VisionEncoderDecoderModel`  
- Achieved better performance on noisy and complex layouts  
- Compared with previous OCR models  

### 7. Table Extraction – Tabula
- Integrated **Tabula** for reading tables from PDFs  
- Converted extracted tables into **Pandas DataFrames**  
- Combined textual and tabular extractions for complete document understanding  

---

##  8. Layout Detection with YOLOv10s

- Trained **YOLOv10s** for detecting different layout elements such as:
  - Text regions  
  - Tables  
  - Images  
  - Headers/Footers  
- Annotated documents in YOLO format for supervised layout learning  
- Visualized detection results with bounding boxes and class labels  

**Steps:**
1. Loaded pretrained YOLOv10s model from Ultralytics  
2. Fine-tuned on document layout dataset  
3. Evaluated using precision, recall, and mAP metrics  
4. Saved layout-detected images for further OCR processing  

**Results:**
- YOLOv10s successfully separated text blocks and tables  
- Improved OCR accuracy by focusing recognition only on detected text regions  

---

##  9. OCR with PaddleOCR

- Integrated **PaddleOCR** for advanced multilingual text recognition  
- Used YOLOv10s detections as region proposals for focused text extraction  
- Supported multiple languages, text orientation, and curved text regions  
- Combined outputs into structured document text files  

**Advantages:**
- High accuracy on mixed-font and noisy text  
- Fast inference on GPU  
- Effective when combined with layout detection  

---

##  10. Model Evaluation

| Model | Average CER | Average WER | Average Similarity | Avg Time (s) |
|:------|:------------:|:------------:|:------------------:|:-------------:|
| Pytesseract | 0.1640 | 0.295 | 0.586 | 7.66 |
| EasyOCR | 0.1496 | 0.274 | 0.786 | 1.08 |
| TrOCR | **0.0905** | **0.1600** | **0.351** | - |
| PaddleOCR | **0.0782** | **0.1425** | **0.814** | **0.95** |

 **Observations**
- PaddleOCR outperformed all previous models in speed and accuracy  
- TrOCR performed well on complex document layouts  
- EasyOCR offered a strong balance between speed and performance  
- YOLOv10s + PaddleOCR pipeline gave the best structured text output overall  

---

##  Visualizations
- Layout detections with YOLOv10s bounding boxes  
- OCR overlays comparing predicted vs. ground truth text  
- Table extraction visual previews  
- Metric comparison plots for CER/WER across models  

---

##  Conclusion

This Task evolved from basic OCR exploration into a **complete document understanding system**:
- Early models (Pytesseract, EasyOCR, TrOCR) handled textual OCR  
- **YOLOv10s** added spatial understanding of document layouts  
- **PaddleOCR** refined text recognition on detected regions  
- **Tabula** extracted structured tables for combined insights  

The final pipeline can process complex PDFs and images efficiently, providing accurate text and layout extraction results.

---

## 🛠️ Installation

Clone the repository and install dependencies:
```bash
git clone https://github.com/<your-username>/OCR-Layout-Detection-Project.git
cd OCR-Layout-Detection-Project
pip install -r requirements.txt
