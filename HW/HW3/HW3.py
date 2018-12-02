from flask import Flask
from flask import render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/write')
def write():
    args = []

    args.append(request.args.get("strogino", ''))
    args.append(request.args.get("mitino", ''))
    args.append(request.args.get("schukino", ''))
    args.append(request.args.get("marino", ''))
    args.append(request.args.get("orehovo", ''))

    with open('data.csv',  'a+', encoding='utf-8') as f:
        f.write('\t'.join(args) + '\r')

    return redirect('/')
