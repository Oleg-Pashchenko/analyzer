from flask import Flask, request, render_template
from db import get_messages_history

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index_handler():
    message_history = None
    if request.method == 'POST':
        lead_id = request.form.get('lead_id')
        if lead_id:
            message_history = get_messages_history(int(lead_id))
    return render_template('index.html', message_history=message_history)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
