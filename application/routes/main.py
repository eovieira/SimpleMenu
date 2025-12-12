from flask import Blueprint, render_template, session, redirect, request, jsonify
import urllib.parse
import os
from twilio.rest import Client

main_bp = Blueprint("main", __name__)

TWILIO_ACCOUNT_SID = 'SIDdaSuaContaTwilioAqui'
TWILIO_AUTH_TOKEN = 'AutenticacaoDaSuaContaTwilioAqui'
TWILIO_WHATSAPP_FROM = 'whatsapp:+14155238886'


@main_bp.route("/")
def home():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("index.html", usuario=session["usuario"])


@main_bp.route("/login")
def login_page():
    if "usuario" in session:
        return redirect("/")
    return render_template("login.html")


@main_bp.route('/send_whatsapp', methods=['POST'])
def send_whatsapp():
    if "usuario" not in session:
        return jsonify({"erro": "Não autorizado"}), 401
    data = request.json or {}
    phone = data.get('phone', '')
    message = data.get('message', '')
    phone_digits = ''.join(ch for ch in phone if ch.isdigit())
    if not phone_digits.startswith('55'):
        return jsonify({"erro": "Telefone deve conter DDI do Brasil (ex: 5511999998888)"}), 400
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    from_whatsapp = TWILIO_WHATSAPP_FROM
    client = Client(account_sid, auth_token)
    try:
        msg = client.messages.create(
            from_=from_whatsapp,
            body=message,
            to=f'whatsapp:+{phone_digits}'
        )
        return jsonify({"status": "ok", "sid": msg.sid})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
