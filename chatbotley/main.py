from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)
openai.api_key = "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"



@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='GET':
        return render_template('index.html')

def get_gpt_response(message):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=2040
        
    )
    return response.choices[0].text.strip()

@app.route('/chatbot_ronald_Jefferson', methods=['POST'])
def chatbot_response():
    message = request.form['message']
    response = get_gpt_response(message)
    return jsonify(response)  # Envía la respuesta como JSON

if __name__ == "__main__":
    app.run(debug=True, port=2003)

