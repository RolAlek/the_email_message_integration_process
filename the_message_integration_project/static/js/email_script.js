const accountId = "{{ account_id }}"

const socket = new WebSocket('ws://localhost:8000/ws/emails/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.progress) {
        document.getElementById('progress-text').innerText = data.progress;
        document.getElementById('progress-bar').value = data.percentage;
    }

    if (data.new_email) {
        const table = document.getElementById('email-table').getElementsByTagName('tbody')[0];
        const row = table.insertRow();

        row.insertCell(0).innerText = data.new_email.message_id;
        row.insertCell(1).innerText = data.new_email.send_date;
        row.insertCell(2).innerText = data.new_email.subject;
        row.insertCell(3).innerText = data.new_email.text + '...';
    }
}