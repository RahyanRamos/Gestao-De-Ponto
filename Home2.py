import streamlit as st
from pmax_back import Pmax
from conexao import conexaoBD

st.set_page_config("Gestão de Ponto", layout="wide")


@st.cache_data
def get_itinerarios():
    ponto_max = Pmax()
    dados_itinerarios = ponto_max.get_itenerarios()

    opc_itinerarios = ponto_max.set_iterarios(dados_itinerarios)

    return opc_itinerarios


def limpa_insert(insert_str):
    return str(insert_str).replace('"', "'")


st.title("Gestão de Ponto")

with st.expander("Criar Jornada"):
    col1, col2 = st.columns([2, 1])
    with col1:
        opc_itinerarios = get_itinerarios()
        itinerario = st.selectbox("Itinerário", opc_itinerarios)
    with col2:
        numVeiculo = st.text_input("Número do Veículo")
    

    col1, col2 = st.columns(2)
    with col1:
        Kms = st.text_input("Kms")
    with col2:
        numMapa = st.text_input("Número do Mapa")
    
    colAux, colButton = st.columns([4, 1])
    with colButton:
        salvar = st.button("Criar Jornada", use_container_width=True)

        check_campos = [len(str(x).strip()) for x in [numVeiculo, Kms, numMapa]]
        if salvar:
            if 0 not in check_campos:            
                
                conexao = conexaoBD()
                cursor = conexao.cursor()

                ############# TRATANDO AS INFORMAÇÕES DO ITINERÁRIO #############
                split_itiner = itinerario.split('.')
                trecho = split_itiner[1].split('(')[0]
                split_trecho_ini = str(trecho.split(' x ')[0]).strip()
                split_trecho_fim = str(trecho.split(' x ')[1]).strip()
                ############# FIM TRATAMENTO #############

                ############# CRIANDO INSERT #############
                cmd = f"""INSERT INTO pmax_getregistro(fgkey_servicolin, fgkey_motorist, matricula_motorist, name_city_ini, name_city_fim, num_veiculo, num_mapa, kms)
                            VALUES (
                                {str(split_itiner[0]).strip()},
                                679,
                                {limpa_insert(255)},
                                "{limpa_insert(split_trecho_ini)}",
                                "{limpa_insert(split_trecho_fim)}",
                                {numVeiculo},
                                {numMapa},
                                "{limpa_insert(Kms)}"
                            );"""
                
                cursor.execute(cmd)
                conexao.commit()

                cursor.close()
                conexao.close()

                st.toast('Jornada criada com sucesso!', icon='✅')

            else:
                st.toast('Por favor, preencha todos os campos corretamente!', icon='❌')



with st.expander("Registros de Ponto"):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        tpParada = st.selectbox("Tipo de Ponto", ["Entrada em Serviço", "Início da Viagem", "Intervalo", "Tempo de Espera", "Repouso no Veículo", "Término da Viagem", "Saída de Serviço"], None, placeholder="Selecione o tipo de parada")

    if tpParada:
        if tpParada in ["Entrada em Serviço", "Início da Viagem", "Término da Viagem", "Saída de Serviço"]:
            with col2:
                data = st.date_input("Data")
            with col3:
                hora = st.time_input("Hora")
        else:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                dtInicio = st.date_input("Data de Início")
            with col3:
                hrInicio = st.time_input("Hora de Início")

            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                dtFim = st.date_input("Data de Fim")
            with col3:
                hrFim = st.time_input("Hora de Fim")

        colAux, col4 = st.columns([4, 1])
        with col4:
            st.write(" ")
            st.write(" ")
            registrar = st.button("Registrar", use_container_width=True)

        html = """<div class="container-pontos">
                <div class="container-tipoParada">
                    <div class="numRegistro">
                        <p>1</p>
                    </div>
                    <div class="nomeParada">
                        <p>Entrada em Serviço</p>
                    </div>
                    <div class="container-paradas">
                        <div class="infoParada">
                            <p>25/09/2024 - 11:14</p>
                        </div>
                    </div>
                </div>
                <div class="container-tipoParada">
                    <div class="numRegistro">
                        <p>2</p>
                    </div>
                    <div class="nomeParada">
                        <p>Início da Viagem</p>
                    </div>
                    <div class="container-paradas">
                        <div class="infoParada">
                            <p>25/09/2024 - 11:20</p>
                        </div>
                    </div>
                </div>
                <div class="container-tipoParada">
                    <div class="numRegistro">
                        <p>3</p>
                    </div>
                    <div class="nomeParada">
                        <p>Intervalo</p>
                    </div>
                    <div class="container-paradas">
                        <div class="infoParada">
                            <p>Início: 25/09/2024 - 15:00</p>
                            <p>Fim: 25/09/2024 - 15:15</p>
                        </div>
                        <div class="infoParada">
                            <p>Início: 25/09/2024 - 20:40</p>
                            <p>Fim: 25/09/2024 - 20:50</p>
                        </div>
                        <div class="infoParada">
                            <p>Início: 26/09/2024 - 06:22</p>
                            <p>Fim: 26/09/2024 - 06:40</p>
                        </div>
                    </div>
                </div>
                <div class="container-tipoParada">
                    <div class="numRegistro">
                        <p>4</p>
                    </div>
                    <div class="nomeParada">
                        <p>Término da Viagem</p>
                    </div>
                    <div class="container-paradas">
                        <div class="infoParada">
                            <p>26/09/2024 - 18:00</p>
                        </div>
                    </div>
                </div>
                <div class="container-tipoParada">
                    <div class="numRegistro">
                        <p>5</p>
                    </div>
                    <div class="nomeParada">
                        <p>Saída de Serviço</p>
                    </div>
                    <div class="container-paradas">
                        <div class="infoParada">
                            <p>Data: 26/09/2024 - 18:10</p>
                        </div>
                    </div>
                </div>
            </div>"""

        css = """.container-pontos {
            display: flex;
            flex-direction: column;
            margin: 30px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .container-tipoParada {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding: 10px;
            background-color: #e9ecef;
            border-radius: 5px;
            border-left: 5px solid #007bff;
        }

        .numRegistro {
            font-weight: bold;
            font-size: 24px;
            color: #007bff;
            width: 20px;
        }

        .nomeParada {
            flex-grow: 1;
            padding-left: 15px;
        }

        .nomeParada p{
            font-weight: bold;
        }

        .infoParada {
            display: flex;
            flex-direction: column;
            width: 100%; /* Garante que a infoParada ocupe toda a largura disponível */
            font-size: 14px;
            color: #333;
            margin: 10px 0;
            /* border-bottom: solid 1px #8f8f8f; */
        }

        .container-tipoParada .infoParada p {
            display: flex; /* Garante que os parágrafos dentro de infoParada ocupem uma linha inteira */
            margin: 2px 0;
        }

        .container-tipoParada:nth-child(odd) {
            background-color: #f8f9fa;
        }

        .container-tipoParada:nth-child(even) {
            background-color: #e9ecef;
        }"""

        st.write(html, unsafe_allow_html=True)
        st.write(f"<style>{css}</style>", unsafe_allow_html=True)