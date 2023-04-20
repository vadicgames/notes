from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class Note_form(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    submit = SubmitField('Создать')