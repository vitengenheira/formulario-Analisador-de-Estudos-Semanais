# 📦 Importando as bibliotecas necessárias
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import os

# 📊 Função que gera o gráfico (com cache)
@st.cache_data
def gerar_grafico(dias, horas):
    fig, ax = plt.subplots()
    ax.bar(dias, horas, color='skyblue')
    ax.set_ylabel('Horas Estudadas')
    ax.set_title('Estudos da Semana')
    ax.set_ylim(0, 12)
    return fig

# 📄 Função que cria o PDF (sem cache pois salva arquivos)
def gerar_pdf(nome, dias, horas, media, maximo, minimo, avaliacao, nome_pdf, imagem):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório de Estudos Semanais", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Aluno: {nome}", ln=True)

    for dia, hora in zip(dias, horas):
        pdf.cell(200, 10, txt=f"{dia}: {hora} horas", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Média diária: {media:.2f} horas", ln=True)
    pdf.cell(200, 10, txt=f"Máximo: {maximo:.2f} horas", ln=True)
    pdf.cell(200, 10, txt=f"Mínimo: {minimo:.2f} horas", ln=True)
    pdf.cell(200, 10, txt=f"Avaliação: {avaliacao}", ln=True)

    pdf.image(imagem, x=30, w=150)
    pdf.output(nome_pdf)

# 🧠 Função de avaliação
def avaliar_semana(media):
    if media >= 6:
        return "Excelente ritmo de estudos! Continue assim e você estará cada vez mais perto dos seus objetivos. 💪📘"
    elif media >= 4:
        return "Bom trabalho, mas você pode melhorar! Tente organizar melhor sua rotina para ganhar mais consistência. 🚀"
    else:
        return "Você estudou pouco essa semana. Procure estabelecer metas diárias e focar no seu objetivo. Você consegue! 🌱📚"

# 🖼️ Configuração do app
st.set_page_config(page_title="Analisador de Estudos", layout="centered")
st.title("📊 Analisador de Estudos Semanais")
st.write("Informe quantas horas você estudou em cada dia da semana. Veja o gráfico e baixe seu relatório em PDF.")

# ✏️ Entrada de nome
nome_aluno = st.text_input("Digite seu nome:")

# 📅 Dias e coleta de horas
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
horas_estudo = []

# 📋 Formulário com sliders
with st.form("form_estudos"):
    for dia in dias_semana:
        horas = st.slider(f"{dia}:", 0.0, 12.0, step=0.5, key=dia)
        horas_estudo.append(horas)
    submitted = st.form_submit_button("Gerar Análise")

# ✅ Processamento
if submitted:
    if nome_aluno.strip() == "":
        st.warning("Por favor, digite seu nome para gerar o relatório.")
    else:
        st.write("🔄 Processando dados...")

        media = np.mean(horas_estudo)
        maximo = np.max(horas_estudo)
        minimo = np.min(horas_estudo)
        avaliacao = avaliar_semana(media)

        # 📋 Avaliação na tela
        st.subheader("📋 Avaliação da Semana")
        st.markdown(f"""
**Média de estudo por dia:** {media:.2f} horas  
**Resumo:** {avaliacao}
""")

        st.write("📊 Gerando gráfico...")

        fig = gerar_grafico(dias_semana, horas_estudo)
        st.subheader("📈 Gráfico de Estudo")
        st.pyplot(fig)

        # Salvando gráfico
        img_path = "grafico_estudos.png"
        fig.savefig(img_path)

        data = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nome_pdf = f"Relatorio_Estudos_{nome_aluno.replace(' ', '_')}_{data}.pdf"

        st.write("📄 Gerando PDF...")
        gerar_pdf(nome_aluno, dias_semana, horas_estudo, media, maximo, minimo, avaliacao, nome_pdf, img_path)

        with open(nome_pdf, "rb") as file:
            st.success("✅ Relatório gerado com sucesso!")
            st.download_button("📥 Baixar PDF", data=file, file_name=os.path.basename(nome_pdf), mime="application/pdf")

