import os

class EnvironmentSetup:
    """
    This creates all the base files needed to run a flask app 
    as well as shows you how to connect to the database and a base app.py file
    """
    def create_project_structure(self, path:str):
        """path = the fully qualified path to the folder where the project will be located"""
        os.chdir(path)
        print('making template dir')
        os.makedirs("templates", exist_ok=True)
        with open("templates/base.html", "w") as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
            """)

        with open("app.py", "w") as f:
            f.write("""
from SLHPWebDev.database_connector import DatabaseConnector

# Initialize the SLHPWebDev
conn = DatabaseConnector(
    is_databricks=1,
    server_hostname="...",
    http_path="...",
    access_token="...",
    database_name="...",
    schema="...",
    secret_key="..."
)

# Or for SQL Server with integrated security
# conn = DatabaseConnector(
#     is_databricks=0,
#     server_hostname="...",
#     database_name="...",
#     use_integrated_security=True
# )

# Or for SQL Server with username and password
# conn = DatabaseConnector(
#     is_databricks=0,
#     server_hostname="...",
#     database_name="...",
#     sqlserver_username="...",
#     sqlserver_password="..."
# )

# Create the database models
from models.base_model import BaseModel
from models.dbfile import db
# Add your model definitions here

# Create the forms
from forms.base_form import BaseForm
# Add your form definitions here

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime

app = Flask(__name__)
                    
app.config['SQLALCHEMY_DATABASE_URI'] = conn.connection_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Reset the metadata for each run
db.metadata.clear()
# Initialize the database
db.init_app(app)

@app.before_request
def before_request():
    #Establish a database connection before each request.
    g.db_session = conn.get_session()  # Assuming you have a method to retrieve the session

@app.teardown_request
def teardown_request(exception):
    #Remove the database connection after the request is finished.
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.close()  # Close the session if it exists                    

@app.route('/', methods=['GET', 'POST'])
def index():
    # Fetch all reviewers from the database
    reviewers = BaseModel.query.all()
    form = BaseForm()

    if form.validate_on_submit():
        #Add submit logic
        db.session.add('insert class here')
        db.session.commit()
        flash('Reviewer added successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('base.html', reviewers=reviewers, form=form)
            """)
        print('making models dir')
        os.makedirs("models", exist_ok=True)
        with open("models/base_model.py", "w") as f:
            f.write("""from models.dbfile import db
from datetime import datetime
                
class Encounter(db.Model):
    __tablename__ = 'Encounter'

    EncounterID = db.Column(db.Integer, primary_key=True)
    ReviewerID = db.Column(db.Integer, db.ForeignKey('Reviewer.ReviewerId'), nullable=False)
    CreatedOn = db.Column(db.DateTime, default=datetime.utcnow)
    ModifiedOn = db.Column(db.DateTime, onupdate=datetime.utcnow)
    IsActive = db.Column(db.Boolean, default=True)

    # Relationship to Reviewer
    reviewer = db.relationship('Reviewer', backref='encounters')

    # Add additional fields as necessary
""")
        with open("models/dbfile.py","w") as f:
            f.write("""from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()""")
            

        print('making forms dir')
        os.makedirs("forms", exist_ok=True)
        with open("forms/base_form.py", "w") as f:
            f.write("""
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class ReviewerForm(FlaskForm):
    FirstName = StringField('First Name', validators=[DataRequired()])
    LastName = StringField('Last Name', validators=[DataRequired()])
    IsActive = BooleanField('Is Active')
    Submit = SubmitField('Save'))
""")