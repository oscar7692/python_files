from flask import Flask, jsonify, request
from prueba import administrador
app = Flask('inicio')


@app.route('/')
def inicio():
    admin = administrador()
    data = admin.mostrar_usuarios()  #  [ {'nombre': 'a'}, {'nombre': 'b'}]
    # resp = jsonify(data)
    # print(admin.mostrar_usuarios())
    resp = jsonify(data)
    # resp.status_code = 200
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp
    # return "Hola"


@app.route('/agrega_usuario', methods=['POST'])
def agregar_usuario():
    nombre = request.form['name']
    apellido1 = request.form['apellido1']
    apellido2 = request.form['apellido2']
    correo = request.form['correo']
    password = request.form['password']
    tipo = request.form['tipo']
    admin = administrador()
    admin.insert_usuario([nombre, apellido1, apellido2, correo, password, tipo])
    print(nombre)
    res = jsonify({'status': 'OK', 'user': nombre})
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.route('/buscar', methods=['POST'])
def buscar_usuario():
    valor = request.form['palabra']
    print(valor)
    admin = administrador()
    data = admin.buscar_usuarios(valor)
    data = jsonify(data)
    data.headers.add('Access-Control-Allow-Origin', '*')
    return data
app.run(debug=True)
