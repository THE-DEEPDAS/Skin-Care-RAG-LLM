from src.api.app import app
from src.config.config import API_PORT

if __name__ == "__main__":
    print(f"Starting Skincare Clinic Chatbot on port {API_PORT}...")
    app.run(port=API_PORT)
