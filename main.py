from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.notes import Note
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.note_form import Note_form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/notes_database.db")
    app.run("localhost", "5050")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/")
def index():
    session = db_session.create_session()
    notes = []
    auth = False
    try:
        a = current_user.id
        auth = True
    except Exception:
        auth = False
    if auth:
        if current_user.login == "admin":
            notes = list(session.query(Note))
        else:
            notes = list(session.query(Note).filter(current_user.id == Note.user_id))
    return render_template("index.html", notes=notes)



@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.login.data == "admin":
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Данный логин запрещён")
        user = User(
            name=form.name.data,
            login=form.login.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add', methods=['POST', "GET"])
@login_required
def add_note():
    form = Note_form()
    if form.validate_on_submit():
        ds = db_session.create_session()
        note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        ds.add(note)
        ds.commit()
        return redirect("/")
    return render_template("note_add.html", title='Создание новости', form=form)


@app.route("/del/<note_id>", methods=["GET"])
@login_required
def confirm_delete(note_id):
    session = db_session.create_session()
    note = list(session.query(Note).filter(Note.id == note_id))[0]
    return render_template("delete.html", note=note)


@app.route("/delete/<note_id>", methods=["POST", "GET"])
@login_required
def delete_note(note_id):
    session = db_session.create_session()
    note = list(session.query(Note).filter(Note.id == note_id))[0]
    if current_user.id == note.user_id or current_user.login == "admin":
        session.delete(note)
        session.commit()
    return redirect('/')


if __name__ == '__main__':
    main()
