import os
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from models import db, Cliente, Libro
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = os.getenv('DEBUG')
app.config['ENV'] = os.getenv('ENV')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
jwt = JWTManager(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route("/")
def main():
    return render_template('index.html')

#======================CREAR USUARIO==============================================
@app.route("/api/crearusuario", methods=['POST', 'GET'])
def crearusuario():

    if request.method == 'POST':
        nombreCompleto = request.json.get('nombreCompleto')
        correo = request.json.get('correo')
        contrasenia = request.json.get('contrasenia')
        telefono = request.json.get('telefono')
        direccion = request.json.get('direccion')
        numero = request.json.get('numero')
        comuna = request.json.get('comuna')
        tipoVivienda = request.json.get('tipoVivienda')
        numDepto = request.json.get('numDepto')

        if not nombreCompleto: return jsonify({"msg": "Nombre Completo es requerido"}), 400
        if not correo: return jsonify({"msg": "correo es requerido"}), 400
        if not contrasenia: return jsonify({"msg": "contrasenia es requerida"}), 400
        if not telefono: return jsonify({"msg": "telefono es requerido"}), 400
        if not direccion: return jsonify({"msg": "direccion es requerido"}), 400
        if not numero: return jsonify({"msg": "numero es requerida"}), 400
        if not comuna: return jsonify({"msg": "comuna Completo es requerido"}), 400
        if not tipoVivienda: return jsonify({"msg": "tipoVivienda es requerido"}), 400
        if not numDepto: return jsonify({"msg": "numDepto es requerido"}), 400
        

        usuario = Cliente.query.filter_by(correo=correo).first()
        if usuario: return jsonify({"error": "ERROR", "msg": "Usuario ya existe!!!"}), 400
        
        usuario = Cliente()
        usuario.nombreCompleto = nombreCompleto
        usuario.correo = correo
        usuario.contrasenia = generate_password_hash(contrasenia)
        usuario.telefono = telefono
        usuario.direccion = direccion
        usuario.numero = numero
        usuario.comuna = comuna
        usuario.tipoVivienda = tipoVivienda
        usuario.numDepto = numDepto
        usuario.estado = "activo"
        usuario.f_creacion = datetime.date.today()
        usuario.f_modificacion= None
        usuario.f_eliminacion = None
        usuario.save()

        if not usuario: return jsonify({"msg": "Registro Fallido!!!"}), 400

        #expires = datetime.timedelta(days=1)
        #access_token = create_access_token(identity=user.id, expires_delta=expires)

        data = {
            "msg": "Usuario creado y activo",
            "usuario": usuario.serialize(),
        }

        return jsonify(data), 201

    if request.method == 'GET':
        usuarios = Cliente.query.all()
        if not usuarios: return jsonify({"msg": "No se encontraron registros"}), 404
        usuarios = list(map(lambda usuarios: usuarios.serialize(), usuarios))
        
        return jsonify(usuarios), 200

#======================LOGIN==========================================================
@app.route("/api/login", methods=['POST'])
def login():

    correo = request.json.get('correo')
    contrasenia = request.json.get('contrasenia')

    if not correo: return jsonify({"msg": "correo es requerido"}), 400
    if not contrasenia: return jsonify({"msg": "contraseña es requerido"}), 400

    user = Cliente.query.filter_by(correo=correo).first()
    if not user: return jsonify({"msg": "correo/contraseña es incorrecto!!!"}), 400

    if not check_password_hash(user.contrasenia, contrasenia):
        return jsonify({"msg": "correo/contraseña es incorrecto!!!"}), 400
    
    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity=user.id, expires_delta=expires)

    data = {
        "estado": "Usuario Validado y Correcto",
        "tokenLogin": access_token,
    }

    return jsonify(data), 200

#======================Perfil de Usuario Segun Token==============================================
@app.route("/api/perfil", methods=['GET'])
@jwt_required()
def perfil():
    id = get_jwt_identity()
    user = Cliente.query.get(id)
    return jsonify(user.serialize()), 200

#======================CREAR LIBRO==============================================
@app.route("/api/crearlibro", methods=['POST', 'GET'])
def crearlibro():

    if request.method == 'POST':
        cliente_id = request.json.get('cliente_id')
        titulo = request.json.get('titulo').lower()
        nombreAutor = request.json.get('nombreAutor')
        editorial = request.json.get('editorial')
        nivel = request.json.get('nivel')
        asignatura = request.json.get('asignatura')
        estadoNuevoUsado = request.json.get('estadoNuevoUsado')
        condicionOriginalCopia = request.json.get('condicionOriginalCopia')
        tipoIntercambio = request.json.get('tipoIntercambio')
        precio = request.json.get('precio')
        comentarios = request.json.get('comentarios')


        if not cliente_id: return jsonify({"msg": "cliente_id es requerido"}), 400
        if not titulo: return jsonify({"msg": "titulo es requerido"}), 400
        if not nombreAutor: return jsonify({"msg": "nombreAutor es requerido"}), 400
        if not editorial: return jsonify({"msg": "editorial es requerida"}), 400
        if not nivel: return jsonify({"msg": "nivel es requerido"}), 400
        if not asignatura: return jsonify({"msg": "asignatura es requerido"}), 400
        if not estadoNuevoUsado: return jsonify({"msg": "estadoNuevoUsado es requerida"}), 400
        if not condicionOriginalCopia: return jsonify({"msg": "condicionOriginalCopia Completo es requerido"}), 400
        if not tipoIntercambio: return jsonify({"msg": "tipoIntercambio es requerido"}), 400
        if not precio: return jsonify({"msg": "precio es requerido"}), 400
        if not comentarios: return jsonify({"msg": "comentarios es requerido"}), 400

        user = Cliente.query.filter_by(id=cliente_id).first()
        if not user: return jsonify({"msg": "Usuario no existe"}), 400
    
        #libro = Libro.query.filter_by(id=id and cliente_id == cliente_id).first()
        #if libro: return jsonify({"error": "ERROR", "msg": "Libro ya existe!!!"}), 400
    
        libro = Libro()
        libro.cliente_id = cliente_id
        libro.titulo = titulo
        libro.nombreAutor = nombreAutor
        libro.editorial = editorial
        libro.nivel = nivel
        libro.asignatura = asignatura
        libro.estadoNuevoUsado = estadoNuevoUsado
        libro.condicionOriginalCopia = condicionOriginalCopia
        libro.tipoIntercambio = tipoIntercambio
        libro.precio = precio
        libro.comentarios = comentarios
        libro.estado = "activo"
        libro.f_creacion = datetime.date.today()
        libro.f_modificacion= None
        libro.f_eliminacion = None
        libro.save()

        if not libro: return jsonify({"msg": "Registro Fallido!!!"}), 400

        data = {
            "msg": "Libro creado y activo",
            "usuario": libro.serialize(),
        }

        return jsonify(data), 201
    
    if request.method == 'GET':
        libros = Libro.query.all()
        if not libros: return jsonify({"msg": "No se encontraron registros"}), 404
        libros = list(map(lambda libros: libros.serialize(), libros))
        
        return jsonify(libros), 200

#======================GET, PUT, DELETE para UN USUARIO==============================================

@app.route("/api/crearusuario/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def crearusuarioid(id = None):

    if request.method == 'GET':
        if id is not None:
            usuario = Cliente.query.get(id)
            if not usuario or usuario.estado == "borrado": return jsonify({"msg": "Registro no encontrado"}), 404
            return jsonify(usuario.serialize()), 200
        else:
            usuario = Cliente.query.all()
            usuario = list(map(lambda usuario: usuario.serialize(), usuario))
            return jsonify(usuario), 200
        
    if request.method == 'PUT':
        nombreCompleto = request.json.get('nombreCompleto')
        correo = request.json.get('correo')
        contrasenia = request.json.get('contrasenia')
        telefono = request.json.get('telefono')
        direccion = request.json.get('direccion')
        numero = request.json.get('numero')
        comuna = request.json.get('comuna')
        tipoVivienda = request.json.get('tipoVivienda')
        numDepto = request.json.get('numDepto')

        if not nombreCompleto: return jsonify({"msg": "Nombre Completo es requerido"}), 400
        if not correo: return jsonify({"msg": "correo es requerido"}), 400
        if not contrasenia: return jsonify({"msg": "contrasenia es requerida"}), 400
        if not telefono: return jsonify({"msg": "telefono es requerido"}), 400
        if not direccion: return jsonify({"msg": "direccion es requerido"}), 400
        if not numero: return jsonify({"msg": "numero es requerida"}), 400
        if not comuna: return jsonify({"msg": "comuna Completo es requerido"}), 400
        if not tipoVivienda: return jsonify({"msg": "tipoVivienda es requerido"}), 400
        if not numDepto: return jsonify({"msg": "numDepto es requerido"}), 400
        
        usuario = Cliente.query.get(id)
        if not usuario: return jsonify({"msg": "Registro no encontrado"}), 404

        usuario.nombreCompleto = nombreCompleto
        usuario.correo = correo
        usuario.contrasenia = generate_password_hash(contrasenia)
        usuario.telefono = telefono
        usuario.direccion = direccion
        usuario.numero = numero
        usuario.comuna = comuna
        usuario.tipoVivienda = tipoVivienda
        usuario.numDepto = numDepto
        usuario.f_modificacion= datetime.date.today()

        usuario.update()

        return jsonify(usuario.serialize()), 200

    if request.method == 'DELETE':
        usuario = Cliente.query.get(id)
        if not usuario or usuario.estado == "borrado": return jsonify({"msg": "Usuario no encontrado"}), 404

        usuario.estado = "borrado"
        usuario.f_eliminacion = datetime.date.today()
        usuario.update()

        return jsonify({"msg": "Registro Borrado"}), 200

#======================GET, PUT, DELETE para UN LIBRO==============================================

@app.route("/api/crearlibro/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def crearlibroid(id = None):

    if request.method == 'GET':
        if id is not None:
            libro = Libro.query.get(id)
            if not libro or libro.estado == "borrado": return jsonify({"msg": "Registro no encontrado"}), 404
            return jsonify(libro.serialize()), 200
        else:
            libro = Libro.query.all()
            libro = list(map(lambda libro: libro.serialize(), libro))
            return jsonify(libro), 200
        
    if request.method == 'PUT':
        titulo = request.json.get('titulo').lower()
        nombreAutor = request.json.get('nombreAutor')
        editorial = request.json.get('editorial')
        nivel = request.json.get('nivel')
        asignatura = request.json.get('asignatura')
        estadoNuevoUsado = request.json.get('estadoNuevoUsado')
        condicionOriginalCopia = request.json.get('condicionOriginalCopia')
        tipoIntercambio = request.json.get('tipoIntercambio')
        precio = request.json.get('precio')
        comentarios = request.json.get('comentarios')
        
        if not titulo: return jsonify({"msg": "titulo es requerido"}), 400
        if not nombreAutor: return jsonify({"msg": "nombreAutor es requerido"}), 400
        if not editorial: return jsonify({"msg": "editorial es requerida"}), 400
        if not nivel: return jsonify({"msg": "nivel es requerido"}), 400
        if not asignatura: return jsonify({"msg": "asignatura es requerido"}), 400
        if not estadoNuevoUsado: return jsonify({"msg": "estadoNuevoUsado es requerida"}), 400
        if not condicionOriginalCopia: return jsonify({"msg": "condicionOriginalCopia Completo es requerido"}), 400
        if not tipoIntercambio: return jsonify({"msg": "tipoIntercambio es requerido"}), 400
        if not precio: return jsonify({"msg": "precio es requerido"}), 400
        if not comentarios: return jsonify({"msg": "comentarios es requerido"}), 400


        libro = Libro.query.get(id)
        if not libro or libro.estado == "borrado": return jsonify({"msg": "Registro no encontrado"}), 404

        libro.titulo = titulo
        libro.nombreAutor = nombreAutor
        libro.editorial = editorial
        libro.nivel = nivel
        libro.asignatura = asignatura
        libro.estadoNuevoUsado = estadoNuevoUsado
        libro.condicionOriginalCopia = condicionOriginalCopia
        libro.tipoIntercambio = tipoIntercambio
        libro.precio = precio
        libro.comentarios = comentarios
        libro.estado = "activo"
        libro.f_modificacion= datetime.date.today()
        libro.update()

        return jsonify(libro.serialize()), 200

    if request.method == 'DELETE':
        libro = Libro.query.get(id)
        if not libro or libro.estado == "borrado": return jsonify({"msg": "libro no encontrado"}), 404

        libro.estado = "borrado"
        libro.f_eliminacion = datetime.date.today()
        libro.update()

        return jsonify({"msg": "Registro Borrado"}), 200

#======================GET - Todos los Libros de un USUARIO==============================================

@app.route("/api/usuario/<int:cliente_id>/libro", methods=['GET'])
@app.route("/api/usuario/<int:cliente_id>/libro/<int:id>", methods=['GET'])
def libroxusuario(cliente_id, id=None):

    if request.method == 'GET':
        if id is not None:
            libroxcliente = Libro.query.filter_by(cliente_id=cliente_id, id = id).first()
            if not libroxcliente: return jsonify({"msg":"Cliente sin Libros"}),404
            return jsonify(libroxcliente.serialize()),200
        else:
            libroxcliente = Libro.query.filter_by(cliente_id = cliente_id).all()
            if not libroxcliente: return jsonify({"msg":"Cliente sin Libros"}),404
            libroxcliente = list(map(lambda libroxcliente: libroxcliente.serialize(), libroxcliente))
            return jsonify(libroxcliente),200

if __name__ == '__main__':
    manager.run()