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

@app.route("/api/registroUsuario", methods=['POST'])
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

    if not cliente_id: return jsonify({"msg": "cliente_id es requerido"}), 400
    if not direccion: return jsonify({"msg": "direccion es requerida"}), 400
    if not numero: return jsonify({"msg": "numero es requerido"}), 400
    if not comuna: return jsonify({"msg": "comuna es requerido"}), 400
    if not tipoVivienda: return jsonify({"msg": "tipoVivienda es requerido"}), 400
    if not numDepto: return jsonify({"msg": "numDepto es requerido"}), 400
    if not estado: return jsonify({"msg": "estado es requerido"}), 400

    direccion = Direccion.query.filter_by(cliente_id=id).first()
    if direccion: return jsonify({"msg": "Direccion ya existe!!!"}), 400
    
    direccion = Direccion()
    direccion.cliente_id = cliente_id
    direccion.direccion = direccion
    direccion.numero = numero
    direccion.comuna = comuna
    direccion.tipoVivienda = tipoVivienda
    direccion.numDepto = numDepto
    direccion.estado = "activo"
    direccion.f_creacion = datetime.date.today()
    direccion.f_modificacion= None
    direccion.f_eliminacion = None
    direccion.save()

    if not direccion: return jsonify({"msg": "Registro Fallido!!!"}), 400

    expires = datetime.timedelta(days=3)

    access_token = create_access_token(identity=direccion.id, expires_delta=expires)

    data = {
        "usuario": direccion.serialize(),
        "tokenDireccion": access_token,
    }

    return jsonify(data), 201


@app.route("/api/autor", methods=['POST'])
def autor():
    nombre = request.json.get('nombreAutor')
    pais = request.json.get('pais')
    
    if not nombre: return jsonify({"msg": "nombreAutor es requerido"}), 400
    if not pais: return jsonify({"msg": "pais es requerida"}), 400

    autor = Autor.query.filter_by(nombre=nombre).first()
    if autor: return jsonify({"msg": "Autor ya existe!!!"}), 400
    
    autor = Autor()
    autor.nombre = nombre
    autor.pais = pais
    autor.estado = "activo"
    autor.f_creacion = datetime.date.today()
    autor.save()

    if not autor: return jsonify({"msg": "Registro Fallido!!!"}), 400

    expires = datetime.timedelta(days=3)

    access_token = create_access_token(identity=autor.id, expires_delta=expires)

    data = {
        "usuario": autor.serialize(),
        "tokenAutor": access_token,
    }

    return jsonify(data), 201


@app.route("/api/libro", methods=['POST'])
def libro():
    titulo = request.json.get('titulo')
    aditorial = request.json.get('aditorial')
    nivel = request.json.get('nivel')
    asignatura = request.json.get('asignatura')
    estadoNuevoUsado = request.json.get('estadoNuevoUsado')
    condicionOriginalCopia = request.json.get('condicionOriginalCopia')
    comentarios = request.json.get('comentarios')
    
    if not titulo: return jsonify({"msg": "titulo es requerido"}), 400
    if not aditorial: return jsonify({"msg": "aditorial es requerida"}), 400
    if not nivel: return jsonify({"msg": "nivel es requerida"}), 400
    if not asignatura: return jsonify({"msg": "asignatura es requerida"}), 400
    if not estadoNuevoUsado: return jsonify({"msg": "estadoNuevoUsado es requerida"}), 400
    if not condicionOriginalCopia: return jsonify({"msg": "condicionOriginalCopia es requerida"}), 400
    if not comentarios: return jsonify({"msg": "comentarios es requerida"}), 400

    libro = Libro.query.filter_by(titulo=titulo).first()
    if libro: return jsonify({"msg": "titulo ya existe!!!"}), 400
    
    libro = Libro()
    libro.titulo = titulo
    libro.aditorial = aditorial
    libro.nivel = nivel
    libro.asignatura = asignatura
    libro.estadoNuevoUsado = estadoNuevoUsado
    libro.condicionOriginalCopia = condicionOriginalCopia
    libro.comentarios = comentarios
    libro.estado = "activo"
    libro.f_creacion = datetime.date.today()
    libro.save()

    if not libro: return jsonify({"msg": "Registro Fallido!!!"}), 400

    expires = datetime.timedelta(days=3)

    access_token = create_access_token(identity=libro.id, expires_delta=expires)

    data = {
        "libro": libro.serialize(),
        "tokenLibro": access_token,
    }

    return jsonify(data), 201


@app.route("/api/libroAutor", methods=['POST'])
def libroAutor():
    autor_id = request.json.get('autor_id')
    libro_id = request.json.get('libro_id')
    
    if not autor_id: return jsonify({"msg": "autor_id es requerido"}), 400
    if not libro_id: return jsonify({"msg": "aditorial es requerida"}), 400

    libroautor = LibroAutor.query.filter_by(autor_id = autor_id).first()
    if libroautor: return jsonify({"msg": "Relacion entre libro y Autor ya existe!!!"}), 400
    
    libroautor = LibroAutor()
    libroautor.autor_id = autor_id
    libroautor.libro_id = libro_id
    libroautor.save()

    if not libroautor: return jsonify({"msg": "Registro Fallido!!!"}), 400

    expires = datetime.timedelta(days=3)

    access_token = create_access_token(identity=libroautor.id, expires_delta=expires)

    data = {
        "libro": libroautor.serialize(),
        "tokenLibroAutor": access_token,
    }

    return jsonify(data), 201


@app.route("/api/venta_permuta", methods=['POST'])
def venta_permuta():
    cliente_id = request.json.get('idRut')
    direccion_id = request.json.get('idDireccion')
    libro_id = request.json.get('idLibro')
    tipoIntercambio = request.json.get('tipoIntercambio')
    precio = request.json.get('precio')
    
    if not cliente_id: return jsonify({"msg": "idRut es requerido"}), 400
    if not direccion_id: return jsonify({"msg": "idDireccion es requerida"}), 400
    if not libro_id: return jsonify({"msg": "idLibro es requerido"}), 400
    if not tipoIntercambio: return jsonify({"msg": "tipoIntercambio es requerida"}), 400
    if not precio: return jsonify({"msg": "precio es requerido"}), 400

    ventapermuta = VentaPermuta.query.filter_by(id = id).first()
    if ventapermuta: return jsonify({"msg": "Relacion entre libro y Autor ya existe!!!"}), 400
    
    ventapermuta = VentaPermuta()
    ventapermuta.cliente_id = cliente_id
    ventapermuta.direccion_id = direccion_id
    ventapermuta.libro_id = libro_id
    ventapermuta.tipoIntercambio = tipoIntercambio
    ventapermuta.estado = "activo"
    ventapermuta.f_creacion = datetime.date.today()
    ventapermuta.save()

    if not ventapermuta: return jsonify({"msg": "Registro Fallido!!!"}), 400

    expires = datetime.timedelta(days=3)

    access_token = create_access_token(identity=ventapermuta.id, expires_delta=expires)

    data = {
        "libro": ventapermuta.serialize(),
        "tokenVentaPermuta": access_token,
    }

    return jsonify(data), 201

@app.route('/api/usuario/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def usuario(id = None):

    if request.method == 'GET':
        if id is not None:
            cliente = Cliente.query.get(id)
            if not cliente or cliente.estado == "borrado": return jsonify({"msg": "Registro no encontrado"}), 404
            return jsonify(cliente.serialize()), 200
        else:
            cliente = Cliente.query.all()
            cliente = list(map(lambda cliente: cliente.serialize(), cliente))
            return jsonify(cliente), 200
        
    if request.method == 'PUT':
        correo = request.json.get('correo')
        contrasenia = request.json.get('contrasenia')
        nombreCompleto = request.json.get('nombreCompleto')
        telefono = request.json.get('telefono')

        if not correo: return jsonify({"msg": "correo es requerido"}), 400
        if not contrasenia: return jsonify({"msg": "contrasenia es requerido"}), 400
        if not nombreCompleto: return jsonify({"msg": "nombreCompleto es requerido"}), 400
        if not telefono: return jsonify({"msg": "telefono es requerido"}), 400

        cliente = Cliente.query.get(id)
        if not cliente: return jsonify({"msg": "Registro no encontrado"}), 404

        cliente.correo = correo
        cliente.contrasenia = generate_password_hash(contrasenia)
        cliente.nombreCompleto = nombreCompleto
        cliente.telefono = telefono
        cliente.f_modificacion = datetime.date.today()

        cliente.update()

        return jsonify(cliente.serialize()), 201

    if request.method == 'DELETE':
        cliente = Cliente.query.get(id)
        if not cliente or cliente.estado == "borrado": return jsonify({"msg": "Usuario no Encontrado"}), 404
        cliente.estado = "borrado"
        cliente.f_eliminacion = datetime.date.today()
        cliente.update()
        return jsonify({"msg": "Registro Borrado"}), 200

@app.route('/api/direccion/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def direccionid(id = None):

    if request.method == 'GET':
        if id is not None:
            direc = Direccion.query.get(id)
            if not direc or direc.estado == "borrado": return jsonify({"msg": "Registro no encontrado"}), 404
            return jsonify(direc.serialize()), 200
        else:
            direc = Direccion.query.all()
            direc = list(map(lambda direc: direc.serialize(), direccion))
            return jsonify(direc), 200
        
    if request.method == 'PUT':
        direccion = request.json.get('direccion')
        numero = request.json.get('numero')
        comuna = request.json.get('comuna')
        tipoVivienda = request.json.get('tipoVivienda')
        numDepto = request.json.get('numDepto')

        if not direccion: return jsonify({"msg": "direccion es requerido"}), 400
        if not numero: return jsonify({"msg": "numero es requerido"}), 400
        if not comuna: return jsonify({"msg": "comuna es requerido"}), 400
        if not tipoVivienda: return jsonify({"msg": "tipoVivienda es requerido"}), 400
        if not numDepto: return jsonify({"msg": "numDepto es requerido"}), 400

        direc = Direccion.query.get(id)
        if not direc: return jsonify({"msg": "Registro no encontrado"}), 404

        direc.direccion = direccion
        direc.numero = numero
        direc.comuna = comuna
        direc.tipoVivienda = tipoVivienda
        direc.numDepto = numDepto
        direc.estado = "activo"
        direc.f_modificacion = datetime.date.today()

        direc.update()

        return jsonify(direc.serialize()), 201

    if request.method == 'DELETE':
        direc = Direccion.query.get(id)
        if not direc or direc.estado == "borrado": return jsonify({"msg": "Direccion no Encontrada"}), 404
        direc.estado = "borrado"
        direc.f_eliminacion = datetime.date.today()
        direc.update()
        return jsonify({"msg": "Registro Borrado"}), 200

@app.route('/api/autor/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def autorid(id = None):

    if request.method == 'GET':
        if id is not None:
            autor = Autor.query.get(id)
            if not autor or autor.estado == "borrado": return jsonify({"msg": "Registro no encontrado"}), 404
            return jsonify(autor.serialize()), 200
        else:
            autor = Autor.query.all()
            autor = list(map(lambda autor: autor.serialize(), autor))
            return jsonify(autor), 200
        
    if request.method == 'PUT':
        nombre = request.json.get('nombreAutor')
        pais = request.json.get('pais')

        if not nombre: return jsonify({"msg": "nombre es requerido"}), 400
        if not pais: return jsonify({"msg": "pais es requerido"}), 400

        autor = Autor.query.get(id)
        if not autor: return jsonify({"msg": "Registro no encontrado"}), 404

        autor.nombre = nombre
        autor.pais = pais
        autor.estado = "activo"
        autor.f_modificacion = datetime.date.today()

        autor.update()

        return jsonify(autor.serialize()), 201

    if request.method == 'DELETE':
        autor = Autor.query.get(id)
        if not autor or autor.estado == "borrado": return jsonify({"msg": "autor no Encontrada"}), 404
        autor.estado = "borrado"
        autor.f_eliminacion = datetime.date.today()
        autor.update()
        return jsonify({"msg": "Registro Borrado"}), 200

@app.route('/api/libro/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def libroid(id = None):

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
        titulo = request.json.get('titulo')
        aditorial = request.json.get('aditorial')
        nivel = request.json.get('nivel')
        asignatura = request.json.get('asignatura')
        estadoNuevoUsado = request.json.get('estadoNuevoUsado')
        condicionOriginalCopia = request.json.get('condicionOriginalCopia')
        comentarios = request.json.get('comentarios')
    
        if not titulo: return jsonify({"msg": "titulo es requerido"}), 400
        if not aditorial: return jsonify({"msg": "aditorial es requerida"}), 400
        if not estadoNuevoUsado: return jsonify({"msg": "estadoNuevoUsado es requerida"}), 400
        if not condicionOriginalCopia: return jsonify({"msg": "condicionOriginalCopia es requerida"}), 400
        if not comentarios: return jsonify({"msg": "comentarios es requerida"}), 400

        libro = Libro.query.get(id)
        if not libro: return jsonify({"msg": "Registro no encontrado"}), 404

        libro.titulo = titulo
        libro.aditorial = aditorial
        libro.nivel = nivel
        libro.asignatura = asignatura
        libro.estadoNuevoUsado = estadoNuevoUsado
        libro.condicionOriginalCopia = condicionOriginalCopia
        libro.comentarios = comentarios
        libro.estado = "activo"
        libro.f_modificacion = datetime.date.today()

        libro.update()

        return jsonify(libro.serialize()), 201

    if request.method == 'DELETE':
        libro = Libro.query.get(id)
        if not libro or libro.estado == "borrado": return jsonify({"msg": "libro no Encontrada"}), 404
        libro.estado = "borrado"
        libro.f_eliminacion = datetime.date.today()
        libro.update()
        return jsonify({"msg": "Registro Borrado"}), 200


@app.route('/api/venta_permuta/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def venta_permutaid(id = None):

    if request.method == 'GET':
        if id is not None:
            ventapermuta = VentaPermuta.query.get(id)
            if not ventapermuta or ventapermuta.estado == "borrado": return jsonify({"msg": "Registro no encontrado"}), 404
            return jsonify(ventapermuta.serialize()), 200
        else:
            ventapermuta = VentaPermuta.query.all()
            ventapermuta = list(map(lambda ventapermuta: ventapermuta.serialize(), ventapermuta))
            return jsonify(ventapermuta), 200
        
    if request.method == 'PUT':
        cliente_id = request.json.get('idRut')
        direccion_id = request.json.get('idDireccion')
        libro_id = request.json.get('idLibro')
        tipoIntercambio = request.json.get('tipoIntercambio')
        precio = request.json.get('precio')
    
        if not cliente_id: return jsonify({"msg": "idRut es requerido"}), 400
        if not direccion_id: return jsonify({"msg": "idDireccion es requerida"}), 400
        if not libro_id: return jsonify({"msg": "idLibro es requerido"}), 400
        if not tipoIntercambio: return jsonify({"msg": "tipoIntercambio es requerida"}), 400
        if not precio: return jsonify({"msg": "precio es requerido"}), 400

        ventapermuta = VentaPermuta.query.get(id)
        if not ventapermuta: return jsonify({"msg": "Registro no encontrado"}), 404

        ventapermuta.cliente_id = cliente_id
        ventapermuta.direccion_id = direccion_id
        ventapermuta.libro_id = libro_id
        ventapermuta.tipoIntercambio = tipoIntercambio
        ventapermuta.precio = precio
        ventapermuta.estado = "activo"
        ventapermuta.f_modificacion = datetime.date.today()

        ventapermuta.update()

        return jsonify(ventapermuta.serialize()), 201

    if request.method == 'DELETE':
        ventapermuta = VentaPermuta.query.get(id)
        if not ventapermuta or ventapermuta.estado == "borrado": return jsonify({"msg": "Registro no Encontrada"}), 404
        ventapermuta.estado = "borrado"
        ventapermuta.f_eliminacion = datetime.date.today()
        ventapermuta.update()
        return jsonify({"msg": "Registro Borrado"}), 200

if __name__ == '__main__':
    app.run()