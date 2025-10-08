#  Task_6_OCR_With_(Pytesseract_EasyOCR_TrOCR_Tabula)

This repository contains the complete workflow for **Optical Character Recognition (OCR)** using multiple models — **Pytesseract**, **EasyOCR**, **TrOCR**, and **Tabula**.  
The work spans from dataset preparation and preprocessing to running multiple OCR models, evaluating their outputs, and visualizing the results.

---

##  Overview

The goal of this project is to extract and analyze text from complex document layouts using both **traditional** and **deep learning–based OCR models**.  
The task compares the performance of different OCR tools on the **DocLayNet dataset**, which contains diverse document structures such as invoices, reports, and tables.

### Key Steps Include:
- Dataset loading and inspection  
- Preprocessing and JSON annotation parsing  
- OCR with **Pytesseract**, **EasyOCR**, and **TrOCR**  
- **Table extraction** using Tabula  
- Model evaluation and visualization of results  

---

##  Dataset Description

**Source:** [DocLayNet Dataset](https://huggingface.co/datasets/doccano/DocLayNet)  
**Format:** Image files (.jpg/.png) with JSON annotations  
**Content:** Structured document pages (e.g., invoices, forms, reports)  
**Annotations Include:**  
- Bounding boxes  
- Text categories  
- Ground-truth text  

---
##  2. Exploratory Data Analysis (EDA)

Explored dataset statistics such as:

- Number of images and annotations  
- Class/category distributions  
- Examples of bounding boxes and text regions  
- Visualized sample images with annotated text boxes to understand layout complexity  

---

##  3. Data Preprocessing

- Defined helper functions to load image–annotation pairs into Pandas DataFrames.  
- Parsed JSON files to extract:  
  - Text labels  
  - Bounding box coordinates  
  - Category names  
- Handled missing data and ensured correct image–label mapping.  

---

##  OCR Models & Implementation

###  4. OCR Model 1 – Pytesseract

- Used **Tesseract OCR** (Google’s open-source engine) as the baseline text extraction model.  
- Preprocessed images using **OpenCV** (grayscale conversion + thresholding).  
- Extracted text and compared results with ground truth data.  
- Stored outputs for evaluation and visualization.  

---

###  5. OCR Model 2 – EasyOCR

- Loaded the **EasyOCR** reader with multilingual support.  
- Extracted text from the same document set for consistency.  
- Compared results to **Pytesseract** in terms of clarity, speed, and accuracy.  
- Visualized sample outputs with bounding boxes on extracted regions.  

---

###  6. OCR Model 3 – TrOCR (Transformer-based)

- Implemented **Microsoft’s TrOCR** using the **Hugging Face Transformers** library.  
- Utilized the `TrOCRProcessor` and `VisionEncoderDecoderModel` for text recognition.  
- Ran inference on document images to extract structured text.  
- Compared performance against Pytesseract and EasyOCR.  
- TrOCR demonstrated **superior performance** on **noisy and complex layouts**.  

---

###  7. Table Extraction with Tabula

- Integrated **Tabula** for extracting tabular data from PDF files.  
- Converted detected tables into **Pandas DataFrames** for structured analysis.  
- Combined **textual** and **tabular extraction** for full document understanding.  

##  Model Performance Comparison

Below is a summary comparing the performance of three OCR models — **Pytesseract**, **EasyOCR**, and **TrOCR** — based on key evaluation metrics:  
- **CER (Character Error Rate)** — lower is better  
- **WER (Word Error Rate)** — lower is better  
- **Similarity** — higher indicates closer text matching  
- **Time (s)** — average time taken per image  

| Model        | Average CER | Average WER | Average Similarity | Average Time (s) |
|---------------|--------------|--------------|---------------------|------------------|
| **Pytesseract** | 0.1640       | 0.295        | 0.586               | 7.66             |
| **EasyOCR**     | 0.1496       | 0.274        | 0.786               | 1.08             |
| **TrOCR**       | 0.0905       | 0.1600       | 0.351               | 12.60            |

###  Observations
- **TrOCR** achieved the **lowest error rates (CER & WER)**, indicating the most accurate recognition on complex images.  
- **EasyOCR** showed **balanced performance**, offering a strong trade-off between accuracy and speed.  
- **Pytesseract** performed the slowest and less accurately compared to modern deep-learning-based OCRs.  
- **TrOCR’s Similarity score** (0.351) is lower because it was tested on a **different evaluation image**, highlighting that deep models may still need fine-tuning for diverse datasets.

###  Conclusion
- **TrOCR** excels in accuracy for high-quality or printed text but may need more optimization for generalization.  
- **EasyOCR** remains the most **efficient and practical choice** for real-time or large-scale document OCR tasks.  
- **Pytesseract**, while reliable for basic OCR tasks, struggles with complex layouts and modern document images.

