import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from dotenv import load_dotenv

load_dotenv()  # loads .env in development; in production use Railway environment variables

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "change_this_secret_for_prod")



# Resume path (static)
RESUME_FILENAME = os.getenv("RESUME_FILENAME", "resume.pdf")


@app.route("/")
def home():
    return render_template("index.html", title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/projects")
def projects():
    # you can add more projects here
    projects_list = [
        {
            "id": "itams",
            "title": "IT Asset Management System (ITAMS)",
            "summary": "Tracks employee IT resources (CPU, IP, printers, monitors).",
            "image": url_for('static', filename='images/project_itams.png'),
            "tech": ["Flask", "MySQL", "Bootstrap", "JS"]
        },
        {
            "id": "pf",
            "title": "PF Management System – ITI Limited",
            "summary": "70+ modules for PF workflows: onboarding, loans, recoveries, settlements.",
            "image": url_for('static', filename='images/project_pf.png'),
            "tech": ["Flask", "MySQL", "Python"]
        }
    ]
    return render_template("projects.html", projects=projects_list, title="Projects")


@app.route("/projects/<project_id>")
def project_detail(project_id):
    # simple mapping, expand as you like
    if project_id == "itams":
        proj = {
            "title": "IT Asset Management System (ITAMS)",
            "desc": "Full-stack IT asset register: CRUD, duplicate-IP prevention, printer inventory, search & filters, update/delete UI.",
            "features": [
                "Add/Edit/Delete assets",
                "Duplicate IP detection",
                "Department-wise listing & search",
                "Printer inventory management",
                "Session-driven search results"
            ],
            "tech": ["Flask", "MySQL", "Bootstrap", "JS"],
            "screenshots": [
                url_for('static', filename='images/project_itams.png'),
            ]
        }
    elif project_id == "pf":
        proj = {
            "title": "PF Management System – ITI Limited",
            "desc": "Comprehensive PF automation with multi-step workflows and monthly processing.",
            "features": [
                "Staff onboarding & master management",
                "OB corrections & loan workflows",
                "Monthly totals & balances",
                "Session-based parameter controls"
            ],
            "tech": ["Flask", "MySQL", "Python"],
            "screenshots": [
                url_for('static', filename='images/project_pf.png'),
            ]
        }
    else:
        return redirect(url_for("projects"))

    return render_template("project_detail.html", project=proj, title=proj["title"])


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/resume")
def resume():
    # serve the resume file from static folder
    return send_from_directory("static", RESUME_FILENAME, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
