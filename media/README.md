# 🎨 Media Folder

This directory contains all **visual and multimedia assets** used in the  
_MachineVision-KNTU-2026-WasteDetection_ project.

It includes:

- Dataset image samples (train/val/test),
- YOLO detection output screenshots,
- high-level annotation files for the custom TACO subsets,
- and project videos (simulation demo + product pitch).

These assets are referenced from the main [`README.md`](../README.md)  
and from the project report in `docs/`.

---

## 📂 Subfolders

### 🖼 `train_images/train_images`
Representative **training images** from the adapted TACO dataset.

- Used for:
  - showing examples of waste scenes,
  - illustrating the variety of classes and backgrounds.
- Can be embedded in documentation to explain the data distribution.

> Example usage in Markdown:  
> `![Sample training image](media/train_images/train_images/example_train.png)`

---

### 🧪 `test_images/test_images`
Selected **test images** used to evaluate and visualize detection results.

- Contains images **not** seen during training.
- Ideal for:
  - qualitative comparison between models,
  - showing real performance on unseen data.

> Example usage:  
> `![Sample test image](media/test_images/test_images/example_test.png)`

---

### 📊 `val_images/val_images`
Images from the **validation set**.

- Used during training to:
  - monitor overfitting,
  - tune hyperparameters.
- Screenshots from this folder may be used to explain validation behavior in the report or slides.

> Example usage:  
> `![Sample validation image](media/val_images/val_images/example_val.png)`

---

### ✅ `yolo_outputs/yolo_outputs`
Visual **YOLOv8 detection outputs**.

- Contains images with:
  - bounding boxes,
  - class labels,
  - confidence scores.
- Used to:
  - demonstrate the detector’s qualitative performance,
  - compare different class configurations (60 / 16 / 13 classes),
  - provide figures for the report and presentation.

> Example usage:  
> `![YOLOv8 detection output](media/yolo_outputs/yolo_outputs/example_output.png)`

---

## 📝 Annotation Files

### 🔹 `annotations_train_high.json`  
### 🔹 `annotations_val_high.json`  
### 🔹 `annotations_test_high.json`

High-level annotation files for the **custom TACO subsets**.

- Store bounding boxes and class labels for:
  - **train**, **validation**, and **test** splits.
- Reflect the **high-level class mapping** (e.g., 60-class remapping).
- Used by the training notebooks in `code/` to load data consistently.

These files document the **exact label configuration** used in experiments,  
ensuring the project is reproducible.

---

## 🎥 Project Videos

The `media/` folder also contains two key video assets  
(filenames may vary, e.g. `simulation_demo.mp4`, `product_pitch.mp4`):

### ▶ Simulation Demo Video
A short video demonstrating:

- The **Webots** environment,
- the **UR5e** robot,
- integration of YOLOv8 detection with the simulated camera,
- visual bounding boxes around detected waste items.

This video is used to show how the trained detector behaves in a **robotics context**,  
even though full Pick & Place is not implemented yet.

---

### 💼 Product Pitch Video
A concise **product pitch** for the project.

- Explains the problem of waste management.
- Presents the vision of an **AI-powered robotic waste sorting system**.
- Highlights:
  - dataset choice (TACO),
  - detection pipeline (YOLOv8),
  - potential real-world applications (smart bins, recycling centers).

This video is intended for **non-technical stakeholders**, judges, or course presentations.

---

## 📌 How to Use This Folder

- Use dataset images (train_images, val_images, test_images) to explain:

scene complexity,
class imbalance,
typical examples of recyclable vs non-recyclable waste.
Use YOLO outputs and videos to visually support:

results sections in the report,
slides in the presentation,
and the Usage & Results sections of the main README.md.
This folder is the visual identity of the project —

it shows what the models see, how they perform, and

how the system is envisioned in a real-world product. 🌍✨
