from flask import Flask, render_template, request
from groq import Groq
from pineconewrapper import PineconeWrapper
import os
import __main__
print("Running from:", __main__.__file__)

app = Flask(__name__)

pinecone = PineconeWrapper()

client = Groq(api_key="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")

messages = [] 

print("Current working dir:", os.getcwd())

def generate_response(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

@app.route("/")
def chathome():

    return render_template("index.html", messages=messages)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("userInput", "").strip()

    if not user_input:
        return "Please enter a message."

    try:
        bot_response = pinecone.executePrompt(user_input)
        messages.append({"user": user_input, "bot": bot_response})

    except Exception as e:
        app.logger.warning(e)
        if 'INVALID_ARGUMENT' in str(e):
            bot_response = "Sorry, the required content is not accessible or does not exist in our database."

        else:
            bot_response = "Sorry, something went wrong. Please try again later."
    return bot_response

if __name__ == "__main__":
    app.run(debug=True)
