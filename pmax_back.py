import mysql.connector


def tratar_direcao(dir):
    aux = {'I': 'IDA',
           'V': 'VOLTA'}
    
    return aux[str(dir).strip().upper()]


class Pmax():
    def __init__(self):
        self.__conexao = mysql.connector.connect(
            passwd='Destak2024',
            port=3306,
            user='admin',
            host='destakveiculos.cjq8g4ggucwy.us-east-1.rds.amazonaws.com',
            database='gestao_escala'
        )


    def __get_cursor(self):
        mycursor = self.__conexao.cursor()
        return mycursor


    def get_itenerarios(self):
        cmd = """        
            SELECT
                id_linha, 
                CP.nome_cidade AS CIDADE_INI,
                CP1.nome_cidade AS CIDADE_FIM,
                NOW() + INTERVAL hora_ini SECOND AS hora_ini,
                cod_linha,
                sentido_linha,
                status_linha
            FROM servico_linhas SL
            JOIN cidades_pontos CP ON CP.id_cidades = SL.fgkey_ponto_ini
            JOIN cidades_pontos CP1 ON CP1.id_cidades = SL.fgkey_ponto_fim;
        """    

        cursor = self.__get_cursor()
        cursor.execute(cmd)
        
        itenerarios = cursor.fetchall()
        cursor.close()

        return itenerarios
    
    def get_typeregistros(self):
        cmd = """SELECT id_registro, name_registro 
            FROM pmax_typeregistro
            WHERE status_registro = 1;"""
        
        cursor = self.__get_cursor()
        cursor.execute(cmd)
        
        typeregistros = cursor.fetchall()
        cursor.close()

        return typeregistros

    @staticmethod
    def set_iterarios(dados_itenerarios_post):
        dados_itenerarios = [
                            '{}. {} x {} ({}) - {}'.format(
                                            x[0],
                                            x[1],
                                            x[2],
                                            tratar_direcao(x[5]),
                                            x[3].time()        
                                        )
                                for x in dados_itenerarios_post]
        
        return dados_itenerarios
    
    # Consulta as jornadas de um motorista específico pela coluna fgkey_motorist.
    def get_jornadas_motorista(self, fgkey_motorist):
        cursor = self.__get_cursor()

        cmd = """SELECT
                id_gregistro, itinerario, fgkey_motorist
            FROM
                pmax_getregistro
            WHERE
                fgkey_motorist = %s;"""
        cursor.execute(cmd, (fgkey_motorist,))
        jornadas = cursor.fetchall()

        cursor.close()
        return jornadas

    # Consulta todos os registros de pontos na tabela pmax_setregistro para validar a presença do número 7 em fgkey_typ_regist.
    def get_registros_pontos(self):
        cursor = self.__get_cursor()

        cmd = """SELECT fgkey_get_regist, fgkey_typ_regist
            FROM pmax_setregistro;"""
        cursor.execute(cmd)
        registros_pontos = cursor.fetchall()

        cursor.close()
        return registros_pontos

    # Valida e prepara as jornadas que ainda não possuem o número 7 (jornadas em aberto).
    @staticmethod
    def set_jornadas_opc(jornadas_post, registros_pontos):
        jornadas_disponiveis = [
            (x[0], x[1]) for x in jornadas_post
            if not any(y[1] == 7 for y in registros_pontos if y[0] == x[0])
        ]
        return jornadas_disponiveis