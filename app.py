import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(page_title="Análise Climática", layout="wide")

# Carregar os dados
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/DarleneSouza/Trabalho_Final/main/previsoes_tempo%20(1).csv")
    df["Data"] = pd.to_datetime(df["Data"])
    return df



df = load_data()

# === Função para gerar histórias de clima ===
def generate_stories(df):
    stories = []
    for _, row in df.iterrows():
        story = ""

        if row["Temp_Max"] > 30:
            if row["Condicao"] in ["Chuva", "Chuva forte", "Chuva com trovoada", "Períodos de chuva", "Chuvas e trovoadas ocasionais"]:
                story = f"Hoje, {row['Cidade']} está muito quente, com grandes chances de chuva, tornando o dia desconfortável."
            elif row["Condicao"] in ["Nevoeiro", "Nublado", "Nebulosidade variável"]:
                story = f"Em {row['Cidade']}, o calor excessivo combinado com o tempo nublado pode tornar o clima abafado e desconfortável."
            elif row["Condicao"] == "Maioritariamente nublado":
                story = f"Em {row['Cidade']}, o calor excessivo combinado com um céu predominantemente nublado pode tornar o clima abafado."
            else:
                story = f"Hoje, {row['Cidade']} está bastante quente, ideal para atividades externas."

        elif 18 <= row["Temp_Max"] <= 26:
            if row["Condicao"] in ["Chuva", "Chuva forte", "Chuva com trovoada", "Períodos de chuva", "Chuvas e trovoadas ocasionais"]:
                story = f"{row['Cidade']} tem uma temperatura agradável, mas a chuva pode atrapalhar atividades ao ar livre."
            elif row["Condicao"] in ["Nublado", "Nebulosidade variável"]:
                story = f"{row['Cidade']} tem uma temperatura agradável, mas o céu nublado pode tornar as caminhadas menos agradáveis."
            elif row["Condicao"] == "Maioritariamente com sol":
                story = f"{row['Cidade']} tem um clima perfeito para atividades ao ar livre, com predominância de sol."
            elif row["Condicao"] in ["Ventos fortes", "Tempestade com ventos fortes"]:
                story = f"{row['Cidade']} tem uma temperatura confortável, mas ventos fortes tornam as atividades ao ar livre mais difíceis."
            else:
                story = f"{row['Cidade']} tem um clima perfeito para caminhadas ao ar livre."

        elif row["Temp_Max"] < 18:
            if row["Condicao"] in ["Chuva", "Chuva forte", "Períodos de chuva"]:
                story = f"Em {row['Cidade']}, a temperatura baixa e a chuva forte tornam o dia desconfortável e pouco propício para atividades ao ar livre."
            elif row["Condicao"] == "Neve":
                story = f"{row['Cidade']} está com temperatura baixa e neve, tornando o clima ideal para quem gosta de atividades de inverno."
            elif row["Condicao"] in ["Nublado", "Maioritariamente nublado"]:
                story = f"A temperatura está fria em {row['Cidade']}, e o céu nublado faz o dia parecer ainda mais gelado."
            else:
                story = f"{row['Cidade']} tem um clima ameno, ótimo para relaxar em ambientes fechados."

        elif row["Condicao"] in ["Tempestade", "Neve", "Granizo"]:
            story = f"Em {row['Cidade']}, condições climáticas extremas, como {row['Condicao']}, tornam o dia mais difícil."

        elif row["Condicao"] in ["Ventos fortes", "Tempestade com ventos fortes"]:
            story = f"Os ventos fortes em {row['Cidade']} tornam o clima mais intenso, ideal para se proteger em ambientes fechados."
        elif row["Condicao"] == "Nevoeiro":
            story = f"Nevoeiro em {row['Cidade']} pode dificultar a visibilidade, cuidado nas estradas."
        elif row["Condicao"] in ["Trovoada em partes da zona", "Aguaceiro ou trovoada"]:
            story = f"Em {row['Cidade']}, a trovoada em partes da zona pode trazer chuvas e ventos fortes em algumas áreas."

        # 🔹 Se nenhuma condição for atendida, cria uma história genérica
        if not story:
            story = f"O clima em {row['Cidade']} hoje é {row['Condicao']}, com temperatura máxima de {row['Temp_Max']}°C."

        stories.append(story)

    return stories


# === Tratamento dos dados antes de chamar a função ===
df_filtered = df.copy()  # Criar uma cópia dos dados originais
df_filtered['Data'] = pd.to_datetime(df_filtered['Data'], errors='coerce')  # Garantir que a data está correta
df_filtered['Data'] = df_filtered['Data'].dt.strftime('%Y-%m-%d')  # Converter para string no formato correto

# Gerando as histórias climáticas
df_filtered['História Climática'] = generate_stories(df_filtered)

# # Exibindo a tabela interativa com as histórias
# st.subheader("📅 Tabela de Dados Climáticos por Data e Cidade")
# st.dataframe(df_filtered[['Data', 'Cidade', 'Temp_Max', 'Temp_Min', 'Precipitacao', 'Condicao', 'História Climática']], use_container_width=True)


# === Barra Lateral ===
st.sidebar.header('Configurações', divider='blue')

data_expander = st.sidebar.expander(label="# **Dados Tabulares**", icon=":material/table:")
with data_expander:
    # Formulário dos filtros
    with st.form("settings_form", clear_on_submit=False):
        explain_data = st.checkbox("Significado dos Dados")
        data_in_table = st.checkbox("Exibir Tabela de Dados")
        data_described = st.checkbox("Resumir Dados")
        show_stories = st.checkbox('Exibir Histórias Climática')
        
        # Todo form precisa de um botão de submit, que guarda se ele foi submetido ou não
        settings_form_submitted = st.form_submit_button("Carregar")

graph_expander = st.sidebar.expander("# **Gráficos**", icon=":material/monitoring:")
# st.sidebar.subheader('Gráficos')
with graph_expander:
    # Formulário dos gráficos
    with st.form("graphs_form", clear_on_submit=False):
        evolucao_temp_max = st.checkbox("Evolução da Temp_Max ao longo do tempo por cidade")
        evolucao_temp_min = st.checkbox("Evolução da Temp_Min ao longo do tempo por cidade")
        corr_precipitacao_data = st.checkbox("Correlação Precipitação por Cidade e Data")
        corr_temp_max_data = st.checkbox("Correlação Temp_Max por Cidade e Data")
        corr_temp_min_data = st.checkbox("Correlaçao Temp_Min por Cidade e Data")
        temp_max_por_condicao = st.checkbox("Temperatura Máxima por Cidade e Condição")
        temp_min_por_condicao = st.checkbox("Temperatura Mínima por Cidade e Condição")
        precipitacao_por_condicao = st.checkbox("Precipitação por Cidade e Condição")
        media_temp_min = st.checkbox("Média de Temp_Min por Data e Cidade")
        media_temp_max = st.checkbox("Média de Temp_Max por Data e Cidade")
        media_precipitacao = st.checkbox("Média de Precipitação por Data e por Cidade")

        graphs_form_submitted = st.form_submit_button("Gerar")



# === Página Principal ===
st.header("📊 Análise de Dados Meteorológicos", divider='blue')

# Um markdown de múltiplas linhas
data_meaning = '''

- `Variável`: Significado

- `Cidade`:Nome da cidade para a qual a previsão do tempo foi coletada.
- `Data`: Data da previsão meteorológica no formato dd/mm/aaaa.
- `Dia`: Nome do dia da semana correspondente à previsão (exemplo: "Segunda-feira").
- `Temp Max`: Temperatura máxima prevista para o dia (geralmente em graus Celsius).
- `Temp Min`: Temperatura mínima prevista para o dia (geralmente em graus Celsius).
- `Condição`: Descrição do clima esperado (exemplo: "Ensolarado", "Chuva moderada", "Nublado").
- `Precipitação`: Probabilidade de chuva ou quantidade de precipitação esperada (normalmente em porcentagem % ou milímetros mm).
'''



# Ao submeter o form de dados tabulares
if settings_form_submitted:
    if explain_data:
        st.subheader("Dicionário dos Dados", divider="gray")
        st.markdown(data_meaning)
    
    if data_in_table:
        st.subheader("Tabela da Dados", divider="gray")
        st.write(df)
    
    if data_described:
        st.subheader("Resumo dos Dados", divider="gray")
        st.write(df.describe())

    if show_stories:  # Corrigida a verificação
        # Certificar-se de que `df_filtered` existe antes de usar
        if 'df_filtered' in locals() and not df_filtered.empty:
            df_filtered["História Climática"] = generate_stories(df_filtered)  # Chamada correta da função
        
            st.subheader("📖 Histórias Climáticas", divider="gray")
            st.dataframe(df_filtered[['Data', 'Cidade', 'História Climática']], use_container_width=True)  # Exibir apenas as histórias
        else:
            st.warning("⚠️ Nenhum dado disponível para gerar histórias.")

# Ao submeter o form de gráficos

# # Seleção de cidades

graphs_form_submitted = True
cidades_selecionadas = st.multiselect("Selecione as cidades:", df["Cidade"].unique(), default=list(df["Cidade"].unique()))
df_filtered = df[df["Cidade"].isin(cidades_selecionadas)]

if graphs_form_submitted:
    if evolucao_temp_max:
        st.subheader("Evolução da Temp_Max ao longo do tempo por cidade", divider="gray")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=df_filtered, x="Data", y="Temp_Max", hue="Cidade", marker="o", ax=ax)
        plt.title("Evolução da Temperatura Máxima")
        plt.xlabel("Data")
        plt.ylabel("Temp Max (°C)")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        

if graphs_form_submitted:
    if evolucao_temp_min:
        st.subheader("Evolução da Temp_Min ao longo do tempo por cidade", divider="gray")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=df_filtered, x="Data", y="Temp_Min", hue="Cidade", marker="o", linestyle="dashed", ax=ax)
        plt.title("Evolução da Temperatura Mínima")
        plt.xlabel("Data")
        plt.ylabel("Temp Min (°C)")
        plt.xticks(rotation=45)
        st.pyplot(fig)


if graphs_form_submitted:
    if corr_precipitacao_data:
        st.subheader("Correlação Precipitação por Cidade e Data", divider="gray")
        
        df_pivot_precip = df_filtered.pivot_table(values="Precipitacao", index="Cidade", columns="Data", aggfunc="mean")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(df_pivot_precip, annot=True, cmap="Blues", fmt=".1f", ax=ax)
        plt.title("Precipitação por Cidade e Data")

        plt.xticks(
            ticks=range(len(df_pivot_precip.columns)),  # Define as posições dos rótulos no eixo X
            labels=[str(date).split()[0] for date in df_pivot_precip.columns],  # Converte para string e remove a hora
            rotation=45  # Rotaciona os rótulos para melhor visualização
        )

        st.pyplot(fig)


if graphs_form_submitted:
    if corr_temp_max_data:
        st.subheader("Correlação Temp_Max por Cidade e Data", divider="gray")
        
        df_pivot_max = df_filtered.pivot_table(values="Temp_Max", index="Cidade", columns="Data", aggfunc="mean")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(df_pivot_max, annot=True, cmap="coolwarm", fmt=".1f", ax=ax)
        plt.title("Temperatura Máxima por Cidade e Data")

        plt.xticks(
            ticks=range(len(df_pivot_max.columns)),  # Define as posições dos rótulos no eixo X
            labels=[str(date).split()[0] for date in df_pivot_max.columns],  # Converte para string e remove a hora
            rotation=45  # Rotaciona os rótulos para melhor visualização
        )

        st.pyplot(fig)


if graphs_form_submitted:
    if corr_temp_min_data:
        st.subheader("Correlação Temp_Min por Cidade e Data", divider="gray")

        df_pivot_min = df_filtered.pivot_table(values="Temp_Min", index="Cidade", columns="Data", aggfunc="mean")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(df_pivot_min, annot=True, cmap="coolwarm", fmt=".1f", ax=ax)
        plt.title("Temperatura Mínima por Cidade e Data")

        plt.xticks(
            ticks=range(len(df_pivot_min.columns)),  # Define as posições dos rótulos no eixo X
            labels=[str(date).split()[0] for date in df_pivot_min.columns],  # Converte para string e remove a hora
            rotation=45  # Rotaciona os rótulos para melhor visualização
        )

        st.pyplot(fig)
        

if graphs_form_submitted:
    if temp_max_por_condicao:
        st.subheader("Temperatura Máxima por Cidade e Condição", divider="gray")

        df_grouped = df_filtered.groupby(["Cidade", "Condicao"], as_index=False)[["Temp_Max", "Temp_Min", "Precipitacao"]].mean()
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_grouped, x="Cidade", y="Temp_Max", hue="Condicao", palette="viridis", ax=ax)
        plt.title("Temperatura Máxima por Cidade e Condição")
        st.pyplot(fig)

if graphs_form_submitted:
    if temp_min_por_condicao:
        st.subheader("Temperatura Mínima por Cidade e Condição", divider="gray")
        
        df_grouped = df_filtered.groupby(["Cidade", "Condicao"], as_index=False)[["Temp_Max", "Temp_Min", "Precipitacao"]].mean()
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_grouped, x="Cidade", y="Temp_Min", hue="Condicao", palette="viridis", ax=ax)
        plt.title("Temperatura Mínima por Cidade e Condição")
        st.pyplot(fig)

if graphs_form_submitted:
    if precipitacao_por_condicao:
        st.subheader("Precipitação por Cidade e Condição", divider="gray")
        
        df_grouped = df_filtered.groupby(["Cidade", "Condicao"], as_index=False)[["Temp_Max", "Temp_Min", "Precipitacao"]].mean()
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_grouped, x="Cidade", y="Precipitacao", hue="Condicao", palette="viridis", ax=ax)
        plt.title("Precipitação por Cidade e Condição")
        st.pyplot(fig)

if graphs_form_submitted:
    if media_temp_min:
        st.subheader("Média de Temp_Min por Data e Cidade", divider="gray")

        df_pivot = df_filtered.pivot_table(values=["Temp_Max", "Temp_Min", "Precipitacao"], index=["Data", "Cidade"], aggfunc="mean").reset_index()
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_pivot, x="Data", y="Temp_Min", hue="Cidade", palette="tab10", ax=ax)
        plt.title("Média de Temp Min por Data e Cidade")
        plt.xticks(rotation=45)
        st.pyplot(fig)

if graphs_form_submitted:
    if media_temp_max:
        st.subheader("Média de Temp_Max por Data e Cidade", divider="gray")

        df_pivot = df_filtered.pivot_table(values=["Temp_Max", "Temp_Min", "Precipitacao"], index=["Data", "Cidade"], aggfunc="mean").reset_index()
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_pivot, x="Data", y="Temp_Max", hue="Cidade", palette="tab10", ax=ax)
        plt.title("Média de Temp Max por Data e Cidade")
        plt.xticks(rotation=45)
        st.pyplot(fig)

if graphs_form_submitted:
    if media_precipitacao:
        st.subheader("Média Precipitação por Data e Cidade", divider="gray")

        df_pivot = df_filtered.pivot_table(values=["Temp_Max", "Temp_Min", "Precipitacao"], index=["Data", "Cidade"], aggfunc="mean").reset_index()
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_pivot, x="Data", y="Precipitacao", hue="Cidade", palette="tab10", ax=ax)
        plt.title("Média de Precipitação por Data e Cidade")
        plt.xticks(rotation=45)
        st.pyplot(fig)

