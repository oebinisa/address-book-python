# Mini Address Book App - Fullstack App
Python(Flask) + HTML/CSS + MySQL

## Overview

This is a simple address book application. 

 - **Frontend:** HTML with Bootstrap
 - **Backend:** Flask
 - **Database:** MySQL
 - **ORM:** SQLAlchemy
 - **Envvironemnt Variables/Sensitive Data:** dotenv


## Project Structure

Here’s the folder structure for the app:

```
address-book-python/
│
├── app/
│   ├── __init__.py             # Flask app and configuration setup
│   ├── config.py               # Configuration file (DB details, hidden using .env)
│   ├── models.py               # Database schema
│   ├── routes.py               # Routes for input and display pages
│   ├── templates/              # HTML templates for the app
│   │   ├── base.html           # Base template with navigation bar
│   │   ├── form.html           # Input form template
│   │   └── display.html        # Display template for submitted data
│   ├── static/                 # Static files (e.g., CSS)
│   │   └── style.css           # Custom styles for the app
│
├── venv/                       # Virtual environment folder
├── .env                        # Environment variables (e.g., DB password)
├── requirements.txt            # Dependencies for the project
├── run.py                      # Main entry point to run the Flask app
└── schema.sql                  # SQL script for creating the database and tables

```

## Part 1: Detailed Steps:

### Step 1: Setting Up the Virtual Environment
1. **Create the project directory**:
   ```bash
   mkdir address-book-python
   cd address-book-python
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install Flask Flask-SQLAlchemy python-dotenv
   pip install pymysql
   ```

4. **Freeze the dependencies**:
   ```bash
   pip freeze > requirements.txt
   ```

### Step 2: Database Schema Script (`schema.sql`)
Create a `schema.sql` file to define the schema:

```sql
CREATE DATABASE IF NOT EXISTS address_book;
USE address_book;
DROP TABLE contacts;

CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    address VARCHAR(255)
);
```

### Step 3: Application Configuration (`app/config.py` and `.env`)
1. **Create a `.env` file** in the root directory to store sensitive information:

   ```ini
   MYSQL_USER=root
   MYSQL_PASSWORD=Pa55word
   MYSQL_DB=address_book
   MYSQL_HOST=localhost
   ```

2. **Create the configuration file** `app/config.py` to read these values:

   ```python
   import os
   from dotenv import load_dotenv

   # Load environment variables
   load_dotenv()

   class Config:
       SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
       SQLALCHEMY_TRACK_MODIFICATIONS = False
   ```

### Step 4: Flask Application Initialization (`app/__init__.py`)
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Initialize database instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Import and register routes
    from .routes import main
    app.register_blueprint(main)

    return app
```

### Step 5: Define the Database Model (`app/models.py`)
```python
from . import db

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)
```

### Step 6: Define Routes for Input and Display Pages (`app/routes.py`)
```python
from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Contact

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('form.html')

@main.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')

    new_contact = Contact(name=name, email=email, phone=phone, address=address)
    db.session.add(new_contact)
    db.session.commit()

    return redirect(url_for('main.view_contacts'))

@main.route('/contacts')
def view_contacts():
    contacts = Contact.query.all()
    return render_template('display.html', contacts=contacts)
```

### Step 7: Create HTML Templates

1. **Base Template (`app/templates/base.html`)**:

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Address Book</title>
       <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
   </head>
   <body>
       <nav>
           <a href="{{ url_for('main.index') }}">Add Contact</a>
           <a href="{{ url_for('main.view_contacts') }}">View Contacts</a>
       </nav>
       <div class="content">
           {% block content %}{% endblock %}
       </div>
   </body>
   </html>
   ```

2. **Input Form Template (`app/templates/form.html`)**:

   ```html
   {% extends "base.html" %}
   {% block content %}
   <h1>Add New Contact</h1>
   <form action="{{ url_for('main.submit') }}" method="POST">
       <input type="text" name="name" placeholder="Name" required>
       <input type="email" name="email" placeholder="Email" required>
       <input type="tel" name="phone" placeholder="Phone" required>
       <textarea name="address" placeholder="Address" required></textarea>
       <button type="submit">Add Contact</button>
   </form>
   {% endblock %}
   ```

3. **Display Page Template (`app/templates/display.html`)**:

   ```html
   {% extends "base.html" %}
   {% block content %}
   <h1>Contacts</h1>
   <ul>
       {% for contact in contacts %}
       <li>{{ contact.name }} - {{ contact.email }} - {{ contact.phone }} - {{ contact.address }}</li>
       {% endfor %}
   </ul>
   {% endblock %}
   ```

### Step 8: Add Custom CSS (`app/static/style.css`)
```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

nav {
    background-color: #333;
    padding: 1em;
}

nav a {
    color: white;
    margin: 0 1em;
    text-decoration: none;
}

.content {
    padding: 2em;
}
```

### Step 9: Create the Main Run Script (`run.py`)
```python
from app import create_app, db
from app.models import Contact

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)
```

### Step 10: Initialize the Database and Run the App
1. **Create the database**:
   ```bash
   mysql -u root -p < schema.sql
   ```

2. **Run the Flask App**:
   ```bash
   python run.py
   ```

Your Address Book app should now be accessible at `http://127.0.0.1:5000`, with a navigation bar to add and view contacts!







## Part 2: CI with GitHub Actions with Compressed/Zipped Artifacts**

#### **Objective**
Set up a Continuous Integration (CI) pipeline using GitHub Actions for the `address-book-python` application. The pipeline will:
1. Run automated tests to verify code quality.
2. Generate a compressed/zipped build artifact containing the app.
3. Upload the artifact to an S3 bucket with a timestamped filename.
4. Send email notifications for CI results using MailGun.

---

### **Prerequisites**
- **Basic Knowledge**: Familiarity with GitHub Actions, Python, Flask, SQLAlchemy, MySQL, and dotenv.
- **Tools**:
  - AWS CLI (configured for access to S3 bucket `s3://simartefacts/`).
  - MailGun account for email notifications.
  - Python development environment (local or virtual).

---

### **Step-by-Step Instructions**

#### **Step 1: Clone the Project Repository**
1. Clone the repository locally:
   ```bash
   git clone https://github.com/oebinisa/address-book-python.git
   cd address-book-python
   ```

2. Verify the folder structure:
   - Backend: Python Flask app.
   - Frontend: HTML and Bootstrap files.
   - Database: MySQL integration with SQLAlchemy ORM.
   - Sensitive Data: `.env` for environment variables.

---

#### **Step 2: Configure GitHub Repository for CI**
1. Create a `.github/workflows/ci.yml` file:
   ```bash
   mkdir -p .github/workflows && touch .github/workflows/ci.yml
   ```

2. Add the following YAML content for GitHub Actions:

   ```yaml
   name: CI Pipeline

   on:
     push:
       branches:
         - main
     pull_request:
       branches:
         - main

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
         # Step 1: Checkout code
         - name: Checkout code
           uses: actions/checkout@v3

         # Step 2: Set up Python environment
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: 3.9

         - name: Install dependencies
           run: |
             python -m venv venv
             source venv/bin/activate
             pip install -r requirements.txt

         # Step 3: Run tests
         - name: Run tests
           run: |
             source venv/bin/activate
             pytest

         # Step 4: Package the app as a zip file
         - name: Create artifact
           run: |
             timestamp=$(date +'%Y%m%d%H%M%S')
             zip -r address-book-python-$timestamp.zip .
           env:
             TIMESTAMP: ${{ github.run_id }}

         # Step 5: Upload to S3
         - name: Upload to S3
           env:
             AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
             AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
             AWS_DEFAULT_REGION: us-east-1
           run: |
             aws s3 cp address-book-python-$TIMESTAMP.zip s3://simartefacts/

         # Step 6: Send email notification
         - name: Send email notification
           run: |
             curl -s --user "api:${{ secrets.MAILGUN_API_KEY }}" \
             https://api.mailgun.net/v3/YOUR_DOMAIN/messages \
             -F from="CI Pipeline <mailgun@YOUR_DOMAIN>" \
             -F to="recipient@example.com" \
             -F subject="CI Pipeline Status: Success" \
             -F text="The build artifact has been successfully created and uploaded to S3."
   ```

---

#### **Step 3: Set Up Secrets in GitHub**
1. Navigate to your GitHub repository → Settings → Secrets → Actions.
2. Add the following secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS Access Key ID.
   - `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key.
   - `MAILGUN_API_KEY`: API key for MailGun.
   - `MAILGUN_DOMAIN`: Your MailGun domain.

---

#### **Step 4: Verify the Pipeline**
1. Push changes to the `main` branch:
   ```bash
   git add .
   git commit -m "Add GitHub Actions CI pipeline"
   git push origin main
   ```

2. Check the **Actions** tab in the GitHub repository for pipeline execution progress.

---

#### **Step 5: Test the Artifacts**
1. Log in to your AWS S3 account.
2. Navigate to the `simartefacts` bucket.
3. Verify the uploaded artifact:
   - The file should be named as `address-book-python-<timestamp>.zip`.

---

#### **Step 6: Check Email Notifications**
1. Verify that the email notification is sent to the configured recipient.
2. Troubleshoot with MailGun logs if emails are not delivered.

---

### **CLI Equivalents for Console Steps**

#### Uploading Artifacts to S3
```bash
aws s3 cp address-book-python-$(date +'%Y%m%d%H%M%S').zip s3://simartefacts/
```

#### Sending Email with MailGun
```bash
curl -s --user "api:<MAILGUN_API_KEY>" \
https://api.mailgun.net/v3/<MAILGUN_DOMAIN>/messages \
-F from="CI Pipeline <mailgun@<MAILGUN_DOMAIN>>" \
-F to="recipient@example.com" \
-F subject="CI Pipeline Status: Success" \
-F text="The build artifact has been successfully created and uploaded to S3."
```

---

### **Assignment Guidelines**
1. Complete the pipeline setup as described.
2. Ensure the pipeline runs successfully on a push or pull request to the `main` branch.
3. Upload proof of your pipeline execution:
   - Screenshot of the Actions tab.
   - Screenshot of the uploaded artifact in S3.

Reach out for guidance via WhatsApp or email if you encounter any issues.