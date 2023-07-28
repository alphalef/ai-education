from flask import Flask, request, jsonify, render_template
import llm

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # templates 폴더에서 index.html 파일을 찾습니다.

@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data['question']
    # 답변 생성 코드
    answer = llm.gptanswer(question)  # generate_answer는 답변을 생성하는 함수
    return jsonify({'answer': answer})
