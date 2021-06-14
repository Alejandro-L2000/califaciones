from sqlalchemy.orm import backref, subqueryload
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(120), index=True)
    apellido_paterno = db.Column(db.String(120), index=True)
    apellido_materno = db.Column(db.String(120))
    matricula = db.Column(db.String(10), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cursos = db.relationship("Curso", backref="profesor", lazy="dynamic")

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__ (self):
        return "Usuario: {}, Email: {}". format(self.matricula, self.email)

usuario_curso = db.Table("usuario_curso", 
    db.Column("id_user", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("id_curso", db.Integer, db.ForeignKey("curso.id"), primary_key=True)
    )

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    id_profesor = db.Column(db.Integer, db.ForeignKey("user.id"))
    alumnos = db.relationship("User", secondary=usuario_curso, lazy="subquery", backref=db.backref("cursos",lazy=True))

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey("curso.id"))
    titulo = db.Column(db.String(150))
    fecha_de_creacion = db.Column(db.DateTime) 
    fecha_de_entrega = db.Column(db.DateTime)
    descripcion = db.Column(db.String(1500))
    puntaje = db.Column(db.Integer)

class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # id_curso = db.Column(db.Integer, db.ForeignKey("curso.id"))
    id_tarea = db.Column(db.Integer, db.ForeignKey("tarea.id"))
    id_alumno = db.Column(db.Integer, db.ForeignKey("user.id"))
    calificacion = db.Column(db.Integer)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))