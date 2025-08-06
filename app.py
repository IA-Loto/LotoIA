import io
import requests
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import tensorflow as tf
from tensorflow.keras import layers, models
import streamlit as st
import streamlit_authenticator as stauth
import toml
import random

# Configurações do Streamlit
st.set_page_config(page_title="Lotofácil IA", layout="wide")
st.title("🔮 Lotofácil IA")

secrets = toml.load("secrets.toml")
hash_da_senha = secrets["credenciais"]["senha_hash"]


# 🔐 Credenciais
credentials = {
    "usernames": {
        "LotoIA": {
            "name": "João",
            "password": hash_da_senha
        }
    }
}

# ⚙️ Autenticador
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="meu_app",
    key="abcdef",
    cookie_expiry_days=0.0417
)

st.markdown("""
        <style>
            .stButton > button {
                width: 100%;
                font-size: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

# 🧑 Tela de login
authenticator.login(location="main")

# 🔓 Verificação de login via session_state
if st.session_state.get("authentication_status"):

    st.success(f"Bem-vindo, {st.session_state['name']}!")
    authenticator.logout("Sair", "sidebar")

    # Sidebar
    st.sidebar.header("⚙️ Configurações da IA")
    prever_ultimo_jogo = st.sidebar.checkbox("🎯 Testar com o último jogo", value=True)
    num_neuronios = st.sidebar.slider("🧠 Neurônios por camada", 32, 128, 64, step=32)
    num_epocas = st.sidebar.slider("🔁 Ciclos de treino", 10, 100, 20, step=10)
    usar_dropout = st.sidebar.checkbox("🌫️ Usar Dropout", value=True)
    dados = None

    # Botão para baixar e usar automaticamente o TXT
    if st.button("⬇️ Baixar histórico da Lotofácil automaticamente"):
        dados = None
        url = "https://www.lotocerta.com.br/wp-content/uploads/resultados_com_estatisticas.txt"
        headers = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache", "Pragma": "no-cache"}
        response = requests.get(url, headers=headers)
        conteudo = response.content.decode("utf-8")

        linhas = conteudo.strip().split("\n")
        dados_completos = []

        for linha in linhas:
            partes = linha.split("\t")  # separador TAB
            if len(partes) >= 17:
                concurso = partes[0]
                data = partes[1]
                dezenas = [int(partes[i]) for i in range(2, 17)]
                dados_completos.append({
                    "concurso": concurso,
                    "data": data,
                    "dezenas": dezenas})
        # Cria o DataFrame
        if len(dados_completos) == 0:
            st.error("⚠️ Não foi possível extrair dados válidos do arquivo. Verifique a conexão ou o site.")
        else:
            dezenas = [d["dezenas"] for d in dados_completos]
            dados_csv = pd.DataFrame(dezenas, columns=[f"Bola {i}" for i in range(1, 16)])
            dados_csv = dados_csv.dropna()
            dados_csv = dados_csv.applymap(int)
            dados_completos = pd.DataFrame(dados_completos)

            # Armazena o DataFrame no session_state
            st.session_state["dados_csv"] = dados_csv
            st.session_state["dados_completos"] = dados_completos
            st.success("Histórico baixado e carregado automaticamente!")

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # # Botão 2: baixar da XLoterias com Selenium

    # if st.button("⬇️ Baixar histórico da Lotofácil (XLoterias via Selenium)"):
    #     # Configura o Chrome em modo headless
    #     options = Options()
    #     options.add_argument("--headless=new")  # Novo modo headless
    #     options.add_argument("--disable-gpu")
    #     options.add_argument("--window-size=1920,1080")
    #     options.add_argument("--no-sandbox")

    #     # Inicializa o navegador com as opções
    #     driver = webdriver.Chrome(options=options)

    #     # Acessa a página da Lotofácil
    #     driver.get("https://www.xloterias.com.br/loterias/lotofacil")

    #     # Aguarda até que o campo seja preenchido
    #     wait = WebDriverWait(driver, 20)
    #     wait.until(lambda d: d.find_element(By.ID, "txtrsListaConcursos").get_attribute("value").strip() != "")

    #     # Extrai o conteúdo da caixa de texto
    #     textarea = driver.find_element(By.ID, "txtrsListaConcursos")
    #     conteudo = textarea.get_attribute("value")

    #     # Encerra o navegador
    #     driver.quit()

    #     # Processa o conteúdo para criar o DataFrame
    #     linhas = conteudo.strip().split("\n")  
    #     dados_completos = []

    #     for linha in linhas:
    #         partes = linha.split()  # separador de espaço
    #         if len(partes) >= 17:
    #             concurso = partes[0]
    #             data = partes[1]
    #             dezenas = [int(partes[i]) for i in range(2, 17)]
    #             dados_completos.append({
    #                 "concurso": concurso,
    #                 "data": data,
    #                 "dezenas": dezenas})

    #     # Cria o DataFrame
    #     if len(dezenas) == 0:
    #         st.error("⚠️ Não foi possível extrair dados válidos da XLoterias. Verifique a conexão ou o site.")
    #     else:
    #         dezenas = [d["dezenas"] for d in dados_completos]     
    #         dados_csv = pd.DataFrame(dezenas, columns=[f"Bola {i}" for i in range(1, 16)])
    #         dados_csv = dados_csv.dropna()  
    #         dados_csv = dados_csv.applymap(int)
    #         dados_csv = dados_csv[::-1].reset_index(drop=True)
    #         dados_completos = pd.DataFrame(dados_completos)
    #         dados_completos = dados_completos[::-1].reset_index(drop=True)

    #         # Armazena o DataFrame no session_state
    #         st.session_state["dados_csv"] = dados_csv
    #         st.session_state["dados_completos"] = dados_completos
    #         st.success("Histórico extraído com sucesso da XLoterias!")

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    if "dados_csv" in st.session_state:
        dados_csv = st.session_state["dados_csv"]
        dados_completos = st.session_state.get("dados_completos", pd.DataFrame())

        max_concursos = len(dados_csv)
        limite_max = max_concursos - 1 if prever_ultimo_jogo else max_concursos

        if "qtd_jogos" not in st.session_state:
            st.session_state.qtd_jogos = min(10, limite_max)
        if "qtd_jogos_slider" not in st.session_state:
            st.session_state.qtd_jogos_slider = st.session_state.qtd_jogos
        if "qtd_jogos_input" not in st.session_state:
            st.session_state.qtd_jogos_input = st.session_state.qtd_jogos
        
            # Antes de criar os widgets, inicialize apenas se não existir
        if "qtd_jogos_preservado" not in st.session_state:
            st.session_state.qtd_jogos_preservado = st.session_state.qtd_jogos  # valor padrão

        # Ajuste o preservado, se necessário
        if st.session_state.qtd_jogos_preservado > limite_max:
            st.session_state.qtd_jogos_preservado = limite_max
            st.session_state.qtd_jogos_input = st.session_state.qtd_jogos_preservado
            st.session_state.qtd_jogos_slider = st.session_state.qtd_jogos_preservado
        else:
            st.session_state.qtd_jogos_input = st.session_state.qtd_jogos_preservado
            st.session_state.qtd_jogos_slider = st.session_state.qtd_jogos_preservado

        def sync_slider():
            st.session_state.qtd_jogos_input = st.session_state.qtd_jogos_slider
            st.session_state.qtd_jogos_preservado = st.session_state.qtd_jogos_slider

        def sync_input():
            st.session_state.qtd_jogos_slider = st.session_state.qtd_jogos_input
            st.session_state.qtd_jogos_preservado = st.session_state.qtd_jogos_input

        # Remova o parâmetro value dos widgets!
        st.sidebar.slider(
            "📊 Quantidade de concursos analisados",
            min_value=1,
            max_value=limite_max,
            step=5,
            key="qtd_jogos_slider",
            on_change=sync_slider
        )

        st.sidebar.number_input(
            "Digite a quantidade:",
            min_value=1,
            max_value=limite_max,
            step=1,
            format="%d",
            key="qtd_jogos_input",
            on_change=sync_input
        )

        # Use sempre a mesma variável
        qtd_jogos = st.session_state.qtd_jogos_input

        # Se marcar a opção, removemos o último jogo
        if prever_ultimo_jogo:
            dados_para_treino = dados_csv.tail(qtd_jogos + 1).reset_index(drop=True)
            info_dados_para_treino = dados_completos.tail(qtd_jogos + 1).reset_index(drop=True)
            jogo_real = dados_para_treino.iloc[-1]  # Último jogo real (para comparar)
            info_jogo_real = info_dados_para_treino.iloc[-1]  # Informações do último jogo real
            concurso = info_jogo_real.iloc[0]
            data = info_jogo_real.iloc[1]

            # Exibe o último concurso  
            st.markdown('<div style="margin-bottom: 0.2rem;"><strong>🎯 Último concurso a ser previsto:</strong></div>', unsafe_allow_html=True)
            dados_exibicao = pd.DataFrame([jogo_real.values], columns=jogo_real.index)
            dados_exibicao = dados_exibicao.applymap(lambda x: f"{int(x):02d}")

            dados_exibicao.index = ["Último Concurso"]
            st.markdown(
                f"""
                <div style="border:1px solid #ddd; padding:10px; margin:10px 0; border-radius:8px;
                        background-color:#E0FFFF; font-size:12px;">
                    Concurso: <strong>{concurso}</strong> &nbsp&nbsp&nbsp Data: <strong>{data}</strong></span><br>
                    {" | ".join(dados_exibicao.iloc[0].tolist())}
                </div>
                """,
                unsafe_allow_html=True
            )

            dados = dados_para_treino.iloc[:-1].reset_index(drop=True)  # dados sem o último jogo
            info_dados = info_dados_para_treino.iloc[:-1].reset_index(drop=True)  # informações sem o último jogo
        else:
            dados = dados_csv.tail(qtd_jogos).reset_index(drop=True)
            info_dados = dados_completos.tail(qtd_jogos).reset_index(drop=True)

        # 📋 Últimos concursos como cards
        st.markdown('<div style="margin-bottom: 0.2rem;">📋 Últimos concursos analisados:</div>', unsafe_allow_html=True)

        dados_exibicao = dados.tail(3).copy()[::-1].reset_index(drop=True)
        info_dados_exibicao = info_dados.tail(3).copy()[::-1].reset_index(drop=True)
        dados_exibicao.index = [f"Concurso {i+1}" for i in range(len(dados_exibicao))]
        dados_exibicao = dados_exibicao.applymap(lambda x: f"{int(x):02d}")

        # Itera pelos concursos e exibe em colunas
        for i in range(len(dados_exibicao)):
            dezenas = dados_exibicao.iloc[i].tolist()
            concurso = info_dados_exibicao.iloc[i, 0]  # Nome do concurso
            data = info_dados_exibicao.iloc[i, 1]  # Data do concurso
            
            with st.container():
                st.markdown(
                    f"""
                    <div style="border:1px solid #ddd; padding:10px; margin:10px 0; border-radius:8px;
                                background-color:#f9f9f9; font-size:12px;">
                        Concurso: <strong>{concurso}</strong> &nbsp&nbsp&nbsp Data: <strong>{data}</strong></span><br>
                        {" | ".join(dezenas)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        # Converte os dados para binários        
        def linha_binaria(linha):
                binario = [0]*25
                for num in linha:
                    if pd.notna(num) and 1 <= int(num) <= 25:
                        binario[int(num)-1] = 1
                return binario

        binarios = [linha_binaria(row) for row in dados.values]
        X = np.array(binarios[:-1]).reshape(-1, 1, 25)
        y = np.array(binarios[1:])

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    
    if st.button("🍀 Dezenas mais frequentes 🍀"):
        if dados is not None:
            # 🔢 Frequência das dezenas
            todas_dezenas = dados.values.flatten()
            contagem = pd.Series(todas_dezenas).value_counts().sort_values(ascending=False)

            # 📋 Jogo 1: 15 dezenas mais frequentes
            top_dezenas = contagem.index.tolist()  # todas ordenadas por frequência
            jogo_base = sorted(top_dezenas[:15])   # Jogo 1: top 15
            todos_os_jogos = [jogo_base]

            # 🧠 Identifica as 3 menos frequentes dentro do jogo_base
            menos_frequentes = sorted(jogo_base, key=lambda d: contagem[d])[:5]

            # 🎯 Jogo 2: substitui pelas 16ª, 17ª, 18ª, 19ª e 20ª mais frequentes
            substitutas_2 = [d for d in top_dezenas[15:20] if d not in jogo_base]
            jogo_2 = [d for d in jogo_base if d not in menos_frequentes] + substitutas_2
            jogo_2 = sorted(jogo_2)
            todos_os_jogos.append(jogo_2)

            # 🎯 Jogo 3: substitui pelas 21ª, 22ª, 23ª, 24ª e 25ª mais frequentes
            substitutas_3 = [d for d in top_dezenas[20:25] if d not in jogo_base]
            jogo_3 = [d for d in jogo_base if d not in menos_frequentes] + substitutas_3
            jogo_3 = sorted(jogo_3)
            todos_os_jogos.append(jogo_3)

            # 🎨 Exibição dos jogos
            st.markdown("📋 Jogos com dezenas mais frequentes:")
            for i, jogo in enumerate(todos_os_jogos, start=1):
                dezenas_formatadas = [f"{n:02d}" for n in jogo]
                st.markdown(
                    f"""
                    <div style="border:1px solid #ddd; padding:10px; margin:10px 0; border-radius:8px;
                                background-color:#eaf4ff; font-size:12px;">
                        <strong>Jogo {i}</strong><br>
                        {" | ".join(dezenas_formatadas)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # 🎯 Comparação com referência
            if prever_ultimo_jogo:
                referencia = jogo_real.values
                origem = "último concurso real"
            else:
                referencia = dados.iloc[-1].values
                origem = "último jogo da lista analisada"

            # 🟢 Mostra acertos de cada jogo
            for i, jogo in enumerate(todos_os_jogos, start=1):
                acertos = len(set(jogo) & set(referencia))
                st.success(f"✅ Jogo {i}: {acertos} acertos em comparação ao {origem}")

        else:
            st.warning("⚠️ Carregue o histórico de sorteios antes.")

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # Botão para LSTM

    # Slider logo abaixo do botão (sempre visível)
    qtde_fixas = st.slider(
        "🔒 Fixar dezenas mais frequentes:",
        min_value=1, max_value=8, value=4
    )    

    usar_selecao_manual = st.checkbox("Selecionar dezenas fixas manualmente")

    dezenas_fixas_manualmente = []

    if usar_selecao_manual:
        st.markdown("Selecione até 8 dezenas fixas:")
        selected = []
        cols = st.columns(5)

        for i in range(25):
            col = cols[i % 5]
            with col:
                checked = st.checkbox(f"{i+1:02d}", key=f"fixa_{i+1}")
                if checked:
                    selected.append(i + 1)

        if len(selected) > 8:
            st.error("⚠️ Você só pode selecionar até 8 dezenas.")
        else:
            dezenas_fixas_manualmente = sorted(selected)


    if st.button("🍀 Dezenas fixas + IA (LSTM) 🍀"):
        if dados is not None:
            
            # Cálculo das 10 dezenas mais frequentes
            frequencias = pd.Series([num for linha in dados.values for num in linha]).value_counts()
            top_frequentes = frequencias.head(10).index.tolist()

            # Seleciona as N mais frequentes
            if usar_selecao_manual and len(dezenas_fixas_manualmente) <= 8:
                dezenas_fixas = dezenas_fixas_manualmente
            else:
                dezenas_fixas = sorted(top_frequentes[:qtde_fixas])  # do slider

            # Quantas dezenas a IA precisa prever por jogo
            qtd_prevista_por_jogo = 15 - qtde_fixas
            if qtd_prevista_por_jogo <= 0:
                st.error("Você selecionou dezenas fixas demais. Cada jogo precisa ter exatamente 15 dezenas.")
                st.stop()

            # Exibir as dezenas fixas no mesmo estilo dos jogos
            fixas_formatadas = [f"{dez:02d}" for dez in dezenas_fixas]

            st.markdown(
                f"""
                <div style="border:1px solid #ddd; padding:10px; margin:10px 0; border-radius:8px;
                            background-color:#eaf4ff; font-size:12px;">
                    <strong>🔒 Dezenas fixas usadas</strong><br>
                    {" | ".join(fixas_formatadas)}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader("⚙️ Treinando IA (LSTM)...")
            progress_bar = st.progress(0)
            status_text = st.empty()

            model = models.Sequential()
            model.add(layers.LSTM(num_neuronios, return_sequences=True, input_shape=(1, 25)))
            if usar_dropout:
                model.add(layers.Dropout(0.3))
            model.add(layers.LSTM(num_neuronios))
            if usar_dropout:
                model.add(layers.Dropout(0.3))
            model.add(layers.Dense(25, activation="sigmoid"))

            model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

            for epoch in range(num_epocas):
                model.fit(X, y, epochs=1, verbose=0)
                progresso = (epoch + 1) / num_epocas
                progress_bar.progress(progresso)
                status_text.text(f"⏳ Treinando ciclo {epoch + 1} de {num_epocas}...")

            status_text.text("✅ Treinamento concluído!")
            st.session_state["modelo"] = model
            st.session_state["binarios"] = binarios
            st.session_state["dados_ia"] = dados

            entrada = np.array([binarios[-1]]).reshape(1, 1, 25)
            predicao = model.predict(entrada)[0]

            indices_prob = np.argsort(predicao)[::-1]  # Índices dos números mais prováveis (do maior ao menor)

            # Previsão da IA
            entrada = np.array([binarios[-1]]).reshape(1, 1, 25)
            predicao = model.predict(entrada)[0]

            # Ordenar os índices das dezenas por probabilidade (exceto as já fixas)
            indices_prob = np.argsort(predicao)[::-1]
            # Seleciona as melhores 20 dezenas previstas que não estão nas fixas
            dezenas_previstas = [i + 1 for i in indices_prob if (i + 1) not in dezenas_fixas][:20]
            
            # Valida se há dezenas suficientes
            if len(dezenas_previstas) < qtd_prevista_por_jogo:
                dezenas_previstas *= (qtd_prevista_por_jogo // len(dezenas_previstas) + 1)
                dezenas_previstas = dezenas_previstas[:qtd_prevista_por_jogo]

            # Garante pelo menos 5 dezenas diferentes entre cada par de jogos
            def diversidade_suficiente(j1, j2, j3):
                return (
                    len(set(j1) ^ set(j2)) >= 3 and
                    len(set(j1) ^ set(j3)) >= 3 and
                    len(set(j2) ^ set(j3)) >= 3
                )

            # Monta os 3 jogos garantindo diversidade mínima
            tentativas = 0
            max_tentativas = 1000
            while tentativas < max_tentativas:
                jogo1_var = random.sample(dezenas_previstas, qtd_prevista_por_jogo)
                jogo2_var = random.sample(dezenas_previstas, qtd_prevista_por_jogo)
                jogo3_var = random.sample(dezenas_previstas, qtd_prevista_por_jogo)

                jogo1 = sorted(dezenas_fixas + jogo1_var)
                jogo2 = sorted(dezenas_fixas + jogo2_var)
                jogo3 = sorted(dezenas_fixas + jogo3_var)

                if diversidade_suficiente(jogo1, jogo2, jogo3):
                    break

                tentativas += 1
            else:
                st.warning("Não foi possível gerar 3 jogos com diversidade mínima. Mostrando os últimos gerados.")

            # Formatação e exibição
            jogos = [jogo1, jogo2, jogo3]
            jogos_formatados = [[f"{dezena:02d}" for dezena in jogo] for jogo in jogos]

            st.markdown('<div style="margin-bottom: 0.2rem;">📋 Jogos sugeridos pela IA (LSTM):</div>', unsafe_allow_html=True)
            for i, dezenas in enumerate(jogos_formatados, 1):
                st.markdown(
                    f"""
                    <div style="border:1px solid #ddd; padding:10px; margin:10px 0; border-radius:8px;
                                background-color:#eaf4ff; font-size:12px;">
                        <strong>Sugestão {i}</strong><br>
                        {" | ".join(dezenas)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Verifica os acertos com o último jogo real (caso esteja ativado)
            if prever_ultimo_jogo:
                dezena_real = list(jogo_real.values)
                dezena_real_set = set(dezena_real)
                for i, jogo in enumerate([jogo1, jogo2, jogo3], 1):
                    acertos = len(set(jogo) & dezena_real_set)
                    st.write(f"✅ Sugestão {i}: {acertos} acertos com o último jogo real")

        else:
            st.warning("⚠️ Carregue o histórico de sorteios antes.")

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # Validação histórica com barra de progresso LSTM
    # if st.button("📊 Validar LSTM com histórico (≥13 acertos)"):
    #     model = st.session_state.get("modelo")
    #     binarios = st.session_state.get("binarios")

    #     if model and binarios:
    #         progress_bar = st.progress(0)
    #         status_text = st.empty()
    #         total = len(binarios) - 2
    #         acertos_lista = []

    #         for i in range(total):
    #             entrada_hist = np.array([binarios[i]]).reshape(1, 1, 25)
    #             real = binarios[i + 1]
    #             predito_hist = model.predict(entrada_hist)[0]
    #             dezenas_preditas = np.argsort(predito_hist)[-15:]
    #             dezenas_reais = [idx for idx, val in enumerate(real) if val == 1]
    #             acertos = len(set(dezenas_preditas) & set(dezenas_reais))
    #             if acertos >= 13:
    #                 acertos_lista.append(acertos)

    #             progresso = (i + 1) / total
    #             progress_bar.progress(progresso)
    #             status_text.text(f"📊 Validando concurso {i + 1} de {total}...")

    #         status_text.text("✅ Validação concluída!")

    #         if acertos_lista:
    #             media = np.mean(acertos_lista)
    #             st.subheader("📈 Validação Histórica")
    #             st.write(f"Média de acertos (≥13): **{media:.2f}**")

    #             # Cria DataFrame para o gráfico
    #             df_acertos = pd.DataFrame({
    #                 "Concurso": list(range(1, len(acertos_lista) + 1)),
    #                 "Acertos": acertos_lista
    #             })

    #             # Gráfico com linha e pontos
    #             chart = alt.Chart(df_acertos).mark_line(point=True).encode(
    #                 x=alt.X("Concurso", title="Concurso", axis=alt.Axis(tickMinStep=1)),
    #                 y=alt.Y("Acertos", title="Quantidade de acertos",
    #                         scale=alt.Scale(domain=[0, 15]),
    #                         axis=alt.Axis(values=list(range(0, 16)), tickCount=16))
    #             ).properties(
    #                 width=700,
    #                 height=400,
    #                 title="Desempenho da IA por concurso"
    #             )

    #             st.altair_chart(chart, use_container_width=True)

    #         else:
    #             st.warning("Nenhum concurso teve 13 ou mais acertos com a IA atual.")
    #     else:
    #         st.warning("⚠️ Execute a previsão da IA antes de validar o histórico.")

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # Botão para ensemble CNN + LSTM
    if st.button("🍀 Prever jogo com IA (CNN + LSTM) 🍀"):
        if dados is not None:
            st.subheader("⚙️ Treinando IA (CNN + LSTM)...")
            progress_bar = st.progress(0)
            status_text = st.empty()

            model_ensemble = models.Sequential()
            model_ensemble.add(layers.Conv1D(filters=64, kernel_size=1, activation='relu', input_shape=(1, 25)))
            model_ensemble.add(layers.MaxPooling1D(pool_size=1))
            model_ensemble.add(layers.LSTM(num_neuronios))
            if usar_dropout:
                model_ensemble.add(layers.Dropout(0.3))
            model_ensemble.add(layers.Dense(25, activation="sigmoid"))

            model_ensemble.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

            for epoch in range(num_epocas):
                model_ensemble.fit(X, y, epochs=1, verbose=0)
                progresso = (epoch + 1) / num_epocas
                progress_bar.progress(progresso)
                status_text.text(f"⏳ Treinando ciclo {epoch + 1} de {num_epocas}...")

            status_text.text("✅ Treinamento concluído!")
            st.session_state["modelo_ensemble"] = model_ensemble
            st.session_state["binarios"] = binarios
            st.session_state["dados_ia"] = dados


            entrada = np.array([binarios[-1]]).reshape(1, 1, 25)
            predicao = model_ensemble.predict(entrada)[0]

            indices_prob = np.argsort(predicao)[::-1]  # Índices dos números mais prováveis (do maior ao menor)
            
            # Gerar 3 conjuntos com variações forçadas
            jogo1 = sorted([i+1 for i in indices_prob[:15]])
            jogo2 = sorted([i+1 for i in indices_prob[3:18]])  # desloca um pouco
            jogo3 = sorted([i+1 for i in indices_prob[5:20]])  # desloca mais

            # Verificar diferença mínima entre os conjuntos
            def diferenca_minima(j1, j2):
                return len(set(j1) ^ set(j2)) >= 3
            
            while not (diferenca_minima(jogo1, jogo2) and diferenca_minima(jogo1, jogo3) and diferenca_minima(jogo2, jogo3)):
                indices_prob = np.roll(indices_prob, 1)  # Rotaciona levemente os índices para gerar novas combinações

                jogo1 = sorted([i+1 for i in indices_prob[:15]])
                jogo2 = sorted([i+1 for i in indices_prob[3:18]])
                jogo3 = sorted([i+1 for i in indices_prob[5:20]])   

            # Exibe os jogos
            jogos = [jogo1, jogo2, jogo3]  # Cada um com 15 dezenas
            jogos_formatados = [[f"{dezena:02d}" for dezena in jogo] for jogo in jogos]

            df_jogos = pd.DataFrame(jogos_formatados)  # Cada linha = um jogo
            df_jogos.index = ["Sugestão 1", "Sugestão 2", "Sugestão 3"]
            df_jogos.columns = [f"Bola {i+1}" for i in range(15)]  # Nome das colunas

            st.markdown('<div style="margin-bottom: 0.2rem;">📋 Jogos sugeridos pela IA (CNN + LSTM):</div>', unsafe_allow_html=True)
            for i, dezenas in enumerate(jogos_formatados, 1):
                st.markdown(
                    f"""
                    <div style="border:1px solid #ddd; padding:10px; margin:10px 0; border-radius:8px;
                                background-color:#eaf4ff; font-size:12px;">
                        <strong>Sugestão {i}</strong><br>
                        {" | ".join(dezenas)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if prever_ultimo_jogo:
                # Verifica o último jogo real
                dezena_real = list(jogo_real.values)  # valores do último jogo
                dezena_real_set = set(dezena_real)

                for i, jogo in enumerate([jogo1, jogo2, jogo3], 1):
                    acertos = len(set(jogo) & dezena_real_set)
                    st.write(f"✅ Sugestão {i}: {acertos} acertos com o último jogo real")
                
        else:
            st.warning("⚠️ Carregue o histórico de sorteios antes.")

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # Validação histórica com barra de progresso CNN + LSTM
    # if st.button("📊 Validar CNN + LSTM com histórico (≥13 acertos)"):
    #     model_ensemble = st.session_state.get("modelo_ensemble")
    #     binarios = st.session_state.get("binarios")

    #     if model_ensemble and binarios:
    #         progress_bar = st.progress(0)
    #         status_text = st.empty()
    #         total = len(binarios) - 2
    #         acertos_lista_ensemble = []

    #         for i in range(total):
    #             entrada_hist = np.array([binarios[i]]).reshape(1, 1, 25)
    #             real = binarios[i + 1]
    #             predito_hist = model_ensemble.predict(entrada_hist)[0]
    #             dezenas_preditas = np.argsort(predito_hist)[-15:]
    #             dezenas_reais = [idx for idx, val in enumerate(real) if val == 1]
    #             acertos = len(set(dezenas_preditas) & set(dezenas_reais))
    #             if acertos >= 13:
    #                 acertos_lista_ensemble.append(acertos)

    #             progresso = (i + 1) / total
    #             progress_bar.progress(progresso)
    #             status_text.text(f"📊 Validando Combinação no concurso {i + 1} de {total}...")

    #         status_text.text("✅ Validação Combinação concluída!")

    #         if acertos_lista_ensemble:
    #             media = np.mean(acertos_lista_ensemble)
    #             st.subheader("📈 Validação Histórica (Combinação)")
    #             st.write(f"Média de acertos (≥13): **{media:.2f}**")
    #             st.bar_chart(acertos_lista_ensemble)
    #         else:
    #             st.warning("Nenhum concurso teve ≥13 acertos com a IA Combinação atual.")
    #     else:
    #         st.warning("⚠️ Execute a previsão com o Ensemble antes de validar seu histórico.")

elif st.session_state.get("authentication_status") is False:
    st.error("Usuário ou senha incorretos.")
    
elif st.session_state.get("authentication_status") is None:
    st.warning("Por favor, faça login para continuar.")