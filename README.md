
---

```markdown
# 🚀 CleanCropper

### ⚡ Turn annotated datasets into clean, ML-ready image crops in seconds.

> A lightweight Python utility that extracts individual objects from annotated images (YOLO-style polygons) and converts them into structured training datasets.

---

# 🧠 The Problem

Working with computer vision datasets is messy:

- Labels are hard to visualize  
- Objects are trapped inside full images  
- Dataset cleaning takes hours of scripting  
- No simple tool exists for instant object cropping from annotations  

---

# ✨ The Solution

CleanCropper automates the entire dataset cropping pipeline.

Drop your dataset → run one script → get clean object-level images ready for ML training.

---

# ⚙️ What CleanCropper Does

1. 🧹 Clean workspace  
   Removes old extracted data to avoid conflicts  

2. 📦 Extract dataset  
   Unzips your dataset automatically  

3. 📍 Locate files  
   Detects `images/` and `labels/` folders  

4. ✂️ Crop objects  
   Converts polygon annotations → bounding boxes → cropped images  

5. 🧠 Remove duplicates  
   Uses MD5 hashing to avoid repeated crops  

6. 💾 Export dataset  
   Saves structured, timestamped output folders  

---

# 📥 Input Format

Your dataset should be a `.zip` file structured like this:

```

images/   → .jpg, .png files
labels/   → annotation .txt files

```

---

# 📄 Annotation Format (YOLO Polygon Style)

Each line represents one object:

```

<class_id> x1 y1 x2 y2 x3 y3 ...

```

### Example:

```

0  0.12 0.34  0.45 0.34  0.45 0.78  0.12 0.78
1  0.50 0.10  0.80 0.10  0.80 0.50  0.50 0.50

````

- Coordinates are normalized (0 → 1)  
- Relative to image width & height  

---

# ▶️ How to Run

```bash
python cleancropper.py
````

✔ Shows progress
✔ Confirms before processing
✔ Generates output automatically

---

# 📁 Output Structure

Every run creates a timestamped folder:

```
cropped_clean/
  crops_YYYYMMDD_HHMMSS/
    image_class0_obj1.jpg
    image_class1_obj2.jpg
```

---

# 🧰 Features

| Feature                | Description                        |
| ---------------------- | ---------------------------------- |
| 🧹 Fresh Start         | Auto-cleans previous runs          |
| 🧩 Polygon Support     | Handles YOLO-style polygons        |
| 🧠 Smart Deduplication | Removes duplicate crops (MD5 hash) |
| 🕒 Timestamped Output  | No file overwrites                 |
| 🛡 Boundary Safety     | Keeps crops within image limits    |
| ⚡ Fault Tolerant       | Continues even if one file fails   |

---

# 📊 Output Summary

After execution, CleanCropper displays:

* Total crops generated
* Duplicate crops skipped
* Output directory path

---

# ⚠️ Common Issues

## ❌ Zip file not found

Ensure:

```
ZIP_FILE path is correct
```

## ❌ Missing folders

ZIP must contain:

```
images/ and labels/
```

## ❌ No crops generated

Check:

* image-label filename match
* correct annotation format

---

# 📂 Project Structure

```
CleanCropper/
│
├── cleancropper.py        # Main script
├── inputfile.zip          # Dataset input
├── extracted_data/        # Temporary workspace
└── cropped_clean/         # Output dataset
```

---

# 🎯 Use Cases

* Computer vision dataset preprocessing
* Object detection → classification dataset conversion
* Dataset cleaning pipelines
* ML model training preparation
* Kaggle / research dataset setup

---

# 👩‍💻 Author

**Swastika Khamaru**

---

# 🧠 One-Line Summary

CleanCropper turns messy annotated datasets into clean, structured, ML-ready object crops — with zero manual effort.


