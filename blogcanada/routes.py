from flask import render_template, url_for, request, flash, redirect, abort
from blogcanada import app, database, bcrypt
from blogcanada.forms import FormLogin, FormCriarConta, FormEditProfile, FormCreatePost
from blogcanada.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route("/", methods=['GET', 'POST'])
def homepage():
    posts = Post.query.order_by(Post.id.desc())

    return render_template('homepage.html', posts=posts)


@app.route("/contato")
def contato():
    return render_template('contato.html')


@app.route("/usuarios")
@login_required
def usuario():
    lista_usuarios = User.query.all()
    return render_template('usuario.html', lista_usuarios=lista_usuarios)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and 'login_button' in request.form:
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.still_conected.data)
            flash(f'Login realizado com sucesso no e-mail: {form_login.email.data}', 'alert-primary')
            next_par = request.args.get('next')
            if next_par:
                return redirect(next_par)
            else:
                return redirect(url_for('homepage'))
        else:
            flash(f'Falha no login. E-mail ou Senha incorretos.', 'alert-danger')

    if form_criar_conta.validate_on_submit() and 'submmit_button' in request.form:
        crypt_password = bcrypt.generate_password_hash(form_criar_conta.password.data)
        user = User(username=form_criar_conta.username.data, email=form_criar_conta.email.data, password=crypt_password)
        database.session.add(user)
        database.session.commit()
        flash(f'Conta criada com sucesso : {form_criar_conta.username.data}', 'alert-primary')
        return redirect(url_for('homepage'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criar_conta)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Logout completed successfully', 'alert-primary')
    return redirect(url_for('homepage'))


@app.route('/profile')
@login_required
def profile():
    profile_picture = url_for('static', filename=f'profile_pictures/{current_user.profile_picture}')
    return render_template('profile.html', profile_picture=profile_picture)


@app.route('/post/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = FormCreatePost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, post_body=form.post_body.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post created successfully.', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template('newpost.html', form=form)


def save_picture(picture):
    cod = secrets.token_hex(8)
    name, extension = os.path.splitext(picture.filename)
    file_name = name + cod + extension
    path = os.path.join(app.root_path, 'static/profile_pictures', file_name)
    size = (400, 400)
    reduced_image = Image.open(picture)
    reduced_image.thumbnail(size)
    reduced_image.save(path)
    return file_name


def update_games(form):
    game_list = []
    for campo in form:
        if 'button_' in campo.name:
            if campo.data:
                game_list.append(campo.label.text)
    return ';'.join(game_list)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = FormEditProfile()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.profile_picture.data:
            picture_name = save_picture(form.profile_picture.data)
            current_user.profile_picture = picture_name
        current_user.games = update_games(form)
        database.session.commit()
        flash(f'Profile updated successfully', 'alert-success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        for game in current_user.games.split(';'):
            for campo in form:
                if game in campo.label.text:
                    campo.data = True
    profile_picture = url_for('static', filename=f'profile_pictures/{current_user.profile_picture}')
    return render_template('editprofile.html', profile_picture=profile_picture, form=form)


@app.route('/post/<post_id>',methods=['GET', 'POST'])
@login_required
def show_posts(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        form = FormCreatePost()
        if request.method == 'GET':
            form.title.data = post.title
            form.post_body.data = post.post_body
        elif form.validate_on_submit():
            post.title = form.title.data
            post.post_body = form.post_body.data
            database.session.commit()
            flash('Post Update Successfully!', 'alert-success')
            return redirect(url_for('homepage'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)



@app.route('/post/<post_id>/delete',methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        database.session.delete(post)
        database.session.commit()
        flash('Post successfully deleted', 'alert-danger')
        return redirect(url_for('homepage'))
    else:
        abort(403)