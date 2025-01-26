from flask import Flask, request, jsonify
from src.llm.chat_model import ChatModel
from src.config.config import API_PORT

app = Flask(__name__)
chat_model = ChatModel()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    response = chat_model.get_response(query)
    return jsonify(response)

@app.route("/book-appointment", methods=["POST"])
def book_appointment():
    data = request.json
    required_fields = ["name", "date", "time", "contact"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    # In a real application, you would save this to a database
    appointment = {
        "name": data["name"],
        "date": data["date"],
        "time": data["time"],
        "contact": data["contact"]
    }
    
    return jsonify({"message": "Appointment booked successfully", "appointment": appointment})

if __name__ == "__main__":
    app.run(port=API_PORT, debug=True)
