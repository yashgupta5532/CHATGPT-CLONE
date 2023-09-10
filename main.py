from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import openai

openai.api_key = "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"
app=Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/ChatGpt"
mongo = PyMongo(app)


@app.route('/')
def home():
    chats = mongo.db.chat.find({})
    myChats = [chat for chat in chats]
    print(myChats)
    return render_template('index.html', myChats=myChats)


@app.route("/api", methods=["GET", "POST"])
def qa():
    
    if request.method == "POST":
        print(request.form, request.json)
        question = request.json.get("question")
        chat = mongo.db.chat.find_one({"question": question})
        print(chat)
        if chat:
            data = {"question":question, "answer": f"{chat['answer']}"}
            return jsonify(data)
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": question,
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print(response)
            data = {"question": question, "answer": response["choices"][0]["text"]}
            mongo.db.chat.insert_one(
                {"question": question, "answer": response["choices"][0]["text"]})
            return jsonify(data)
   

if __name__ == "__main__":
    app.run(debug=True, port=5001)
