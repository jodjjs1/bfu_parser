from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import InputRequired

def chek_snils_validator(form, field):
        if len(field.data) > 14:
            raise ValidationError('Некоректный снилс')

class SnilsForm(FlaskForm):
    snils = StringField('Снилс:', description='000-000-000 00' , validators=[InputRequired(), chek_snils_validator]) # написать валидатор
    submit = SubmitField('Искать')
