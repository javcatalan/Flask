from flask import Flask
from flask import request

app = Flask(__name__)#nuevo decoradador

#http://localhost:8000/params?params1=ejamplo&params2=test
#http://localhost:8000/params

@app.route('/')#wrap o un decorador
def index():
    return 'hola'#regresa un string

@app.route('/params')
def params():
    param =request.args.get('params1','no contiene este parametro')
    params_dos=request.args.get('params2','no contiene este parametro')
    return 'El parametro es : {}, {}'.format(param, params_dos)

if __name__=='__main__':
    app.run(debug=True,port=8000)#se encarga de ejecutar en el servidor 500
