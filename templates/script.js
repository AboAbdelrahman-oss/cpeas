document.getElementById('upload-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('pdf-file');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('pdf-file', file);

        // إرسال الملف إلى السيرفر أو النموذج لتحليله
        const response = await fetch('/upload-pdf', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        alert("File uploaded and processed!");
    }
});

document.getElementById('ask-btn').addEventListener('click', async function() {
    const question = document.getElementById('question').value;
    if (question) {
        const response = await fetch('/ask-question', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        const result = await response.json();
        document.getElementById('answer-text').innerText = result.answer;
    }
});

document.getElementById('download-excel').addEventListener('click', async function() {
    const response = await fetch('/download-excel');
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'output.xlsx';
    link.click();
});
