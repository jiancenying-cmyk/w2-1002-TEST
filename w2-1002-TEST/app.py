from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    topic = ""
    feedback = ""
    student_answer = ""
    question_text = "請先選擇學習主題"
    
    if request.method == "POST":
        topic = request.form.get("topic", "")
        action = request.form.get("action", "")
        print("我選擇的主題:", topic)
        
        # 根據學習主題設定對應題目
        if topic == "輸入輸出":
            question_text = "Python 使用哪個函數顯示文字？"
        elif topic == "條件判斷":
            question_text = "Python 中用來判斷條件的分支語法是什麼？"
        elif topic == "迴圈":
            question_text = "Python 中用來執行固定次數迴圈的指令是什麼？"
        elif topic == "串列":
            question_text = "Python 用來建立串列 (List) 的符號是什麼？"
        elif topic == "":
            question_text = "請選擇學習主題"
        else:
            question_text = "尚未放置題目"
            
        # 檢查學生的作答結果 (支援所有主題)
        if action == "check":
            student_answer = request.form.get("student_answer", "")
            
            if topic == "輸入輸出" and student_answer == "B":
                feedback = "答對了！"
            elif topic == "條件判斷" and student_answer == "A":
                feedback = "答對了！"
            elif topic == "迴圈" and student_answer == "A":
                feedback = "答對了！"
            elif topic == "串列" and student_answer == "A":
                feedback = "答對了！"
            else:
                feedback = "答錯了！"
                
    return render_template("index_1002.html",
                           topic=topic,
                           question_text=question_text,
                           feedback=feedback
                           )

if __name__ == "__main__":
    app.run(debug=True, port=5001)