from flask_login.utils import login_required, logout_user
from app.forms import LoginForm, RegisterForm, CursoForm, TareaForm
from app import app
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Curso, Tarea, Calificacion
from app import db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
# @login_required
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        # Lidera con datos del Login
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        if user is None or  not user.check_password(form.password.data):
            ## FLASK con el Error
            print("Usuario no existe")
            return redirect(url_for("login"))
        else:
            login_user(user, remember = form.remember_me.data)
        return redirect(url_for("index"))
    else:
        return render_template("login.html", form=form)
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        # Lidera con datos del Login
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        if user is None and form.password.data == form.password_confirm.data:
            user = User(email = email)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember = True)
            return redirect(url_for("login"))
        else:
            return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# Cursos
@app.route("/cursos", methods=["GET"])
@login_required
def cursos_index():
    # Solo puedan acceder profesores.
    curso = Curso.query.filter_by(id_profesor = current_user.id).all()
    return render_template("cursos_index.html", curso=curso)

@app.route("/cursos/<int:id>")
@login_required
def cursos_show(id):
    curso = Curso.query.filter_by(id=id).first()
    # for alumno in cursos.alumnos:
    return render_template("cursos_show.html", curso=curso)

@app.route("/cursos/create", methods=["GET", "POST"])
@login_required
def cursos_create():
    form = CursoForm()
    if form.validate_on_submit():
        print(form.name.data)
        curso = Curso(name = form.name.data, id_profesor = current_user.id)
        db.session.add(Curso)
        db.session.commit()
        return redirect(url_for("cursos_index"))
    else:
        # Pendiente el formulario
        return render_template("curso_create.html", form=form)

# <!-- cursos/<int:id>/alumnos/store -->
@login_required
@app.route("/cursos/<int:id_curso>/alumnos/store", methods=["POST"])
def cursos_alumnos_store(id_curso):
    correos = request.form["alumnos"]
    correos = correos.replace(" ","")
    correos = correos.split(",")
    curso = Curso.query.filter_by(id=id_curso).first()

    for correo in correos:
        # Si el alumno ya esta inscrito, saltar
        alumno = User.query.filter_by(email=correo).first()
        if alumno:
            # if alumno esta inscrito no inscribir
            curso.alumnos.append(alumno)
        else:
            pass
    # db.session.add(curso)
    db.session.commit()
    return redirect(url_for("cursos_show", id=id_curso))

@app.route("/cursos/destroy/<int:id>", methods=["GET"])
@login_required
def cursos_destroy(id):
    # Revisar la BD por si existe ese curso.
    curso = Curso.query.filter_by(id=id).first()
    # Eliminarlo de la base de datos.
    db.session.delete(curso)
    db.session.commit()
    # Redireccionar a cursos_create
    return redirect(url_for("cursos_index"))
    # return str(curso.name)

#Tareas
@app.route("/cursos/<int:id>/tareas/create", methods=["GET","POST"])
@login_required
def cursos_tareas_create(id):
    curso = Curso.query.filter_by(id=id).first()
    form = TareaForm()
    if form.validate_on_submit():
        # POST
        tarea = Tarea()
        tarea.titulo = form.titulo.data
        tarea.id_curso = id
        tarea.fecha_de_creacion = form.fecha_de_creacion.data
        tarea.fecha_de_entrega = form.fecha_de_entrega.data
        tarea.descripcion = form.descripcion.data
        tarea.puntaje = form.puntos.data
        db.session.add(tarea)
        db.session.commit()
        return redirect(url_for("cursos_tareas_index", id=id))
    else:
        return render_template("cursos_tareas_create.html", curso=curso, form=form)

@app.route("/cursos/<int:id>/tareas", methods=["GET","POST"])
@login_required
def cursos_tareas_index(id):
    curso = Curso.query.filter_by(id=id).first()
    tareas = Tarea.query.filter_by(id_curso=id)
    return render_template("cursos_tareas_index.html", curso=curso, tareas=tareas)

#Calificaciones

#Editar calificaciones
@app.route("/cursos/<int:id_curso>/tareas/<int:id_tarea>/edit", methods=["GET","POST"])
@login_required
def cursos_tareas_calificaciones_edit(id_curso, id_tarea):
    curso = Curso.query.filter_by(id=id_curso).first()
    tarea = Curso.query.filter_by(id=id_tarea).first()
    calificaciones = Calificacion.query.filter_by(id_tarea=id_tarea).all()
    for calificacion in calificaciones:
        calificaciones_dict[calificacion.id_alumno] = calificacion.calificacion
    return render_template("cursos_tareas_calificaciones_edit.html", curso=curso, tarea=tarea, alumnos=curso.alumnos, calificaciones=calificaciones_dict)

#Update calificaciones
@app.route("/cursos/<int:id_curso>/tareas/<int:id_tarea>/update", methods=["GET","POST"])
@login_required
def cursos_tareas_calificaciones_update(id_curso, id_tarea):
    calificaciones = request.form
    for id_alumno, calificacion_tarea in calificaciones.items():
        calificacion = Calificacion.query.filter_by(id_alumno=id_alumno, id_tarea=id_tarea).first()
        if not calificacion:
            calificacion = Calificacion()
            calificacion.id_alumno = id_alumno
            calificacion.id_tarea = id_tarea
        calificacion.calificacion = calificacion_tarea

        db.session.add(calificacion)
    db.session.commit()
    return redirect(url_for("cursos_tareas_calificaciones_edit", id_tarea=id_tarea, id_curso=id_curso))
