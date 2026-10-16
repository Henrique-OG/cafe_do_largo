from flask import render_template, request, redirect, session, url_for
from public import public_bp

@public_bp.route('/')
def apresentacao():
    return render_template('index.html')
