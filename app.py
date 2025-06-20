import streamlit as st
from PIL import Image  # 画像表示用に追加
from analyzer import analyze_video
from utils import save_graph_image, zip_results
import tempfile
import os

# ページ設定
st.set_page_config(page_title="Motion visualizer by shinike", layout="wide")

# ロゴ画像の読み込みと表示
try:
    image = Image.open("アイコン例.png")  # アップロードしたファイル名と一致させる
    st.image(image, width=180)
except FileNotFoundError:
    st.warning("ロゴ画像（アイコン例.png）が見つかりませんでした。")

# タイトルと説明
st.markdown("""
<div style='text-align: center'>
    <h1>Motion visualizer by shinike</h1>
    <p><i>精緻な骨格可視化と動作解析を、誰でも簡単に。</i><br>
    <small>Posture and motion visualization powered by MediaPipe</small></p>
</div>
<hr>
""", unsafe_allow_html=True)

# ファイルアップロードと分析処理（以下略）
