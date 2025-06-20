import streamlit as st
from PIL import Image  # 追加
from analyzer import analyze_video
from utils import save_graph_image, zip_results
import tempfile
import os

# ページ設定
st.set_page_config(page_title="Motion visualizer by shinike", layout="wide")

# 画像の表示（中央揃え）
with st.container():
    try:
        image = Image.open("アイコン例.png")
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.image(image, width=180)
        st.markdown("</div>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("ロゴ画像（アイコン例.png）が見つかりませんでした。")

# ヘッダー
st.markdown(
    """
    <div style='text-align: center'>
        <h1>Motion visualizer by shinike</h1>
        <p><i>精緻な骨格可視化と動作解析を、誰でも簡単に。</i><br>
        <small>Posture and motion visualization powered by MediaPipe</small></p>
    </div>
    <hr>
    """, unsafe_allow_html=True
)

# ファイルアップロード
uploaded_video = st.file_uploader("動画ファイルを選択してください（.mp4 または .mov）", type=["mp4", "mov"])

# 分析開始ボタン
if uploaded_video:
    if st.button("分析を開始する"):
        with st.spinner("解析中...しばらくお待ちください。"):
            with tempfile.TemporaryDirectory() as tmpdir:
                result = analyze_video(uploaded_video, tmpdir)
                save_graph_image(result["csv_path"], result["graph_path"])
                zip_path = zip_results(
                    result["annotated_path"],
                    result["skeleton_path"],
                    result["csv_path"],
                    result["graph_path"],
                    os.path.join(tmpdir, "analysis_results.zip")
                )

                st.success("✅ 分析完了！以下の結果をご確認ください。")

                st.video(result["annotated_path"], format="video/mp4")
                st.video(result["skeleton_path"], format="video/mp4")
                st.image(result["graph_path"], caption="関節角度の推移グラフ")

                with open(result["csv_path"], "rb") as f:
                    st.download_button("CSVをダウンロード", f, file_name="angles.csv")

                with open(zip_path, "rb") as f:
                    st.download_button("ZIP一括ダウンロード", f, file_name="analysis_results.zip")

# 利用上の注意
with st.expander("📝 利用上の注意 / Terms of Use", expanded=False):
    st.markdown("""
- 本ツールは教育・研究目的で提供されています。医療目的や商用利用は行わないでください。  
- 分析結果の正確性や適合性は保証されません。参考情報としてご活用ください。  

This tool is for educational and research purposes only.  
Do not use for medical or commercial purposes.  
Accuracy and fitness of results are not guaranteed.
""")
