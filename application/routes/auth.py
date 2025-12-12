from flask import Blueprint, request, jsonify, session, redirect, url_for
import json
import os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

CAMINHO = "data/usuarios.json"


def carregar_usuarios():
    if not os.path.exists(CAMINHO):
        return {}
    with open(CAMINHO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_usuarios(usuarios_dict):
    os.makedirs(os.path.dirname(CAMINHO), exist_ok=True)
    with open(CAMINHO, "w", encoding="utf-8") as f:
        json.dump(usuarios_dict, f, indent=4, ensure_ascii=False)


@auth_bp.route("/register", methods=["POST"])
def register():
    if request.is_json:
        data = request.json
    else:
        data = request.form
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    if not nome or not email or not senha:
        if request.is_json:
            return jsonify({"erro": "Preencha todos os campos!"}), 400
        else:
            return redirect(url_for('main.login_page'))
    usuarios = carregar_usuarios()
    if email in usuarios:
        if request.is_json:
            return jsonify({"erro": "Email já existe!"}), 409
        else:
            return redirect(url_for('main.login_page'))
    usuarios[email] = {"nome": nome, "email": email, "senha": senha}
    salvar_usuarios(usuarios)
    if request.is_json:
        return jsonify({"status": "ok"})
    else:
        return redirect(url_for('main.login_page'))


@auth_bp.route("/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.json
    else:
        data = request.form
    email = data.get("email")
    senha = data.get("senha")
    usuarios = carregar_usuarios()
    user = usuarios.get(email)
    if not user or user["senha"] != senha:
        if request.is_json:
            return jsonify({"erro": "Email ou senha incorretos!"}), 401
        else:
            return redirect(url_for('main.login_page'))
    session["usuario"] = {
        "nome": user["nome"],
        "email": user["email"]
    }
    if request.is_json:
        return jsonify({"status": "ok"})
    else:
        return redirect(url_for('main.home'))


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("usuario", None)
    return jsonify({"status": "ok"})


@auth_bp.route("/session")
def check_session():
    if "usuario" in session:
        return jsonify({"logado": True, "usuario": session["usuario"]})
    return jsonify({"logado": False})
