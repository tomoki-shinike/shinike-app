import cv2
import numpy as np
import mediapipe as mp
import pandas as pd
import os
import math

def analyze_video(uploaded_file, output_dir):
    def calculate_angle(a, b, c):
        ba = [a[i] - b[i] for i in range(3)]
        bc = [c[i] - b[i] for i in range(3)]
        cosine = sum(ba[i] * bc[i] for i in range(3)) / (
            (sum(x * x for x in ba) ** 0.5) * (sum(x * x for x in bc) ** 0.5) + 1e-6
        )
        return math.degrees(math.acos(min(1.0, max(-1.0, cosine))))

    temp_input = os.path.join(output_dir, "input_video.mp4")
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.read())
        f.flush()
        os.fsync(f.fileno())

    cap = cv2.VideoCapture(temp_input)
    if not cap.isOpened():
        raise RuntimeError("❌ 動画ファイルの読み込みに失敗しました。")

    width, height = int(cap.get(3)), int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    annotated_path = os.path.join(output_dir, "annotated_output.mp4")
    skeleton_path = os.path.join(output_dir, "skeleton_black.mp4")
    csv_path = os.path.join(output_dir, "angles.csv")
    graph_path = os.path.join(output_dir, "angles_graph.png")

    codec = cv2.VideoWriter_fourcc(*'avc1')
    annotated_writer = cv2.VideoWriter(annotated_path, codec, fps, (width, height))
    skeleton_writer = cv2.VideoWriter(skeleton_path, codec, fps, (width, height))

    pose = mp.solutions.pose.Pose(static_image_mode=False)
    drawing = mp.solutions.drawing_utils
    style = mp.solutions.drawing_styles

    angles_data = []
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        skeleton_frame = np.zeros_like(frame)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            get = lambda i: [lm[i].x, lm[i].y, lm[i].z]

            shoulder_l = calculate_angle(get(13), get(11), get(23))
            hip_l     = calculate_angle(get(11), get(23), get(25))
            knee_l    = calculate_angle(get(23), get(25), get(27))
            ankle_l   = calculate_angle(get(25), get(27), get(31))

            shoulder_r = calculate_angle(get(14), get(12), get(24))
            hip_r     = calculate_angle(get(12), get(24), get(26))
            knee_r    = calculate_angle(get(24), get(26), get(28))
            ankle_r   = calculate_angle(get(26), get(28), get(32))

            angles_data.append([
                frame_id,
                shoulder_l, shoulder_r,
                hip_l, hip_r,
                knee_l, knee_r,
                ankle_l, ankle_r
            ])

            # ポーズを描画（角度ラベルは描かない）
            drawing.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
            drawing.draw_landmarks(skeleton_frame, results.pose_landmarks,
                                   mp.solutions.pose.POSE_CONNECTIONS,
                                   style.get_default_pose_landmarks_style())

        annotated_writer.write(frame)
        skeleton_writer.write(skeleton_frame)
        frame_id += 1

    cap.release()
    annotated_writer.release()
    skeleton_writer.release()

    df = pd.DataFrame(angles_data, columns=[
        "Frame", "Shoulder_L", "Shoulder_R",
        "Hip_L", "Hip_R", "Knee_L", "Knee_R",
        "Ankle_L", "Ankle_R"
    ])
    df.to_csv(csv_path, index=False)

    return {
        "annotated_path": annotated_path,
        "skeleton_path": skeleton_path,
        "csv_path": csv_path,
        "graph_path": graph_path
    }
