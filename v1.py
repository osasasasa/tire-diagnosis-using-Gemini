import google.generativeai as genai
import base64
import google.api_core.exceptions

genai.configure(api_key='API_KEY')
model = genai.GenerativeModel(model_name = "gemini-1.5-flash-002")
image_path = "sample1.jpeg"

# 画像データの読み込み
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# 画像データをBase64にエンコード
encoded_image = base64.b64encode(image_data).decode('utf-8')

# プロンプトの設定
prompt = "タイヤの状態を調べて欲しい"

# 画像とプロンプトをモデルに入力
try:
    response = model.generate_content([
        {'mime_type': 'image/jpeg', 'data': encoded_image},
        prompt
    ])
    # 結果の出力
    print(response.text)
except google.api_core.exceptions.InternalServerError:
    print("サービスが一時的に利用できません。しばらくしてから再度お試しください。")
except Exception as e:
    print(f"エラーが発生しました: {e}")