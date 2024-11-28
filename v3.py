import os
import google.generativeai as genai
import base64
import google.api_core.exceptions
import streamlit as st
from jinja2 import Environment, FileSystemLoader

# 起動command streamlit run v3.py --server.port 8080
# 環境変数からAPIキーを取得
api_key = os.environ.get('API_KEY')
if not api_key:
    st.error("APIキーが設定されていません。環境変数 'API_KEY' を設定してください。")
    st.stop()
genai.configure(api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

st.title("タイヤ保険 AI有無責判定システム")
st.write("3つの画像をアップロードしてください")

col1_upload, col2_upload, col3_upload = st.columns(3)
col1_preview, col2_preview, col3_preview = st.columns(3)

with col1_upload: image1 = st.file_uploader("タイヤの状態の写真", type=['jpg', 'jpeg'])
# プレビュー画像を表示
if image1 is not None:
    with col1_preview: st.image(image1, caption="タイヤの状態の写真")

with col2_upload: image2 = st.file_uploader("タイヤのメーカーがわかる写真", type=['jpg', 'jpeg'])
# プレビュー画像を表示
if image2 is not None:
    with col2_preview: st.image(image2, caption="タイヤのメーカーがわかる写真")

with col3_upload: image3 = st.file_uploader("タイヤのサイズがわかる写真", type=['jpg', 'jpeg'])
# プレビュー画像を表示
if image3 is not None:
    with col3_preview: st.image(image3, caption="タイヤのサイズがわかる写真")

# 診断開始ボタン
if st.button("診断開始"):
    st.write("診断中...")

# 画像を読み込んだら以下を実行する
if image1 is not None and image2 is not None and image3 is not None:
    image1_data = image1.read()
    image2_data = image2.read()
    image3_data = image3.read()

    # 画像データをBase64にエンコード
    encoded_image1 = base64.b64encode(image1_data).decode('utf-8')
    encoded_image2 = base64.b64encode(image2_data).decode('utf-8')
    encoded_image3 = base64.b64encode(image3_data).decode('utf-8')

    # プロンプトの設定
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "./prompt"))
    env = Environment(loader=FileSystemLoader(template_dir))

    diagnosis = env.get_template("./diagnosis.jinja2")

    # 2枚の画像とプロンプトをモデルに入力
    try:
        response = model.generate_content([
            {'mime_type': 'image/jpeg', 'data': encoded_image1},
            {'mime_type': 'image/jpeg', 'data': encoded_image2},
            {'mime_type': 'image/jpeg', 'data': encoded_image3},
            diagnosis.render()
        ])
        # 結果の出力
        st.write(response.text)
    except google.api_core.exceptions.InternalServerError:
        st.write("サービスが一時的に利用できません。しばらくしてから再度お試しください。")
    except Exception as e:
        st.write(f"エラーが発生しました: {e}")