# 📚 Docs Folder

This directory contains the **project documentation** for the  
_MachineVision-KNTU-2026-WasteDetection_ repository.

It is mainly used for storing the written report and presentation materials
that support the experimental code and results.

---

## 📄 Files

### 🔹 `Project (1).pdf`
This file is the main **course project report**.

It typically includes:

- Problem definition: **waste detection** using computer vision.
- Dataset description: how the **TACO** dataset is adapted to custom class sets.
- Model overview:
  - Faster R-CNN and Mask R-CNN baselines,
  - YOLOv8s experiments on 60, 16 and 13 classes.
- Training setup and evaluation metrics.
- Result tables and visual examples of detections.
- Discussion of limitations:
  - restricted dataset size and class imbalance,
  - only detection implemented in simulation (no Pick & Place),
  - hardware and time constraints.
- Future work and possible extensions for robotic waste sorting.

Use this document when you need a **high-level explanation** of the project,
for grading, review, or sharing with non-technical audiences.

---

## 🎤 Presentation Slides (PowerPoint)

A **PowerPoint slide deck** is also stored in this folder  

The slide deck is intended for:

- Classroom or conference presentations.
- Summarizing key ideas of the project in a visual format.
- Showing selected detection results, comparison tables,
  and an overview of the Webots/UR5e simulation concept.

Typical slide contents:

- Title & team members.
- Motivation and problem statement.
- Dataset and preprocessing pipeline (high-level / image-level class mapping).
- Model architecture snapshots (Faster R-CNN, Mask R-CNN, YOLOv8s).
- Experimental setup and main metrics.
- Best-performing configurations and qualitative results.
- Limitations and future work (e.g., full robotic Pick & Place).

---

## 🔎 How to Use This Folder

- Open `Project (1).pdf` to **understand the project story** end-to-end.
- Use the PowerPoint file when preparing or rehearsing your **oral presentation**.
- For technical details (datasets, training scripts, simulation code),
  refer to:
  - [`code/README.md`](../code/README.md)
  - and the main [`README.md`](../README.md) at the repository root.

This folder is the **communication layer** of the project:
it explains what the code does, why the experiments matter,
and how the results should be interpreted. 📝✨
