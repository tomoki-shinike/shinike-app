import streamlit as st
from PIL import Image
from analyzer import analyze_video
from utils import save_graph_image, zip_results
import tempfile
import os
from io import BytesIO

st.set_page_config(page_title="Motion visualizer by shinike", layout="wide")

# ① タイトル（画像の直前に表示）
st.markdown("""
<div style='text-align: center'>
    <h1>動画を選択するだけで骨格の可視化と角度表示</h1>
</div>
""", unsafe_allow_html=True)

# ② 画像（主タイトルの下・副タイトルの上）
st.image("header_visual.png", use_column_width=True)

# ③ サブタイトル・説明文
st.markdown("""
<div style='text-align: center'>
    <p><i>Motion visualizer by shinike</i><br>
    <small>解析後、データが保存できます（撮影対象は1名を推奨）</small></p>
</div>
<hr>
""", unsafe_allow_html=True)

# ④ ファイルアップロード
uploaded_video = st.file_uploader("動画ファイルを選択してください（.mp4 または .mov）", type=["mp4", "mov"])

if uploaded_video:
    if st.button("分析を開始する"):
        with st.spinner("解析中...しばらくお待ちください。"):
            with tempfile.TemporaryDirectory() as tmpdir:
                video_bytes = BytesIO(uploaded_video.read())
                result = analyze_video(video_bytes, tmpdir)
                save_graph_image(result["csv_path"], result["graph_path"])
                zip_path = zip_results(
                    result["annotated_path"],
                    result["skeleton_path"],
                    result["csv_path"],
                    result["graph_path"],
                    os.path.join(tmpdir, "analysis_results.zip")
                )

                st.success("✅ 分析完了！以下の結果をご確認ください。")

                st.markdown("### 骨格付き動画")
                if os.path.exists(result["annotated_path"]):
                    with open(result["annotated_path"], "rb") as f:
                        video_data = f.read()
                        st.video(video_data)
                        st.download_button("📥 骨格付き動画をダウンロード", video_data, "annotated_video.mp4", mime="video/mp4")
                else:
                    st.error("❌ 骨格付き動画が見つかりませんでした。")

                st.markdown("### スティックピクチャー動画")
                if os.path.exists(result["skeleton_path"]):
                    with open(result["skeleton_path"], "rb") as f:
                        skeleton_data = f.read()
                        st.video(skeleton_data)
                        st.download_button("📥 骨格だけの動画をダウンロード", skeleton_data, "skeleton_video.mp4", mime="video/mp4")
                else:
                    st.error("❌ 骨格だけの動画が見つかりませんでした。")

                st.image(result["graph_path"], caption="関節角度の推移グラフ")

                with open(result["csv_path"], "rb") as f:
                    st.download_button("CSVをダウンロード", f, file_name="angles.csv")

                with open(zip_path, "rb") as f:
                    st.download_button("ZIP一括ダウンロード", f, file_name="analysis_results.zip")

with st.expander("📝 利用上の注意 / Terms of Use", expanded=False):
    st.markdown("""
- 本ツールは教育・研究目的で提供されています。医療目的や商用利用は行わないでください。  
- 分析結果の正確性や適合性は保証されません。参考情報としてご活用ください。  
- 使用しているツールの関係上、角度は各ランドマークが成す角を表記しています。  

This tool is for educational and research purposes only.  
Do not use for medical or commercial purposes.  
Accuracy and fitness of results are not guaranteed.
Due to the nature of the tools used, the angles represent those formed by specific landmarks.
""")
