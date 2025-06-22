import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

def save_graph_image(csv_file, save_path):
    df = pd.read_csv(csv_file)
    plt.figure(figsize=(12, 6))

    columns_to_plot = [
        "Shoulder_L", "Shoulder_R",
        "Hip_L", "Hip_R",
        "Knee_L", "Knee_R",
        "Ankle_L", "Ankle_R"
    ]

    for col in columns_to_plot:
        if col in df.columns:
            plt.plot(df['Frame'], df[col], label=col)

    plt.xlabel('Frame')
    plt.ylabel('Angle (°)')
    plt.title('Joint Angles Over Time')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def zip_results(video1_path, video2_path, csv_path, graph_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in [video1_path, video2_path, csv_path, graph_path]:
            if os.path.exists(file):
                zipf.write(file, arcname=os.path.basename(file))
    return zip_path
