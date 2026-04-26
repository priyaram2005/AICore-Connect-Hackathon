# 🚀 GitInsight AI – Intelligent GitHub Profile Analyzer

## 📌 Problem Statement
Recruiters often rely on GitHub profiles to evaluate candidates, but:
- Manual evaluation is time-consuming
- Important signals like project quality and consistency are hard to assess
- Students lack guidance on improving their profiles

---

## 💡 Solution
**GitInsight AI** is an AI-powered web application that analyzes GitHub profiles and provides:

- 📊 AI-generated profile score
- 🧠 Recruiter-style analysis
- 🎯 Strengths & weaknesses
- 🚀 Actionable suggestions for improvement

---

## ⚙️ Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **API:** GitHub REST API  
- **AI Engine:** OpenAI GPT (LLM)

---

## 🔥 Key Features
- ✅ AI-based GitHub profile scoring  
- ✅ Recruiter-style insights (best & weak projects)  
- ✅ Structured AI feedback (strengths, weaknesses, suggestions)  
- ✅ Clean and minimal UI for easy understanding  
- ✅ Real-time analysis using GitHub API  

---

## 🧠 How It Works
1. User enters a GitHub username  
2. Backend fetches profile and repository data  
3. AI model analyzes:
   - Repository count
   - Activity & consistency
   - Visibility (stars, engagement)  
4. System generates:
   - AI score  
   - Structured insights  
   - Recruiter-style verdict  

---

## 🔑 API Configuration

This project requires API keys to function properly.

### 1️⃣ OpenAI API Key (Required for AI Analysis)

Set your OpenAI API key:

#### Windows
set OPENAI_API_KEY=your_openai_api_key_here


## 🚀 How to Run Locally

1. Clone the repository
git clone https://github.com/yourusername/your-repo-name.git cd your-repo-name

2. Install dependencies
pip install -r requirements.txt

3. Run the Flask application
python app.py

4. Open in Browser
http://127.0.0.1:5000/
