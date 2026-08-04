# 🧠 Code Folder

This directory contains all core notebooks used for waste detection experiments in the **MachineVision-KNTU-2026-WasteDetection** project.

It currently focuses on **CNN-based detectors** (Faster R-CNN, Mask R-CNN) and **YOLOv8** training on different TACO subsets and Webots/UR5e simulation controllers.

---

## 📂 File Overview

### 🔹 `faster_R_CNN.ipynb`
Notebook for training and evaluating a **Faster R-CNN** detector on the waste dataset.

- Loads the prepared TACO-based dataset.
- Configures Faster R-CNN backbone and detection heads.
- Trains the model and reports detection metrics.
- Used as a baseline to compare with YOLOv8 performance.

---

### 🔹 `mask_R_CNN.ipynb`
Notebook for **Mask R-CNN** instance segmentation on waste images.

- Performs object detection **and** pixel-level segmentation.
- Useful for analyzing how well the model separates overlapping waste items.
- Serves as a complementary baseline to bounding-box-only detectors.

---

### 🔹 `yolo_no_test.ipynb`
Initial YOLOv8 experiment notebook.

- Sets up basic YOLOv8 training on the waste dataset.
- Focuses mainly on training configuration and convergence.
- Limited or no test/evaluation phase; used as a quick prototype.

---

### 🔹 `yolov8s_batchlvl_batch16.ipynb`
YOLOv8s training on the **batch-level 60-class** configuration (TACO high-level mapping)  
with **batch size = 16**.

- Uses the full high-level 60-class label set.
- Optimized for slightly larger batch size (16) when enough GPU memory is available.
- Logs training loss and detection metrics for analysis.

---

### 🔹 `yolov8s_batchlvl_batch8.ipynb`
YOLOv8s training on the **batch-level 60-class** configuration  
with **batch size = 8**.

- Same label setup as the previous notebook (60 high-level classes).
- Lower batch size (8) for more constrained hardware.
- Allows direct comparison between batch size 8 vs 16 on the same dataset.

---

### 🔹 `yolov8s_imglvl_16class.ipynb`
YOLOv8s training on the **image-level 16-class** configuration.

- Works on a curated subset of 16 meaningful waste classes.
- Uses image-level prepared annotations for better class balance.
- Designed to study performance when reducing the number of classes.

---

### 🔹 `yolov8s_imglvl_13class.ipynb`
YOLOv8s training on the **image-level 13-class** configuration.

- Starts from the 16-class setup and applies class **merging**/**removal** based on data analysis.
- Targets more robust detection on a compact set of 13 classes.
- Used to compare how class reduction impacts mAP and per-class performance.

---

### 🔹 `yolov8s_imglvl_13class_delete.ipynb`
Experimental notebook focusing on **deleting / filtering** specific classes  
from the image-level configuration.

- Implements class removal rules and data filtering logic.
- Helps evaluate which classes should be kept, merged, or discarded.
- Supports the final design of the 13-class configuration.

---

## 🔮  Webots & UR5e Simulation

- Python controllers and utilities for **Webots** simulation.
- Scripts for integrating YOLOv8 detection with the **UR5e** robot.
- Code for visualizing bounding boxes and class labels in the simulated camera view.
- (Optional future work) logic for Pick & Place and waste sorting.

---

## 📌 Usage Notes

- All notebooks are designed to be run from the **root of the repository** with paths configured to use the `data/` and `media/` folders.
- For detailed installation, dataset preparation, and global usage instructions, see the main [`README.md`](../README.md) at the repository root.
