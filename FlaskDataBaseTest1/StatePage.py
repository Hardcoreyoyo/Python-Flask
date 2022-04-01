from FromFlaskAppImport import app
from flask import render_template, request, redirect, url_for


@app.route('/statepage')
def StatePage():
    return render_template('StatePage.html')
