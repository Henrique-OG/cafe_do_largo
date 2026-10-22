from admin import admin_bp
import os
import uuid 

from flask import render_template, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename

from admin.forms import PratoForm
from extensions import db
from models import Pratos

def salvar_imagem(arquivo):
    extensao = os.path.splitext(secure_filename(arquivo.filename))[1].lower()
    nome_final = f"{uuid.uuid4().hex}{extensao}"

    pasta = os.path.join(current_app.static_folder, "imagens", "pratos")
    os.makedirs(pasta, exist_ok=True)

    arquivo.save(os.path.join(pasta, nome_final))
    return nome_final

@admin_bp.route("pratos/novo", methods=["GET","POST"])
def novo_prato():
    form = PratoForm()

    if form.validate_on_submit():
        nome_arquivo = salvar_imagem(form.imagem.data)

        prato = Pratos(
            nome=form.nome.data.strip(),
            valor=float.valor.data,
            sobre_prato=form.sobre_prato.data.strip(),
            classificacao=form.classificacao.data,
            imagem=nome_arquivo,
        )
        db.session.add(prato)
        db.session.commit()

        flash("Prato cadastrado com sucesso!")
        return redirect(url_for("admin.novo_prato"))
    return render_template("admin/adicionar_prato.html", form=form)
