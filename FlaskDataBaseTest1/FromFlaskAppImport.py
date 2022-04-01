from datetime import timedelta

from flask import Flask, session
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.secret_key = '334gab1hu1884er64gy'

bcrypt = Bcrypt(app)

