# CleanCropper

**Automated Image Crop Extractor from Annotated Datasets**

**Version:** 1.0
**Requirements:** Python 3.8+, Pillow

---

## 📌 What is CleanCropper?

CleanCropper is a Python utility designed for computer vision and machine learning workflows.
It processes a zipped dataset of annotated images, extracts individual objects based on polygon labels, and saves each object as a separate cropped image.

It helps you:

* Isolate labeled objects quickly
* Avoid duplicate crops
* Prepare datasets efficiently for training ML models

---

## ⚙️ How It Works

Each run follows this pipeline:

| Step           | Description                                             |
| -------------- | ------------------------------------------------------- |
| 1. Clean       | Deletes old `extracted_data/` to avoid leftover files   |
| 2. Extract     | Unzips the dataset into a fresh folder                  |
| 3. Locate      | Finds `images/` and `labels/` directories               |
| 4. Crop        | Converts polygon labels → bounding boxes → crops images |
| 5. Deduplicate | Uses MD5 hashing to skip identical crops                |
| 6. Save        | Stores crops in a timestamped output folder             |

---

## 🧰 Requirements

Install dependencies:

```bash
pip install Pillow
```

* Python 3.8 or higher
* No additional external libraries required

---

## 📥 Input Format

Your ZIP file must contain:

* `images/` (or `image/`) → image files (`.jpg`, `.png`, etc.)
* `labels/` (or `label/`) → annotation files (`.txt`)

### 📄 Label Format (YOLO Polygon Style)

Each line represents one object:

```
<class_id>  <x1> <y1>  <x2> <y2>  <x3> <y3> ...
```

### Example:

```
0  0.12 0.34  0.45 0.34  0.45 0.78  0.12 0.78
1  0.50 0.10  0.80 0.10  0.80 0.50  0.50 0.50
```

* Coordinates are normalized (0 → 1)
* Relative to image width & height

---

## ⚙️ Configuration

Edit these lines in the script:

```python
ZIP_FILE = "inputfile.zip"
OUTPUT_FOLDER = "cropped_clean"
```

---

## 📁 Output Structure

Each run creates a timestamped folder:

```
cropped_clean/
  crops_YYYYMMDD_HHMMSS/
    image_class0_obj1.jpg
    image_class1_obj2.jpg
```

### Naming Pattern:

```
<original_name>_class<class_id>_obj<object_number>.jpg
```

---

## ▶️ Running the Script

```bash
python cleancropper.py
```

* The script prints progress
* Pauses once for confirmation before cropping

---

## 📊 Output Summary

After execution, the script displays:

* Total crops saved
* Duplicate crops skipped
* Output folder location

---

## 🚀 Key Features

| Feature             | Description                                    |
| ------------------- | ---------------------------------------------- |
| Fresh Start         | Cleans previous extracted data automatically   |
| Polygon Support     | Converts polygon annotations to bounding boxes |
| Duplicate Detection | Uses MD5 hashing to skip identical crops       |
| Timestamped Output  | Prevents overwriting previous runs             |
| Boundary Safety     | Ensures crops stay within image limits         |
| Error Handling      | Continues processing even if one image fails   |

---

## ⚠️ Common Errors & Fixes

### ❌ Zip file not found

* Ensure correct path in `ZIP_FILE`
* Script prints expected path for debugging

### ❌ Missing folders

* ZIP must contain `images/` and `labels/`

### ❌ No crops saved

* Check:

  * Matching filenames between images and labels
  * Proper YOLO polygon format

---

## 📂 Project Structure

```
CleanCropper/
│
├── cleancropper.py        # Main script
├── inputfile.zip          # Input dataset
├── extracted_data/        # Temporary extracted files
└── cropped_clean/         # Output folder
    └── crops_timestamp/
```

---

## 💡 Use Cases

* Object detection dataset preparation
* Annotation processing pipelines
* ML model training preprocessing
* Data cleaning and augmentation

---

## 👩‍💻 Author

Swastika Khamaru

---

## 🧠 Summary

CleanCropper is a lightweight yet powerful tool for transforming annotated datasets into clean, structured image crops—ready for machine learning workflows.

---
