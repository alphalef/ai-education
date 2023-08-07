function submitQuestion() {
    let question = document.getElementById('question').value;
    let logfile = document.getElementById('logfile').value;

    // 스피너 표시 및 제출 버튼 숨기기
    document.getElementById('spinner').style.display = 'inline-block';
    document.getElementById('submitBtn').style.display = 'none';

    fetch('/get_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'question': question, 'logfile': logfile })
    }).then(response => response.json())
    .then(data => {
        // 응답 받으면 스피너 숨기기 및 제출 버튼 표시
        document.getElementById('spinner').style.display = 'none';
        document.getElementById('submitBtn').style.display = 'inline-block';
        document.getElementById('answer').textContent = data.answer;
    });
}

function submitQuestion1() {
    let question = document.getElementById('question1').value;

    // 스피너 표시 및 제출 버튼 숨기기
    document.getElementById('spinner1').style.display = 'inline-block';
    document.getElementById('submitBtn1').style.display = 'none';

    fetch('/get_genanswer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'question1': question })
    }).then(response => response.text())
    .then(data => {
        // 응답 받으면 스피너 숨기기 및 제출 버튼 표시
        document.getElementById('spinner1').style.display = 'none';
        document.getElementById('submitBtn1').style.display = 'inline-block';
        document.getElementById('answer1').textContent = data;
    });
}


function submitQuestion2() {
    let question = document.getElementById('question2').value;

    // 스피너 표시 및 제출 버튼 숨기기
    document.getElementById('spinner2').style.display = 'inline-block';
    document.getElementById('submitBtn2').style.display = 'none';

    fetch('/create_img', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'question2': question })
    }).then(response => response.text())
    .then(data => {
        // 응답 받으면 스피너 숨기기 및 제출 버튼 표시
        document.getElementById('spinner2').style.display = 'none';
        document.getElementById('submitBtn2').style.display = 'inline-block';
        document.getElementById('answer2').innerHTML = '<img src="data:img/png;base64,'+data+'" style="max-width:200px; height:auto;"></img>';
        // console.log(data);
    });
}