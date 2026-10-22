from extensions import db

class Pratos(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    sobre_prato = db.Column(db.Text())
    valor = db.Column(db.Numeric(8, 2), nullable=False)
    imagem = db.Column(db.String(255))
    classificacao = db.Column(db.String(30), nullable=False)
    disponibilidade = db.Column(db.Boolean, default=True)

class Adm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    senha = db.Column(db.String(255), nullable=False)

class Galeria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_img = db.Column(db.String(40))
    imagem_url = db.Column(db.String(255), nullable=True)