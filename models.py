from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombreCompleto = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    contrasenia = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    f_creacion = db.Column(db.Date, nullable=True)
    f_modificacion = db.Column(db.Date, nullable=True)
    f_eliminacion = db.Column(db.Date, nullable=True)
    direccion = db.relationship("Direccion", backref="cliente", uselist=False)
    ventaPermuta = db.relationship("VentaPermuta", backref="cliente", uselist=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "nombreCompleto": self.nombreCompleto,
            "correo": self.correo,
            "telefono": self.telefono,
            "estado": self.estado,
            "f_creacion": self.f_creacion,
            "f_modificacion": self.f_modificacion,
            "f_eliminacion": self.f_eliminacion,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Direccion(db.Model):
    __tablename__ = 'direcciones'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    comuna = db.Column(db.String(100), nullable=False)
    tipoVivienda = db.Column(db.String(20), nullable=False)
    numDepto = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    f_creacion = db.Column(db.Date, nullable=True)
    f_modificacion = db.Column(db.Date, nullable=True)
    f_eliminacion = db.Column(db.Date, nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    ventaPermuta = db.relationship("VentaPermuta", backref="direccion", uselist=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "direccion": self.direccion,
            "numero": self.numero,
            "comuna": self.comuna,
            "tipoVivienda": self.tipoVivienda,
            "numDepto": self.numDepto,
            "estado": self.estado,
            "f_creacion": self.f_creacion,
            "f_modificacion": self.f_modificacion,
            "f_eliminacion": self.f_eliminacion,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class VentaPermuta(db.Model):
    __tablename__ = 'ventaPermuta'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    direccion_id = db.Column(db.Integer, db.ForeignKey('direcciones.id'), nullable=False)
    tipoIntercambio = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.String(100), nullable=False)
    
    
    def serialize(self):
        return {
            "cliente_id": self.cliente_id,
            "direccion_id": self.direccion_id,
            "libro_id": self.libro_id,
            "tipoIntercambio": self.tipoIntercambio,
            "precio": self.precio,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Libro(db.Model):
    __tablename__ = 'libros'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    aditorial = db.Column(db.String(100), nullable=False)
    nivel = db.Column(db.String(100), nullable=False)
    asignatura = db.Column(db.String(100), nullable=False)
    estadoNuevoUsado = db.Column(db.String(100), nullable=False)
    condicionOriginalCopia = db.Column(db.String(100), nullable=False)
    comentarios = db.Column(db.String(100), nullable=False)
    ventaPermuta = db.relationship("VentaPermuta", backref="libro", uselist=False)
    libroAutor = db.relationship("LibroAutor", backref="libro", uselist=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "aditorial": self.aditorial,
            "nivel": self.nivel,
            "asignatura": self.asignatura,
            "estadoNuevoUsado": self.estadoNuevoUsado,
            "condicionOriginalCopia": self.condicionOriginalCopia,
            "comentarios": self.comentarios,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Autor(db.Model):
    __tablename__ = 'autores'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    libroAutor = db.relationship("LibroAutor", backref="autor", uselist=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "pais": self.pais,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class LibroAutor(db.Model):
    __tablename__ = 'libroAutor'
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'), primary_key=True, nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), primary_key=True, nullable=False)

    
    def serialize(self):
        return {
            "autor_id": self.autor_id,
            "libro_id": self.libro_id,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()