# Relatório Diário Automático (Cloud Run)

Este projeto expõe o endpoint `/relatorio-diario` que, ao ser acessado, executa uma consulta no BigQuery, gera um CSV e envia por e-mail automaticamente.

## Configuração

1. **Configurar variáveis de ambiente no deploy do Cloud Run:**
   - EMAIL_REMETENTE: email que vai enviar (ex: seu_email@gmail.com)
   - EMAIL_SENHA: senha de app do Gmail (não a senha normal)
   - EMAIL_DESTINATARIOS: lista de e-mails separados por vírgula

2. **Ajustar a query do BigQuery em `main.py`:**
   - Troque `SEU_PROJECT_ID.SEU_DATASET.SEU_TABLE` pela sua tabela.

3. **Build e Deploy:**

   ```bash
   gcloud builds submit --tag gcr.io/SEU_PROJECT_ID/relatorio-diario
   gcloud run deploy relatorio-diario \
     --image gcr.io/SEU_PROJECT_ID/relatorio-diario \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars EMAIL_REMETENTE=seu_email@gmail.com,EMAIL_SENHA=sua_senha_app,EMAIL_DESTINATARIOS=email1@dominio.com,