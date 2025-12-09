import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from dotenv import load_dotenv

load_dotenv()  # loads .env in development; in production use Railway environment variables

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "change_this_secret_for_prod")

# Email configuration (use environment variables)
EMAIL_HOST = os.getenv("EMAIL_HOST")           # e.g., smtp.gmail.com
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587)) # 587 for TLS, 465 for SSL
EMAIL_USER = os.getenv("EMAIL_USER")           # sender email
EMAIL_PASS = os.getenv("EMAIL_PASS")           # app password or SMTP password
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "false").lower() == "true"

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


@app.route("/blogs")
def blogs():
    # Placeholder blog list - replace with dynamic source or DB later
    posts = [
        {"slug": "how-i-built-itams", "title": "How I built ITAMS", "summary": "Design decisions & stack"},
        {"slug": "pf-automation-case-study", "title": "PF Automation Case Study", "summary": "Workflows and problems solved"}
    ]
    return render_template("blogs.html", posts=posts, title="Blogs")


@app.route("/blogs/<slug>")
def blog_post(slug):
    # static example posts
    if slug == "how-i-built-itams":
        post = {
            "title": "How I built ITAMS",
            "body": "<p>Explain architecture, Blueprints, DB schema, validations and UI choices.</p>"
        }
    elif slug == "pf-automation-case-study":
        post = {
            "title": "PF Automation Case Study",
            "body": "<p>Explain PF workflows, example calculations, and testing approach.</p>"
        }
    else:
        return redirect(url_for("blogs"))
    return render_template("blog_post.html", post=post, title=post["title"])


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "Portfolio Contact").strip()
        message = request.form.get("message", "").strip()

        # Basic validation
        if not name or not email or not message:
            flash("Please fill in name, email and message.", "danger")
            return redirect(url_for("contact"))

        # Construct email
        body = f"New contact form submission\n\nName: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
        try:
            send_email(subject=f"[Portfolio] {subject}", body=body, to_email=EMAIL_USER)
            flash("Message sent successfully. I will get back to you soon.", "success")
            return redirect(url_for("contact"))
        except Exception as e:
            print("Email send error:", e)
            flash("Could not send message right now. Please try again later.", "danger")
            return redirect(url_for("contact"))

    return render_template("contact.html", title="Contact")


def send_email(subject: str, body: str, to_email: str):
    """
    Sends an email using SMTP. Uses EMAIL_USE_SSL to choose SSL or STARTTLS.
    Make sure environment variables EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS are set.
    """
    if not EMAIL_HOST or not EMAIL_USER or not EMAIL_PASS:
        raise RuntimeError("Email server not configured. Set EMAIL_HOST, EMAIL_USER and EMAIL_PASS env vars.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content(body)

    if EMAIL_USE_SSL:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)


@app.route("/resume")
def resume():
    # serve the resume file from static folder
    return send_from_directory("static", RESUME_FILENAME, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
