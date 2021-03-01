from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombreCompleto = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    contrasenia = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    comuna = db.Column(db.String(100), nullable=False)
    tipoVivienda = db.Column(db.String(20), nullable=False)
    numDepto = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    f_creacion = db.Column(db.Date, nullable=True)
    f_modificacion = db.Column(db.Date, nullable=True)
    f_eliminacion = db.Column(db.Date, nullable=True)
    libros_id = db.relationship('Libro', cascade='all,delete', backref="cliente", lazy=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "nombreCompleto": self.nombreCompleto,
            "correo": self.correo,
            "telefono": self.telefono,
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

    def cliente_libro(self):
        return {
            "id": self.id,
            "nombreCompleto": self.nombreCompleto,
            "libros": self.get_libros,
        }

    def get_libros (self):
        return list(map(lambda libro: libro.serialize(), self.libros_id))

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
    nombreAutor = db.Column(db.String(100), nullable=False)
    editorial = db.Column(db.String(100), nullable=False)
    nivel = db.Column(db.String(100), nullable=False)
    asignatura = db.Column(db.String(100), nullable=False)
    estadoNuevoUsado = db.Column(db.String(100), nullable=False)
    condicionOriginalCopia = db.Column(db.String(100), nullable=False)
    tipoIntercambio = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=True)
    estado = db.Column(db.String(100), nullable=False)
    comentarios = db.Column(db.String(100), nullable=False)
    f_creacion = db.Column(db.Date, nullable=True)
    f_modificacion = db.Column(db.Date, nullable=True)
    f_eliminacion = db.Column(db.Date, nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete= 'CASCADE'), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "nombreAutor": self.nombreAutor,
            "editorial": self.editorial,
            "nivel": self.nivel,
            "asignatura": self.asignatura,
            "estadoNuevoUsado": self.estadoNuevoUsado,
            "condicionOriginalCopia": self.condicionOriginalCopia,
            "tipoIntercambio": self.tipoIntercambio,
            "precio": self.precio,
            "estado": self.estado,
            "comentarios": self.comentarios,
            "cliente_id": self.cliente_id,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()