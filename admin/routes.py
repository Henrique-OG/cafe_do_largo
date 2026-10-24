from admin import admin_bp
import os
import uuid 

from flask import render_template, redirect, request, url_for, flash, current_app
from werkzeug.utils import secure_filename

from admin.forms import PratoForm, EditarPratoForm
from extensions import db
from models import Pratos
from werkzeug.datastructures import FileStorage


def salvar_imagem(arquivo):
    extensao = os.path.splitext(secure_filename(arquivo.filename))[1].lower()
    nome_final = f"{uuid.uuid4().hex}{extensao}"

    pasta = os.path.join(current_app.static_folder, "imagens", "pratos")
    os.makedirs(pasta, exist_ok=True)

    arquivo.save(os.path.join(pasta, nome_final))
    return nome_final

@admin_bp.route("/pratos/novo", methods=["GET","POST"])
def novo_prato():
    form = PratoForm()

    if form.validate_on_submit():
        nome_arquivo = salvar_imagem(form.imagem.data)

        prato = Pratos(
            nome=form.nome.data.strip(),
            valor=form.valor.data,
            sobre_prato=(form.sobre_prato.data or '').strip(),
            classificacao=form.classificacao.data,
            imagem=nome_arquivo,
        )
        db.session.add(prato)
        db.session.commit()

        flash("Prato cadastrado com sucesso!")
        return redirect(url_for("admin.novo_prato"))
    return render_template("admin/adicionar_prato.html", form=form)

@admin_bp.route("/pratos/gerenciar", methods=["GET"])
def gerenciar_pratos():
    filtro = request.args.get('filtro')
    if filtro == 'todos':
        pratos = Pratos.query.all()
    elif filtro == "salgados":
        pratos = Pratos.query.filter_by( classificacao="salgado").all()
    elif filtro == "doces":
        pratos = Pratos.query.filter_by( classificacao="doce").all()
    elif filtro == "bebidas":
        pratos = Pratos.query.filter_by( classificacao="bebida").all()
    else:
        pratos = Pratos.query.all()

    return render_template("admin/gerenciar_pratos.html" , pratos = pratos)

@admin_bp.route("/pratos/gerenciar/excluir/<int:prato_id>", methods=["POST"])
def excluir_prato(prato_id):

    prato = db.get_or_404(Pratos, prato_id)
    nome_imagem = prato.imagem

    db.session.delete(prato)
    db.session.commit()

    if nome_imagem:
        caminho = os.path.join(
                current_app.static_folder,
                'imagens',
                'pratos',
                nome_imagem
            )
            
        if os.path.isfile(caminho):
            os.remove(caminho)

    return redirect(url_for('admin.gerenciar_pratos'))

@admin_bp.route("/pratos/editar/<int:prato_id>", methods=["GET","POST"])
def editar_prato(prato_id):
    prato = db.get_or_404(Pratos, prato_id)
    form = EditarPratoForm(obj=prato)

    if form.validate_on_submit():
        prato.nome = form.nome.data.strip()
        prato.valor = form.valor.data
        prato.sobre_prato = (form.sobre_prato.data or '').strip()
        prato.classificacao = form.classificacao.data
        arquivo = form.imagem.data

        if isinstance(arquivo, FileStorage) and arquivo.filename:
            nome_imagem_antiga = prato.imagem
            caminho = os.path.join(current_app.static_folder, "imagens", "pratos", nome_imagem_antiga)
            os.remove(caminho)

            nome_arquivo = salvar_imagem(form.imagem.data)
            prato.imagem = nome_arquivo
        
        db.session.commit()

        flash("Prato atualizado com sucesso!")
        return redirect(url_for("admin.gerenciar_pratos"))
    return render_template("admin/editar_prato.html", form=form)

@admin_bp.route("/pratos/alternar-disponibilidade/<int:prato_id>", methods=["POST"])
def alternar_disponibilidade(prato_id):
    prato = db.get_or_404(Pratos, prato_id)
    prato.disponibilidade = not prato.disponibilidade
    db.session.commit()
    return redirect(url_for('admin.gerenciar_pratos'))

    