from flask import Flask, jsonify, render_template_string
from analyzer import (
    get_user_data,
    get_repos,
    recruiter_insights,
    ai_analysis
)

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>GitInsight AI</title>

    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: #f6f7fb;
            color: #333;
            text-align: center;
        }

        h1 {
            margin-top: 30px;
            font-weight: 700;
            font-size: 50px;
        }

        input {
            padding: 12px;
            width: 260px;
            border-radius: 8px;
            border: 1px solid #ddd;
        }

        button {
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 550;
            margin-left: 10px;
            border: none;
            background: linear-gradient(to right, #4f46e5, #06b6d4);
            color: white;
            border-radius: 20px;
            cursor: pointer;
        }

        .card {
            background: white;
            padding: 25px;
            margin: 20px auto;
            width: 65%;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            text-align: left;
            animation: fadeIn 0.5s ease;
        }

        .score {
            font-size: 26px;
            font-weight: bold;
            color: #4f46e5;
            margin-top: 10px;
        }

        .verdict {
            background: #eef2ff;
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
            font-style: italic;
            border-left: 4px solid #4f46e5;
        }

        ul {
            padding-left: 20px;
        }

        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(10px);}
            to {opacity: 1; transform: translateY(0);}
        }
    </style>
</head>

<body>

<h1>🚀 GitInsight AI</h1>

<input type="text" id="username" placeholder="Enter GitHub username">
<button onclick="analyze()">Analyze</button>

<div id="output"></div>

<script>
function analyze() {
    let username = document.getElementById("username").value;

    document.getElementById("output").innerHTML =
        "<div class='card'>⏳ Analyzing profile...</div>";

    fetch("/analyze/" + username)
    .then(res => res.json())
    .then(data => {

        let html = "";

        if(data.error){
            html = "<div class='card'>" + data.error + "</div>";
        } else {

            // PROFILE SUMMARY (WITH SCORE)
            html += "<div class='card'>";
            html += "<h2>Profile Summary</h2>";
            html += "<p><b>Username:</b> " + data.username + "</p>";
            html += "<p><b>Followers:</b> " + data.followers + "</p>";
            html += "<p><b>Repositories:</b> " + data.public_repos + "</p>";
            html += "<p class='score'>AI Score: " + data.score + "/100</p>";
            html += "</div>";

            // RECRUITER INSIGHTS
            html += "<div class='card'>";
            html += "<h2>Recruiter Insights</h2>";
            html += "<p>⭐ Best Project: " + data.insights.best_repo + "</p>";
            html += "<p>🔥 Stars: " + data.insights.best_repo_stars + "</p>";
            html += "<p>❌ Weak Project: " + data.insights.weak_repo + "</p>";
            html += "</div>";

            // AI ANALYSIS (CLEAN FORMAT)
            html += "<div class='card'>";
            html += "<h2>🧠 AI Analysis</h2>";

            let lines = data.ai_text.split("\\n");
            let inList = false;

            lines.forEach(line => {
                line = line.trim();

                // ❌ REMOVE unwanted sections
                if(
                    line.startsWith("Score") ||
                    line.startsWith("Breakdown") ||
                    line.includes("Project Quality") ||
                    line.includes("Activity") ||
                    line.includes("Visibility") ||
                    line.includes("Consistency")
                ){
                    return;
                }

                if(line.startsWith("Strengths")){
                    html += "<h3>✅ Strengths</h3><ul>";
                    inList = true;
                }
                else if(line.startsWith("Weaknesses")){
                    html += "</ul><h3>⚠️ Weaknesses</h3><ul>";
                }
                else if(line.startsWith("Suggestions")){
                    html += "</ul><h3>🚀 Suggestions</h3><ul>";
                }
                else if(line.startsWith("Verdict")){
                    html += "</ul><h3>🧑‍💼 Recruiter Verdict</h3>";
                    inList = false;
                }
                else if(line.startsWith("-")){
                    html += "<li>" + line.substring(1) + "</li>";
                }
                else if(line.length > 0){
                    html += "<div class='verdict'>" + line + "</div>";
                }
            });

            html += "</div>";
        }

        document.getElementById("output").innerHTML = html;
    });
}
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)


@app.route('/analyze/<username>')
def analyze(username):
    try:
        user = get_user_data(username)

        if not user:
            return jsonify({"error": "User not found"}), 404

        repos = get_repos(username)

        ai_data = ai_analysis(user, repos)
        insights = recruiter_insights(repos)

        return jsonify({
            "username": username,
            "followers": user.get("followers", 0),
            "public_repos": user.get("public_repos", 0),
            "score": ai_data["score"],
            "insights": insights,
            "ai_text": ai_data["raw"]
        })

    except Exception as e:
        print("SERVER ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True)