import streamlit as st
from PIL import Image
from analyzer import analyze_video
from utils import save_graph_image, zip_results
import tempfile
import os
import subprocess

# ページ設定
st.set_page_config(page_title="Motion visualizer by shinike", layout="wide")

# 📼 動画再エンコード関数
def reencode_video(input_path, output_path):
    command = [
        "ffmpeg",
        "-y",  # 上書き許可
        "-i", input_path,
        "-vcodec", "libx264",
        "-acodec", "aac",
        "-movflags", "+faststart",
        output_path
    ]
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        st.error("❌ ffmpeg による再エンコードに失敗しました")
        st.code(e.stderr.decode("utf-8"))
        return False
    return True

# ヘッダー
st.markdown("""
<div style='text-align: center'>
    <h1>動画を選択するだけで骨格の可視化と角度表示</h1>
    <p><i>Motion visualizer by shinike</i><br>
    <small>解析後、ページの一番下からデータがダウンロードできます（撮影対象は1名を推奨）</small></p>
</div>
<hr>
""", unsafe_allow_html=True)

# ファイルアップロード
uploaded_video = st.file_uploader("動画ファイルを選択してください（.mp4 または .mov）", type=["mp4", "mov"])

# 分析開始ボタン
if uploaded_video:
    if st.button("分析を開始する"):
        with st.spinner("解析中...しばらくお待ちください。"):
            with tempfile.TemporaryDirectory() as tmpdir:
                result = analyze_video(uploaded_video, tmpdir)
                save_graph_image(result["csv_path"], result["graph_path"])

                # 🔄 再エンコード先ファイルパス
                reencoded_annotated = os.path.join(tmpdir, "annotated_encoded.mp4")
                reencoded_skeleton = os.path.join(tmpdir, "skeleton_encoded.mp4")

                # 🔧 再エンコード実行
                reencode_video(result["annotated_path"], reencoded_annotated)
                reencode_video(result["skeleton_path"], reencoded_skeleton)

                zip_path = zip_results(
                    reencoded_annotated,
                    reencoded_skeleton,
                    result["csv_path"],
                    result["graph_path"],
                    os.path.join(tmpdir, "analysis_results.zip")
                )

                st.success("✅ 分析完了！以下の結果をご確認ください。")

                # ▶️ 表示・ダウンロード
                st.video(reencoded_annotated)
                with open(reencoded_annotated, "rb") as f:
                    st.download_button("📥 注釈付き動画をダウンロード", f, file_name="annotated_video.mp4", mime="video/mp4")

                st.video(reencoded_skeleton)
                with open(reencoded_skeleton, "rb") as f:
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
