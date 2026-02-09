import os
import json
from datetime import datetime

from langchain_aws import ChatBedrock
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver





# ==================================================
# 🔧 TOOLS
# ==================================================

@tool
def calculator(expression: str) -> str:
    """Solve mathematical expressions"""
    try:
        return str(eval(expression))
    except Exception:
        return "❌ Invalid calculation"

@tool
def resume_analyzer(resume_text: str) -> str:
    """Analyze resume and return score + tips"""
    skills = ["python", "sql", "machine learning", "project", "data"]
    score = sum(10 for s in skills if s in resume_text.lower())

    tips = []
    if score < 30:
        tips.append("Add 2–3 real-world projects")
    if "intern" not in resume_text.lower():
        tips.append("Mention internship or practical experience")

    return f"📄 Resume Score: {score}/50\nTips: {', '.join(tips)}"

@tool
def career_roadmap(role: str) -> str:
    """Generate career roadmap for a role"""
    roadmaps = {
        "data scientist": "Python → SQL → ML → Projects → Internships → Kaggle",
        "data analyst": "Excel → SQL → Python → Power BI → Projects",
        "software developer": "DSA → Python/Java → Projects → GitHub → Interviews"
    }
    return roadmaps.get(role.lower(), "Role not found")

tools = [calculator, resume_analyzer, career_roadmap]

# ==================================================
# 💾 LONG-TERM MEMORY (JSON)
# ==================================================

MEMORY_FILE = "user_profile.json"

def load_profile():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_profile(profile):
    with open(MEMORY_FILE, "w") as f:
        json.dump(profile, f, indent=2)

user_profile = load_profile()

# ==================================================
# 🤖 AWS BEDROCK LLM (CLAUDE 3.5)
# ==================================================

llm = ChatBedrock(
    model_id="arn:aws:bedrock:us-east-1:629927974043:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    provider="anthropic",
    region="us-east-1",
    temperature=0.3
)


# ==================================================
# 🧠 PROMPT
# ==================================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an advanced AI Career Assistant. "
        "You analyze resumes, generate career roadmaps, "
        "use tools when required and remember user goals."
    ),
    ("human", "{input}")
])

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

def tool_router(message):
    return message

chain = prompt | llm | StrOutputParser()


# ==================================================
# 🔁 SESSION MEMORY
# ==================================================

sessions = {}

def get_session_history(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = ChatMessageHistory()
    return sessions[session_id]

chatbot = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input"
)

# ==================================================
# 🧪 SMART MEMORY UPDATE
# ==================================================

def update_user_profile(text: str):
    text = text.lower()

    if "data scientist" in text:
        user_profile["target_role"] = "Data Scientist"
    if "data analyst" in text:
        user_profile["target_role"] = "Data Analyst"
    if "fresher" in text:
        user_profile["experience"] = "Fresher"

    user_profile["last_updated"] = str(datetime.now())
    save_profile(user_profile)

# ==================================================
# 🚀 CHAT LOOP

print("🤖 AWS Bedrock Career Chatbot Ready")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("👋 Goodbye!")
        break

    update_user_profile(user_input)

    response = chatbot.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "user_01"}}
    )

    print("Bot:", response)


    if user_profile:
        print("🧠 Remembered:", user_profile, "\n") 