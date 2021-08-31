from flask import Flask, render_template
from data import Articles

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/', methods=['GET', 'POST'])
def index():
    name = "JUNG"
    return render_template('index.html', data=name)

@app.route('/articles', methods=['GET','POST'])
def articles():
    list_data = Articles()
    return render_template('articles.html', data = list_data)
    
@app.route('/detail/<ids>')
def detail(ids):
    list_data = Articles()
    for data in list_data:
        if data['id'] == int(ids):
            article = data
    return render_template('article.html', article1=article)


if __name__ == '__main__':
    app.run(debug=True)