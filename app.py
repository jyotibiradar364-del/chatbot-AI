import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client for HuggingFace
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN"),
)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        completion = client.chat.completions.create(
            model="Qwen/Qwen3-Coder-Next:novita",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
        )

        bot_response = completion.choices[0].message.content
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
