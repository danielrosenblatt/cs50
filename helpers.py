import csv
import urllib.request
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from functools import wraps
from flask_session import Session
from tempfile import mkdtemp
import urllib3
import json

http = urllib3.PoolManager()

db = SQL("sqlite:///project.db")

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function