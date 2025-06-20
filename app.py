import streamlit as st
from PIL import Image  # 追加
from analyzer import analyze_video
from utils import save_graph_image, zip_results
import tempfile
import os

# ページ設定
st.set_page_config(page_title="Motion visualizer by shinike", layout="wide")

# ヘッダー
st.markdown(
    """
    <div style='text-align: center'>
        <h1>動画を選択するだけで骨格の可視化と角度表示</h1>
        <p><i>Motion visualizer by shinike</i><br>
        <small>解析後、ページの一番下からデータがダウンロードできます（撮影対象は1名を推奨）</small></p>
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
with open(result["annotated_path"], "rb") as f:
    st.download_button("📥 注釈付き動画をダウンロード", f, file_name="annotated_video.mp4", mime="video/mp4")

                sst.video(result["skeleton_path"], format="video/mp4")
with open(result["skeleton_path"], "rb") as f:
    st.download_button("📥 骨格動画をダウンロード", f, file_name="skeleton_video.mp4", mime="video/mp4")

                       
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
