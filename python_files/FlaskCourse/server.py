#!/user/bin/python3

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')#wrap o decorador indica que dir puede acceder el usuario
def index():
    return 'sup'

@app.route('/params')#http://127.0.0.1:8000/params?params1=oscar_pulido  ejemplo de pasar datos por url
def params():
    params = request.args.get('params1', 'no contine nada')
    return 'El parametro es : {}'.format(params)

if __name__ == '__main__':
    app.run(debug=True, port=8000)