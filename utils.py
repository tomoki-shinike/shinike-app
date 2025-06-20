# utils.py
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

def save_graph_image(csv_file, save_path):
    df = pd.read_csv(csv_file)
    plt.figure(figsize=(12, 6))
    for col in ['Shoulder', 'Trunk', 'Hip', 'Knee', 'Ankle']:
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
            zipf.write(file, arcname=os.path.basename(file))
    return zip_path