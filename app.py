import os
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from models import db, Cliente, Direccion, VentaPermuta, Libro, Autor, LibroAutor
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

@app.route("/api/registrar", methods=['POST'])
def registrar():
    correo = request.json.get('correo')
    contrasenia = request.json.get('contrasenia')
    nombreCompleto = request.json.get('nombreCompleto')
    telefono = request.json.get('telefono')


    if not correo: return jsonify({"msg": "correo es requerido"}), 400
    if not contrasenia: return jsonify({"msg": "contrasenia es requerida"}), 400
    if not nombreCompleto: return jsonify({"msg": "Nombre Completo es requerido"}), 400
    if not telefono: return jsonify({"msg": "telefono es requerido"}), 400
    

    user = Cliente.query.filter_by(correo=correo).first()
    if user: return jsonify({"error": "ERROR", "msg": "correo ya existe!!!"}), 400
    
    user = Cliente()
    user.nombreCompleto = nombreCompleto
    user.correo = correo
    user.contrasenia = generate_password_hash(contrasenia)
    user.telefono = telefono
    user.estado = "activo"
    user.f_creacion = datetime.date.today()
    user.f_modificacion= None
    user.f_eliminacion = None
    user.save()

    if not user: return jsonify({"msg": "Registro Fallido!!!"}), 400

    expires = datetime.timedelta(days=3)

    access_token = create_access_token(identity=user.id, expires_delta=expires)

    data = {
        "usuario": user.serialize(),
        "access_token": access_token,
    }

    return jsonify(data), 201

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
    
    expires = datetime.timedelta(days=3)

    access_token = create_access_token(identity=user.id, expires_delta=expires)

    data = {
        "usuario": user.serialize(),
        "tokenLogin": access_token,
    }

    return jsonify(data), 200

@app.route("/api/perfil", methods=['GET'])
@jwt_required()
def perfil():
    id = get_jwt_identity()
    user = Cliente.query.get(id)
    return jsonify(user.serialize()), 200

@app.route("/api/direccion", methods=['POST'])
def direccion():
    cliente_id = request.json.get('cliente_id')
    direccion = request.json.get('direccion')
    numero = request.json.get('numero')
    comuna = request.json.get('comuna')
    tipoVivienda = request.json.get('tipoVivienda')
    numDepto = request.json.get('numDepto')
    estado = request.json.get('estado')
    f_creacion = request.json.get('f_creacion')
    f_modificacion = request.json.get('f_modificacion')
    f_eliminacion = request.json.get('f_eliminacion')

    if not cliente_id: return jsonify({"msg": "cliente_id es requerido"}), 400
    if not direccion: return jsonify({"msg": "direccion es requerida"}), 400
    if not numero: return jsonify({"msg": "numero es requerido"}), 400
    if not comuna: return jsonify({"msg": "comuna es requerido"}), 400
    if not tipoVivienda: return jsonify({"msg": "tipoVivienda es requerido"}), 400
    if not numDepto: return jsonify({"msg": "numDepto es requerido"}), 400
    if not estado: return jsonify({"msg": "estado es requerido"}), 400

    user = Direccion.query.filter_by(cliente_id=id).first()
    if user: return jsonify({"msg": "Direccion ya existe!!!"}), 400
    
    user = Direccion()
    user.cliente_id = cliente_id
    user.direccion = direccion
    user.numero = numero
    user.comuna = comuna
    user.tipoVivienda = tipoVivienda
    user.numDepto = numDepto
    user.estado = estado
    user.f_creacion = datetime.date.today()
    user.f_modificacion= None
    user.f_eliminacion = None
    user.save()

    if not user: return jsonify({"msg": "Registro Fallido!!!"}), 400

    expires = datetime.timedelta(days=3)

    access_token = create_access_token(identity=user.id, expires_delta=expires)

    data = {
        "usuario": user.serialize(),
        "tokenDireccion": access_token,
    }

    return jsonify(data), 201


if __name__ == '__main__':
    app.run()