from controller import Robot, Camera
import cv2
import numpy as np
from ultralytics import YOLO
import math

# ==================== YOLO CONFIG ====================

YOLO_MODEL_PATH = 'best.pt'
CONF_UNKNOWN_THRESHOLD = 0.15
MIN_DETECTION_CONF = 0.35  # Detection های خیلی ضعیف را رد کن

HIGH_LEVEL_CLASSES = [
    "Glass",
    "Metal",
    "PaperCard",
    "PlasticBottle",
    "PlasticFilmBag",
    "Container",
    "CigaretteItem",
    "CupItem",
    "BagWrapper",
    "MiscPlastic",
    "UnlabeledItem",
    "BottleCapItem",
    "Straw",
]

CLASS_STATE = {
    "Glass": "recyclable",
    "Metal": "recyclable",
    "PaperCard": "recyclable",
    "PlasticBottle": "recyclable",
    "PlasticFilmBag": "recyclable",
    "Container": "recyclable",
    "BottleCapItem": "recyclable",

    "CigaretteItem": "non_recyclable",
    "CupItem": "non_recyclable",
    "BagWrapper": "non_recyclable",
    "MiscPlastic": "non_recyclable",
    "Straw": "non_recyclable",

    "UnlabeledItem": "unknown",
}

UNLABELED_CLASS_NAME = "UnlabeledItem"

BIN_COLOR_RECYCLABLE = 'green'
BIN_COLOR_NON_RECYCLABLE = 'red'
BIN_COLOR_UNKNOWN = 'yellow'


def interpret_detection(cls_name: str, conf: float):
    if conf < CONF_UNKNOWN_THRESHOLD:
        return "unknown", "low_confidence"
    if cls_name == UNLABELED_CLASS_NAME:
        return "unknown", "unlabeled_class"
    state = CLASS_STATE.get(cls_name, "unknown")
    return state, "none"


def decide_bin_from_state(state: str) -> str:
    if state == "recyclable":
        return BIN_COLOR_RECYCLABLE
    elif state == "non_recyclable":
        return BIN_COLOR_NON_RECYCLABLE
    else:
        return BIN_COLOR_UNKNOWN


# ==================== WEBOTS INIT ====================

robot = Robot()
timestep = int(robot.getBasicTimeStep())

camera: Camera = robot.getDevice('waste_camera')
camera.enable(timestep)

joint1 = robot.getDevice('shoulder_pan_joint')
joint2 = robot.getDevice('shoulder_lift_joint')
joint3 = robot.getDevice('elbow_joint')
joint4 = robot.getDevice('wrist_1_joint')
joint5 = robot.getDevice('wrist_2_joint')
joint6 = robot.getDevice('wrist_3_joint')

arm_joints = [joint1, joint2, joint3, joint4, joint5, joint6]
for j in arm_joints:
    j.setVelocity(1.0)

pose_home = [0.0, -1.2, 1.8, -1.5, 0.0, 0.0]

SCAN_FIXED_POSE = [-1.0, 1.5, -1.3, 0.0, 0.0]  # joint2..joint6


def move_arm_to_home():
    for joint, target in zip(arm_joints, pose_home):
        joint.setPosition(target)


def move_arm_to_scan_pose_without_shoulder():
    joints_without_shoulder = arm_joints[1:]  # joint2..joint6
    for joint, target in zip(joints_without_shoulder, SCAN_FIXED_POSE):
        joint.setPosition(target)


move_arm_to_home()
move_arm_to_scan_pose_without_shoulder()

# ==================== YOLO MODEL ====================

model = YOLO(YOLO_MODEL_PATH)
model_names = model.names

# ==================== OBJECT MEMORY ====================

MEMORY_TIMEOUT_STEPS = 500
MERGE_DISTANCE_PIXELS = 70 

class DetectedObject:
    def __init__(self, object_id, cls_name, conf, bbox, center, state_label, bin_color, current_step, dist_to_center):
        self.id = object_id
        self.class_name = cls_name
        self.max_conf = conf
        self.bbox = bbox               # (x1, y1, x2, y2)
        self.center = center           # (cx, cy)
        self.state = state_label       # recyclable / non_recyclable / unknown
        self.bin = bin_color
        self.first_seen_step = current_step
        self.last_seen_step = current_step
        self.detected_count = 1
        self.dist_to_image_center = dist_to_center

    def update(self, conf, bbox, center, current_step, dist_to_center):
        self.max_conf = max(self.max_conf, conf)
        self.bbox = bbox
        self.center = center
        self.last_seen_step = current_step
        self.detected_count += 1
        self.dist_to_image_center = dist_to_center


objects = []        
next_object_id = 1    


def distance(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def is_same_object(obj: DetectedObject, cls_name, center, bbox):

    if obj.class_name != cls_name:
        return False


    d = distance(center, obj.center)
    if d > MERGE_DISTANCE_PIXELS:
        return False

   
    old_area = (obj.bbox[2] - obj.bbox[0]) * (obj.bbox[3] - obj.bbox[1])
    new_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

    if old_area <= 0 or new_area <= 0:
        return True

    area_ratio = new_area / old_area
    if area_ratio < 0.5 or area_ratio > 2.0:
        return False

    return True


def find_existing_object(cls_name, center, bbox):
    for obj in objects:
        if is_same_object(obj, cls_name, center, bbox):
            return obj
    return None


def add_new_object(cls_name, conf, bbox, center, current_step, state_label, bin_color, dist_to_center):
    global next_object_id, pause_steps_after_new_object

    obj = DetectedObject(
        object_id=next_object_id,
        cls_name=cls_name,
        conf=conf,
        bbox=bbox,
        center=center,
        state_label=state_label,
        bin_color=bin_color,
        current_step=current_step,
        dist_to_center=dist_to_center
    )

    objects.append(obj)
    next_object_id += 1

    print(
        f"[OBJECT] NEW: id={obj.id}, class={cls_name}, center={center}, conf={conf:.2f}, "
        f"state={state_label}, bin={bin_color}, step={current_step}"
    )

    pause_steps_after_new_object = PAUSE_DURATION_STEPS


def prune_memory(current_step):
    global objects
    before = len(objects)
    objects = [
        obj for obj in objects
        if (current_step - obj.last_seen_step) < MEMORY_TIMEOUT_STEPS
    ]
    after = len(objects)
    if after < before:
        print(f"[MEMORY] Pruned objects: {before} -> {after} at step={current_step}")


# ==================== STATE & SCAN CONFIG ====================

STATE_SCAN = "scan"
state = STATE_SCAN

scan_angle = 0.0
scan_speed = 0.02
max_scan_angle = math.radians(180)
scan_direction = 1

pause_steps_after_new_object = 0
PAUSE_DURATION_STEPS = 20

FRAME_SKIP_FOR_YOLO = 10
frame_counter = 0

frames_without_detection = 0
NO_DETECTION_TIMEOUT = 200

sweep_count = 0

print("[SYSTEM] Starting Phase 1 (enhanced): Scan + Detect + Object Memory + Visualization.")

current_step = 0

while robot.step(timestep) != -1:
    current_step += 1
    frame_counter += 1

 
    if pause_steps_after_new_object > 0:
        pause_steps_after_new_object -= 1
    else:
        previous_scan_angle = scan_angle

        scan_angle += scan_direction * scan_speed
        if scan_angle > max_scan_angle:
            scan_angle = max_scan_angle
            scan_direction = -1
            sweep_count += 1
            print(f"[SWEEP] Completed sweep #{sweep_count} at step={current_step}")
        elif scan_angle < -max_scan_angle:
            scan_angle = -max_scan_angle
            scan_direction = 1
            sweep_count += 1
            print(f"[SWEEP] Completed sweep #{sweep_count} at step={current_step}")

    joint1.setPosition(scan_angle)
    move_arm_to_scan_pose_without_shoulder()


    image = camera.getImage()
    width = camera.getWidth()
    height = camera.getHeight()
    frame_bgra = np.frombuffer(image, np.uint8).reshape((height, width, 4))
    frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    img_center = (width / 2.0, height / 2.0)

    if state == STATE_SCAN:
        if frame_counter % FRAME_SKIP_FOR_YOLO != 0:
            continue

        results = model(frame_bgr, verbose=False)
        any_detection_this_frame = False

        if len(results) > 0:
            r = results[0]
            if r.boxes is not None and len(r.boxes) > 0:
                boxes = r.boxes

                for box in boxes:
                    conf = float(box.conf.item())
                    if conf < MIN_DETECTION_CONF:
                        continue

                    cls_id = int(box.cls.item())
                    cls_name = model_names[cls_id]

                    xyxy = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = xyxy
                    cx = (x1 + x2) / 2.0
                    cy = (y1 + y2) / 2.0
                    center = (cx, cy)
                    bbox = (x1, y1, x2, y2)

                    any_detection_this_frame = True

                    state_label, reason = interpret_detection(cls_name, conf)
                    bin_color = decide_bin_from_state(state_label)

                    dist_to_center = distance(center, img_center)

                    existing = find_existing_object(cls_name, center, bbox)

                    if existing is not None:
                        existing.update(conf, bbox, center, current_step, dist_to_center)
                    else:
                        add_new_object(cls_name, conf, bbox, center, current_step, state_label, bin_color, dist_to_center)

                    # Visualization روی همان فریم
                    if bin_color == BIN_COLOR_RECYCLABLE:
                        color = (0, 255, 0)
                    elif bin_color == BIN_COLOR_NON_RECYCLABLE:
                        color = (0, 0, 255)
                    else:
                        color = (0, 255, 255)

                    cv2.rectangle(
                        frame_bgr,
                        (int(x1), int(y1)),
                        (int(x2), int(y2)),
                        color,
                        2
                    )

                    label = f"{cls_name} ({state_label}) {conf:.2f}"
                    cv2.putText(
                        frame_bgr,
                        label,
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        color,
                        1,
                        cv2.LINE_AA
                    )

        if any_detection_this_frame:
            frames_without_detection = 0
        else:
            frames_without_detection += 1
            if frames_without_detection > NO_DETECTION_TIMEOUT:
                print("[SCAN] No detections for a long time, still sweeping...")
                frames_without_detection = 0

     
        if current_step % 200 == 0:
            prune_memory(current_step)

    
        if current_step % 300 == 0:
            print(f"[SUMMARY] step={current_step}, objects_count={len(objects)}, sweeps={sweep_count}")
            for obj in objects:
                print(
                    f"  ID={obj.id}, class={obj.class_name}, state={obj.state}, bin={obj.bin}, "
                    f"max_conf={obj.max_conf:.2f}, detected_count={obj.detected_count}, "
                    f"first_seen={obj.first_seen_step}, last_seen={obj.last_seen_step}"
                )
