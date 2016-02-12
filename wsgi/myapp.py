from flask import Flask, render_template

#
# Our WSGI application .. in this case Flask based
#
app = Flask(__name__)


@app.route('/')
def page_home():
    return render_template('index.html', message="Hello from Crossbar.io")
