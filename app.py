from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "edubuddy_secret_key"
RESOURCE_FILE = 'resources.json'

# Load existing resources
def load_resources():
    if not os.path.exists(RESOURCE_FILE):
        return []
    with open(RESOURCE_FILE, 'r') as f:
        return json.load(f)

# Save new resource
def save_resource(resource):
    data = load_resources()
    data.append(resource)
    with open(RESOURCE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resources')
def view_resources():
    data = load_resources()
    semester = request.args.get('semester')
    subject = request.args.get('subject')
    if semester:
        data = [r for r in data if r['semester'].strip() == semester.strip()]
    if subject:
        data = [r for r in data if r['subject'].strip().lower() == subject.strip().lower()]
    return render_template('resources.html', resources=data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        link = request.form['link'].strip()
        semester = request.form['semester'].strip()
        subject = request.form['subject'].strip()

        if not (title and description and link and semester and subject):
            flash("Please fill in all fields.", "error")
            return redirect(url_for('upload'))

        resource = {
            'title': title,
            'description': description,
            'link': link,
            'semester': semester,
            'subject': subject
        }
        save_resource(resource)
        flash("Resource uploaded successfully!", "success")
        return redirect(url_for('view_resources'))

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False, threaded=True)
