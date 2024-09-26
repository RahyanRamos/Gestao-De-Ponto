import mysql.connector

def conexaoBD():
    conexao = mysql.connector.connect(
        passwd='Destak2024',
        port=3306,
        user='admin',
        host='destakveiculos.cjq8g4ggucwy.us-east-1.rds.amazonaws.com',
        database='gestao_escala'
    )

    return conexao
