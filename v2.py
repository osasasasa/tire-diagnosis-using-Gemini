import os
import google.generativeai as genai
import base64
import google.api_core.exceptions
import streamlit as st
from jinja2 import Environment, FileSystemLoader

genai.configure(api_key='API_KEY')
model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")
image1_path = "sample1.jpeg"
image2_path = "sample2.jpeg"
image3_path = "sample3.jpeg"


# 画像データの読み込み
with open(image1_path, "rb") as image_file:
    image1_data = image_file.read()
with open(image2_path, "rb") as image_file:
    image2_data = image_file.read()
with open(image3_path, "rb") as image_file:
    image3_data = image_file.read()

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
    print(response.text)
except google.api_core.exceptions.InternalServerError:
    print("サービスが一時的に利用できません。しばらくしてから再度お試しください。")
except Exception as e:
    print(f"エラーが発生しました: {e}")