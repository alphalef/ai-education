from flask import Flask, request, jsonify, render_template
import llm
import datetime
import json
import os

app = Flask(__name__)

log_folder = './stored'

def create_log_file():
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d_%H-%M-%S') + '.json'

    # 빈 딕셔너리 생성
    # empty_dict = {}

    # 빈 JSON 파일 생성
    # with open(filename, 'w') as f:
    #     json.dump(empty_dict, f)

    return filename

def store_question_answer(question, answer, filename):
    # 저장할 데이터 생성
    now = datetime.datetime.now()
    data = {
        'time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'question': question,
        'answer': answer
    }

    # 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    filepath = os.path.join(log_folder, filename)

    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            loaded_data = json.load(f)
    else:
        loaded_data = []
    
    # 새로운 질문과 답변을 추가
    loaded_data.append(data)

    # JSON 파일로 저장
    with open(filepath, 'w') as f:
        json.dump(loaded_data, f, ensure_ascii=False, indent=4)

@app.route('/')
def home():
    filename = create_log_file()
    return render_template('index.html', value=filename) 

@app.route('/after')
def home():
    filename = create_log_file()
    return render_template('index2.html', value=filename)  

@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data['question']
    filename = 'post-' + data['logfile']

    # 답변 생성 코드
    answer = llm.gptanswer(question)  # generate_answer는 답변을 생성하는 함수
    # 로그작성
    store_question_answer(question, answer, filename)

    return jsonify({'answer': answer})

@app.route('/get_genanswer', methods=['POST'])
def get_genanswer():
    data = request.get_json()
    question = data['question1']
    filename = 'pre-' + data['logfile1']

    # 답변 생성 코드
    answer = llm.gptgeneral(question)  # generate_answer는 답변을 생성하는 함수

    # 로그작성
    store_question_answer(question, answer, filename) 

    return answer

@app.route('/input_opinion', methods=['POST'])
def input_opinion():
    data = request.get_json()
    opinion = data['opinion']
    filename = 'opinion-' + data['logfile2']

    # 로그작성
    store_question_answer('', opinion, filename)

    return '1'

@app.route('/create_img', methods=['POST'])
def create_img():
    data = request.get_json()
    question = data['question2']

    # 이미지 생성 코드
    img = llm.createimg(question)  # generate_answer는 답변을 생성하는 함수

    return img 