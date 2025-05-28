import os
from flask import Flask
from google.cloud import bigquery
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

@app.route("/relatorio-diario", methods=["GET"])
def relatorio_diario():
    # Consulta ao BigQuery
    client = bigquery.Client()
    QUERY = """
        SELECT
            data_envio,
            num_paginas
        FROM `neogov-default.arquivos.relatorios_uploads`
        WHERE DATE(data_envio) = CURRENT_DATE("America/Sao_Paulo")
        ORDER BY data_envio DESC
    """
    df = client.query(QUERY).to_dataframe()
    if df.empty:
        return "Nenhum upload hoje.", 200

    # Gera CSV temporário
    file_path = '/tmp/relatorio_diario.csv'
    df.to_csv(file_path, index=False)

    # Dados do e-mail (via variáveis de ambiente para segurança)
    remetente = os.environ.get('EMAIL_REMETENTE')
    senha = os.environ.get('EMAIL_SENHA')
    destinatarios = os.environ.get('EMAIL_DESTINATARIOS', '').split(',')
    assunto = 'Relatório Diário de Uploads PDF'
    corpo = 'Segue em anexo o relatório diário de uploads de PDFs.'

    # Monta e envia o e-mail
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = ", ".join(destinatarios)
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    with open(file_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename=relatorio_diario.csv')
        msg.attach(part)

    # Envio via SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remetente, senha)
    server.sendmail(remetente, destinatarios, msg.as_string())
    server.quit()

    return "Relatório enviado com sucesso!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
