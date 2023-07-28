function submitQuestion() {
    let question = document.getElementById('question').value;

    // 스피너 표시 및 제출 버튼 숨기기
    document.getElementById('spinner').style.display = 'inline-block';
    document.getElementById('submitBtn').style.display = 'none';

    fetch('/get_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'question': question })
    }).then(response => response.json())
    .then(data => {
        // 응답 받으면 스피너 숨기기 및 제출 버튼 표시
        document.getElementById('spinner').style.display = 'none';
        document.getElementById('submitBtn').style.display = 'inline-block';

        document.getElementById('answer').textContent = data.answer;
    });
}