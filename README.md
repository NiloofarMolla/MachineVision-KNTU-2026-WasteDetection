<div align="center">
  <h1> 🤖 Robotics and Machine Vision </h1>
  <h3> K. N. Toosi University of Technology (KNTU) </h3>
  <h4> ARAS Neura Academy </h4>
  <p>
    <strong>Instructors:</strong> <a href="https://www.linkedin.com/in/mjahmadi/">Mohammad Javad Ahmadi</a> & <a href="https://www.linkedin.com/in/hamid-taghirad/">Prof. Hamid D. Taghirad</a>
  </p>
</div>

## 📝 Project Title
> **Waste Detection on TACO Dataset using YOLOv8**

A robotic machine vision project focused on **waste detection** using the **TACO dataset** and modern deep learning detectors.  
We preprocess TACO into **high-level** and **image-level** class subsets, train multiple models (YOLOv8s, Faster R-CNN, Mask R-CNN), and analyze their performance to find a robust detector that can be integrated into a **robotic waste sorting system**.  

In this course project, we implemented and evaluated the **Detection phase** (Scan + Detect + Evaluate models).  
The Pick & Place phase for the robot was not completed and is considered future work.

---

## 🎥 Product Pitch & Demos
Watch the full presentation and demonstration of the project here:
- [**YouTube Video**](Link-Here)
- [**Aparat Video**](Link-Here)

- [**simulation Video**](Link-Here)

📄 **[Project Report & Documentation (Google Drive)](Link-Here)**

---

## 👥 Team Members
| Name | Student ID | GitHub Profile | Role / Contribution |
| :--- | :--- | :--- | :--- |
| [Niloofar Molla] | `40122903` | [@username](https://github.com/NiloofarMolla) | model training & Simulation & Path Planning |
| [Mohadese Alirezaee] | `40121123` | [@username](https://github.com/username) | model training & Report writing & documentation |
| [Arshia Ebrahimi] | `40002243` | [@username](https://github.com/earshia82) | model training & Dataset preprocessing |

---

## 📂 Repository Structure
```text
Project-Name/
├── code/              # Source code for algorithms and main scripts and simulation
├── docs/              # Reports, diagrams, and supplementary documentation
├── media/             # Images, GIFs, and media used in this README
├── data/              # Dataset of TACO
├── .gitignore          
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## ⚙️ Installation & Requirements
Provide step-by-step instructions to set up the environment and run your code.

1. Clone the repository:
   ```bash
   git clone https://github.com/NiloofarMolla/MachineVision-KNTU-2026-WasteDetection.git
   ```
2. Navigate to the directory:
   ```bash
   cd MachineVision-KNTU-2026-WasteDetection
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage & Execution

### 1️⃣ Dataset Preparation (TACO → Custom Subsets)

This project uses the **TACO** dataset and converts it into several custom subsets to improve model training.  
Scripts in the `code/` folder handle the following steps:

- Remapping the original TACO annotations into a **60-class high-level** subset.
- Building **image-level** subsets, including:
  - a 16-class configuration,
  - and a 13-class configuration where some low-frequency or overlapping classes are **removed** or **merged**.

These preprocessing steps make the classes more coherent and balanced, which helps the detectors learn more reliably and become more suitable for robotic applications.

---

### 2️⃣ Model Training (YOLOv8s on TACO Subsets)

After preprocessing, a **YOLOv8s** detector is trained on the different TACO subsets, including:

- a **60-class batch-level** setting (high-level mapping applied to the full dataset),
- **image-level** configurations with 16 classes,
- and an **image-level 13-class** configuration where classes are carefully **removed** or **merged** based on data analysis.

For each configuration, training hyperparameters (number of epochs, batch size, etc.) are chosen according to the available hardware and the goals of the project, allowing a fair comparison and analysis of model performance across different scenarios.

---

### 3️⃣ Webots Detection (UR5e Simulation Integration)

In the simulation phase, the trained YOLOv8s weights are integrated into a **Webots** environment with a **UR5e** robot to visually inspect and debug detection results.  
Controller scripts in the `code/` folder implement:

- loading the trained YOLOv8s weights,
- connecting to the Webots camera and receiving image frames,
- running detection on each frame,
- and overlaying **bounding boxes** and **class labels** on the camera view for visual debugging and performance analysis.

In this course project, only the **Detection and Visualization** stages of the robotic pipeline are implemented.  
The **Pick & Place** stage (grasping and sorting waste with the UR5e robot and gripper) is **not implemented** and is considered **future work**.


```bash
python code/train_yolov8_highlevel.py --config configs/highlevel.yaml
```
*(Add screenshots or GIFs of your project running here to make it visually appealing!)*

---

## 📊 Results & Achievements
We trained several models on different TACO subsets and compared mAP, precision, and recall.

Summary of key results:

YOLOv8s (batch-level, 60 classes) achieved moderate performance withmAP50 ≈ 0.143, mAP50-95 ≈ 0.117, precision ≈ 0.40, recall ≈ 0.12–0.13.
Faster R-CNN (60 classes) performed worse on this setupwith mAP50 ≈ 0.068, precision ≈ 0.28, recall ≈ 0.073.
Transitioning to image-level subsets improved performance:
16 classes: mAP50 ≈ 0.22, mAP50-95 ≈ 0.186, precision ≈ 0.29, recall ≈ 0.27.
13 classes (class removal): mAP50 ≈ 0.184, mAP50-95 ≈ 0.217, precision ≈ 0.248, recall ≈ 0.208.
13 classes (class merging): best overall model withmAP50 ≈ 0.253, mAP50-95 ≈ 0.203, precision ≈ 0.29, recall ≈ 0.25.
This shows that:

Carefully reducing and merging classes on TACO
And switching from a large 60-class scenario to smaller, more coherent subsets
significantly improves detection quality and makes the model more suitable for downstream robotic applications.

Challenges
During the project we faced several important challenges:

The usable portion of TACO for our experiments was relatively small, making it hard to train deep models without overfitting.
The dataset is highly imbalanced, with some classes having many samples and others being very rare.
Many objects are small and appear in cluttered scenes, which makes detection difficult and reduces mAP.
Designing good high-level and image-level class mappings required experimentation and multiple training runs to achieve stable results.
Despite these challenges, we achieved a consistent improvement across models and identified a strong YOLOv8s-based detector for waste detection.

---
 
