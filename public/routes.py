from flask import render_template, request
from public import public_bp
from models import Pratos

@public_bp.route('/')
def apresentacao():
    return render_template('index.html')

@public_bp.route('/cardapio')
def cardapio():
    filtro = request.args.get('filtro')
    if filtro == 'todos':
        pratos = Pratos.query.filter_by(disponibilidade=True).all()
    elif filtro == "salgados":
        pratos = Pratos.query.filter_by(disponibilidade=True, classificacao="salgado").all()
    elif filtro == "doces":
        pratos = Pratos.query.filter_by(disponibilidade=True, classificacao="doce").all()
    elif filtro == "bebidas":
        pratos = Pratos.query.filter_by(disponibilidade=True, classificacao="bebida").all()
    else:
        pratos = Pratos.query.filter_by(disponibilidade=True).all()


    return render_template('public/cardapio.html', pratos = pratos)
