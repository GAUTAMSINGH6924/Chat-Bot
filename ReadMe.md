# 🤖 AI Chatbot

An intelligent AI-powered chatbot built using Python that can interact with users in real-time and generate meaningful responses using modern AI APIs.

---

## 🚀 Overview

This project demonstrates how to build a simple yet powerful AI chatbot by integrating external AI APIs. It is designed to be modular, scalable, and easy to understand for beginners and developers exploring AI applications.

---

## ✨ Features

- 💬 Real-time conversation with AI
- 🔐 Secure API key management using `.env`
- 🧠 Context-based responses
- ⚡ Lightweight and fast execution
- 📦 Clean project structure

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Libraries:** Requests / OpenAI / dotenv (based on your implementation)  
- **Environment Management:** Virtual Environment (venv)  

---

## 📁 Project Structure

Chatbot/
│── app.py # Main application logic
│── requirements.txt # Dependencies
│── .env # API keys (ignored)
│── .gitignore # Ignored files
│── venv/ # Virtual environment (ignored)


## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/GAUTAMSINGH6924/Chat-Bot.git

cd Chat-Bot

2️⃣ Create Virtual Environment
python -m venv venv

3️⃣ Activate Virtual Environment
venv\Scripts\activate   # On Windows

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Setup Environment Variables
Create a .env file in the root directory:

API_KEY=your_api_key_here

▶️ Running the Application
python app.py