import os
import json
from dotenv import load_dotenv
from google import genai
from flask import Flask, render_template, request, session

# 1. 讀取同資料夾下的 .env 檔案
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# 2. 建立 Gemini 用戶端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
app.secret_key = os.urandom(32)  # 用來保護 session 資料

# 3. 建立 Gemini AI 出題函式
def generate_question(topic):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=(
            f"請根據「{topic}」產生一道 Python 初學者的四選一選擇題。"
            "只能有一個正確答案。"
            "請回傳 JSON 格式，包含 question、A、B、C、D、answer、explanation 七個欄位。"
            "answer 只能填入 A、B、C 或 D。"
            "explanation 請用繁體中文解釋正確答案，50字以內。"
        ),
        config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)

@app.route("/", methods=["POST", "GET"])
def home():
    topic = ""
    feedback = ""
    student_answer = ""
    question_text = "請先選擇學習主題"
    question_data = {}

    if request.method == "POST":
        topic = request.form.get("topic", "")
        action = request.form.get("action", "")
        print("我選擇的主題:", topic)

        # 動作一：按下「幫我出題」
        if action == "generate":
            if not topic:
                question_text = "請先選擇學習主題"
            else:
                # 呼叫 Gemini AI 產生題目並存入 session
                question_data = generate_question(topic)
                session["question_data"] = question_data
                session["topic"] = topic
                question_text = question_data["question"]

        # 動作二：按下「提交答案」
        elif action == "check":
            # 從 session 取得先前 AI 出的題目與答案
            question_data = session.get("question_data", {})
            student_answer = request.form.get("student_answer", "")

            if not question_data:
                feedback = "目前尚未產生題目，請先點擊幫我出題。"
            else:
                question_text = question_data["question"]
                if student_answer == "":
                    feedback = "請先選擇答案。"
                elif student_answer == question_data["answer"]:
                    feedback = "答對了！" + question_data["explanation"]
                else:
                    feedback = (
                        "答錯了！正確答案是 "
                        + question_data["answer"]
                        + "："
                        + question_data["explanation"]
                    )

    # 確保重新整理或剛進網頁時也能抓到 session 裡的資料
    if not question_data and "question_data" in session:
        question_data = session["question_data"]
        topic = session.get("topic", "")
        if question_data:
            question_text = question_data.get("question", question_text)

    return render_template("index_1002.html",  # 如果你的前端檔案名稱是 index_1002.html 也可以改成對應名稱
                           topic=topic,
                           question_text=question_text,
                           feedback=feedback,
                           question_data=question_data
                           )

if __name__ == "__main__":
    app.run(debug=True, port=5001)