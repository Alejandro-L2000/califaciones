from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(120), index=True)
    apellido_paterno = db.Column(db.String(120), index=True)
    apellido_materno = db.Column(db.String(120))
    matricula = db.Column(db.String(10), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__ (self):
        return "Usuario: {}, Email: {}". format(self.matricula, self.email)
