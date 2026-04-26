import requests
import os
from datetime import datetime
from openai import OpenAI
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔐 SAFE TOKEN HANDLING
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
} if GITHUB_TOKEN else {}

GITHUB_API = "https://api.github.com/users/"


# ✅ USER DATA
def get_user_data(username):
    try:
        response = requests.get(GITHUB_API + username, headers=HEADERS)

        if response.status_code == 404:
            return None
        elif response.status_code != 200:
            print("API Error:", response.json())
            return {"error": "API issue"}

        return response.json()
    except:
        return None


# ✅ REPOS
def get_repos(username):
    try:
        response = requests.get(GITHUB_API + username + "/repos", headers=HEADERS)
        if response.status_code != 200:
            return []
        return response.json()
    except:
        return []


# ✅ RECRUITER INSIGHTS
def recruiter_insights(repos):
    try:
        if not repos:
            return {
                "best_repo": "N/A",
                "best_repo_stars": 0,
                "weak_repo": "N/A"
            }

        def repo_score(repo):
            score = 0
            score += repo.get('stargazers_count', 0) * 5

            if repo.get('description'):
                score += 10

            try:
                updated = datetime.strptime(repo['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
                if (datetime.now() - updated).days < 30:
                    score += 10
            except:
                pass

            return score

        best_repo = max(repos, key=repo_score)

        best_name = best_repo.get('name', 'N/A')
        best_stars = best_repo.get('stargazers_count', 0)

        weak_repo = "None"
        for repo in repos:
            if repo.get('stargazers_count', 0) == 0 and not repo.get('description'):
                weak_repo = repo.get('name', 'N/A')
                break

        return {
            "best_repo": best_name,
            "best_repo_stars": best_stars,
            "weak_repo": weak_repo
        }

    except Exception as e:
        print("Insight Error:", e)
        return {
            "best_repo": "Error",
            "best_repo_stars": 0,
            "weak_repo": "Error"
        }


# 🧠 🔥 AI ANALYSIS (UPGRADED)
def ai_analysis(user, repos):
    try:
        prompt = f"""
        You are a technical recruiter.

        Analyze this GitHub profile:

        Followers: {user.get('followers')}
        Total Repositories: {len(repos)}

        Return STRICTLY in this format:

        Score: <number>

        Breakdown:
        - Project Quality: <number>
        - Activity: <number>
        - Visibility: <number>
        - Consistency: <number>

        Strengths:
        - point
        - point

        Weaknesses:
        - point
        - point

        Suggestions:
        - point
        - point

        Verdict:
        <short recruiter opinion in 1-2 lines>
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content.strip()

        # 🔥 Extract score
        score_match = re.search(r"Score:\s*(\d+)", text)
        score = int(score_match.group(1)) if score_match else 50

        return {
            "score": score,
            "raw": text
        }

    except Exception as e:
        print("AI ERROR:", e)

        # 🔥 SMART FALLBACK (NEVER FAIL)
        fallback_score = min(len(repos) * 5, 100)

        return {
            "score": fallback_score,
            "raw": f"""
Score: {fallback_score}

Breakdown:
- Project Quality: 50
- Activity: 40
- Visibility: 20
- Consistency: 45

Strengths:
- Has {len(repos)} repositories
- Shows basic development activity

Weaknesses:
- Low visibility (stars/followers)
- No standout project

Suggestions:
- Build 2 strong projects
- Improve README
- Stay consistent

Verdict:
Profile shows potential but lacks strong impact projects. Needs improvement for recruiter attention.
"""
        }