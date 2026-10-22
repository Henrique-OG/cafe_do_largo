from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class PratoForm(FlaskForm):
    nome = StringField(
        "Nome do prato",
        validators=[
            DataRequired(message="Informe o nome do prato."),
            Length(max=60, message="O nome deve ter no máximo 60 caracteres.")
        ],
    )

    valor = DecimalField(
        "Valor (R$)",
        places=2,
        validators=[
            DataRequired(message="Informe o valor"),
            NumberRange(min=0.01, max=9999.99, message="Valor inválido"),
        ]
    )

    sobre_prato = TextAreaField(
        "Descrição",
        validators=[
            Optional(),
            Length(max=300, message="A descrição pode ter no máximo 300 caracteres."),
        ]
    )

    classificacao = SelectField(
        'Classificação do prato',
        render_kw={"class": "classificacao_prato_escolha"},
        choices=[
            ('salgado', 'Salgado'),
            ('doce', 'Doce'),
            ('bebida', 'Bebida')
        ],
        validators=[DataRequired()]
    )

    imagem = FileField(
        "Imagem do prato",
        render_kw={"class": "colocar_imagem_forms"},
        validators=[
            FileRequired(message="Escolha uma imagem."),
            FileAllowed(["jpg", "jpeg", "png", "webp"], message="Envie apenas JPG, PNG ou WEBP."),
        ],
    )

    enviar = SubmitField("Cadastrar prato")