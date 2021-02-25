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
        

        usuarios = Cliente.query.filter_by(correo=correo).first()
        if usuarios: return jsonify({"error": "ERROR", "msg": "correo ya existe!!!"}), 400
        
        usuarios = Cliente()
        usuarios.nombreCompleto = nombreCompleto
        usuarios.correo = correo
        usuarios.contrasenia = generate_password_hash(contrasenia)
        usuarios.telefono = telefono
        usuarios.direccion = direccion
        usuarios.numero = numero
        usuarios.comuna = comuna
        usuarios.tipoVivienda = tipoVivienda
        usuarios.numDepto = numDepto
        usuarios.estado = "activo"
        usuarios.f_creacion = datetime.date.today()
        usuarios.f_modificacion= None
        usuarios.f_eliminacion = None
        usuarios.save()

        if not usuarios: return jsonify({"msg": "Registro Fallido!!!"}), 400

        #expires = datetime.timedelta(days=1)
        #access_token = create_access_token(identity=user.id, expires_delta=expires)

        data = {
            "msj": "Usuario creado y activo",
            "usuario": usuarios.serialize(),
        }

        return jsonify(data), 201

    if request.method == 'GET':
        usuarios = Cliente.query.all()
        if not usuarios: return jsonify({"msg": "No se encontraron registros"}), 404
        usuarios = list(map(lambda usuarios: usuarios.serialize(), usuarios))
        
        return jsonify(usuarios), 200

#======================LOGIN==============================================
@app.route("/api/login", methods=['POST'])
def login():

    correo = request.json.get('correo')
    contrasenia = request.json.get('contrasenia')

    if not correo: return jsonify({"msg": "correo es requerido"}), 400
    if not contrasenia: return jsonify({"msg": "contrasenia es requerido"}), 400

    user = Cliente.query.filter_by(correo=correo).first()
    if not user: return jsonify({"msg": "correo/contrasenia es incorrecto!!!"}), 400

    if not check_password_hash(user.contrasenia, contrasenia):
        return jsonify({"msg": "correo/contrasenia es incorrecto!!!"}), 400
    
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
@app.route("/api/crearlibro", methods=['POST'])
def crearlibro():
    
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
    

    user = Cliente.query.filter_by(correo=correo).first()
    if user: return jsonify({"error": "ERROR", "msg": "correo ya existe!!!"}), 400
    
    user = Cliente()
    user.nombreCompleto = nombreCompleto
    user.correo = correo
    user.contrasenia = generate_password_hash(contrasenia)
    user.telefono = telefono
    user.direccion = direccion
    user.numero = numero
    user.comuna = comuna
    user.tipoVivienda = tipoVivienda
    user.numDepto = numDepto
    user.estado = "activo"
    user.f_creacion = datetime.date.today()
    user.f_modificacion= None
    user.f_eliminacion = None
    user.save()

    if not user: return jsonify({"msg": "Registro Fallido!!!"}), 400

    #expires = datetime.timedelta(days=1)
    #access_token = create_access_token(identity=user.id, expires_delta=expires)

    data = {
        "msj": "Usuario creado y activo",
        "usuario": user.serialize(),
    }

    return jsonify(data), 201


if __name__ == '__main__':
    app.run()