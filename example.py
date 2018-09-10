from flask import Flask

def base():
    return ('Hey')

def hi():
    return ('Hi there...')

def plus(num, pls):
    ans =  num + pls
    return (str(ans))

app = Flask(__name__)

app.add_url_rule('/', 'Home', (lambda: base()))
app.add_url_rule('/hi', 'Hi', (lambda: hi()))
app.add_url_rule('/plus/<int:num>/<int:pls>',
        'Add', (lambda num, pls: plus(num, pls)))

if __name__ == "__main__":
    app.run()
