#criar as rotas/views do nosso site

from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import Formlogin, Formcriarconta, Formfoto
from fakepinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename


@app.route("/")
def homepage():
    foto = Foto.query.order_by(Foto.data.desc())[:3]
    return render_template("homepage.html",fotos=foto)


@app.route("/login", methods=["GET", "POST"])
def login():
    formlogin = Formlogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and usuario.senha == formlogin.senha.data: #bcrypt.check_password_hash(usuario.senha,formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", variavel=usuario.id))

    return render_template("login.html", form=formlogin)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    formcadastro = Formcriarconta()
    if formcadastro.validate_on_submit():
        senha = formcadastro.senha.data #bcrypt.generate_password_hash(formcadastro.senha.data)
        usuario = Usuario(nome=formcadastro.nome.data, email=formcadastro.email.data, senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", variavel=usuario.id))
    return render_template("cadastro.html", form=formcadastro)


@app.route("/perfil/<variavel>", methods=["GET", "POST"])
@login_required
def perfil(variavel):
    if int(variavel) == int(current_user.id):
        formfotos = Formfoto()
        if formfotos.validate_on_submit():
            arquivo = formfotos.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", email=current_user, usuario=current_user, form=formfotos)
    else:
        usuario = Usuario.query.get(int(variavel))
        return render_template("perfil.html", usuario=usuario, email=None, form=None)


@app.route("/home")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feeds")
@login_required
def feed():
    foto = Foto.query.order_by(Foto.data.desc()).all()
    return render_template("feed.html", fotos=foto)
