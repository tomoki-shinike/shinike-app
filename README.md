# 🎥 Motion visualizer by shinike

**骨格の可視化と動作解析を無料で簡単に。**  
_Posture and motion visualization powered by MediaPipe._

---

## 💡 概要 / Overview

アップロードされた動画に対して MediaPipe を用いた骨格分析を行い、関節の動きや角度を可視化する Web アプリです。

shinike is a web application that uses MediaPipe to analyze posture and joint angles from uploaded videos.

---

## 🧭 主な機能 / Features

- スティックピクチャー付き動画生成（注釈付き）
- 黒背景に骨格のみのスケルトン動画
- 肩・体幹・股関節・膝・足関節の角度を記録したCSV
- 時系列グラフ（PNG）
- すべてをZIPで一括ダウンロード可能

---

## 🚀 使い方 / How to Use

1. `.mp4` または `.mov` の動画をアップロード  
2. 「分析を開始する」ボタンをクリック  
3. 処理が完了すると、各種出力ファイルが表示／ダウンロード可能になります

---

## ⚠️ 注意事項 / Disclaimer

- 本ツールは教育・研究目的で提供されています  
- 医療的評価・診断・商用利用は行わないでください  
- 分析精度・再現性は保証されません  

This tool is intended for educational and research purposes only.  
Do not use it for commercial, diagnostic, or medical purposes.  
No guarantee is made regarding the accuracy or reliability of the analysis.

---

## 🧪 使用技術 / Built with

- Python
- Streamlit
- MediaPipe
- OpenCV
- Pandas