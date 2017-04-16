from flask import Flask, render_template

#
# Our WSGI application .. in this case Flask based
#
app = Flask(__name__)

app.config.seq = 0

@app.route('/')
def page_home():
    app.config.seq += 1
    return render_template('index.html',
                           message="Hello from Crossbar.io",
                           seq=app.config.seq)
