from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models import Category






class AddCategoryForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AddRecordForm(FlaskForm):
    name = StringField('Наименование записи', validators=[DataRequired()])
    # category_id = SelectField('Категория', choices=categories)
    submit = SubmitField('Добавись')
