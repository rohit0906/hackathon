from flask import Flask, render_template, request
from script import assistant_gui


app = Flask(__name__)


@app.route("/")
def load_home():
    name = "Ratnesh"
    return render_template('home.html', name=name)


@app.route("/func", methods={'GET', 'POST'})
def process():
    name = request.form.get('input')
    '''name=assistant_gui.record_audio()
    assistant_gui.respond(name)'''
    assistant_gui.respond(name)
    return render_template('home.html', name=name)

if __name__ == "__main__":
    app.run(debug=False)
