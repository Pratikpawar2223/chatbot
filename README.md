# 📄 AI Career Assistant (AWS Bedrock + LangChain + LangGraph)

An intelligent AI-powered Career Assistant built using **AWS Bedrock (Claude 3.5 Sonnet)**, **LangChain**, and **LangGraph**.

This chatbot can:
- 📄 Analyze resumes  
- 🧮 Solve calculations  
- 🗺️ Generate career roadmaps  
- 🧠 Remember user goals (Long-term JSON memory)  
- 💬 Maintain conversation session memory  

---

## 🚀 Features

### 🔧 Smart Tools Integrated
- **Calculator Tool** – Solve mathematical expressions  
- **Resume Analyzer Tool** – Score resumes & suggest improvements  
- **Career Roadmap Tool** – Generate structured learning paths  

### 🧠 Memory System
- **Session Memory** → Maintains chat context  
- **Long-Term Memory (JSON)** → Stores:
  - Target role  
  - Experience level  
  - Last interaction timestamp  

### 🤖 LLM Used
- AWS Bedrock – Claude 3.5 Sonnet  
- Temperature: 0.3  

---

## 🛠️ Tech Stack

- Python  
- LangChain  
- LangGraph  
- AWS Bedrock  
- Anthropic Claude 3.5 Sonnet  
- JSON (Persistent Memory)  

---

## 📂 Project Structure

ai-career-assistant/
│
├── main.py
├── user_profile.json
├── requirements.txt
└── README.md


---

## 🔐 AWS Configuration

Make sure AWS credentials are configured:

aws configure

Or set environment variables:

set AWS_ACCESS_KEY_ID=your_key  
set AWS_SECRET_ACCESS_KEY=your_secret  
set AWS_DEFAULT_REGION=us-east-1  

---

## ▶️ Run the Chatbot

python main.py

---

## 💬 Example Usage

You: I am a fresher and want to become a Data Scientist  
Bot: Here is your roadmap...  
🧠 Remembered: {'target_role': 'Data Scientist', 'experience': 'Fresher'}

You: 25*4+10  
Bot: 110

  
  
