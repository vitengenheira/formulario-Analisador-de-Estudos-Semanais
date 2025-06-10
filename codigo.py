# 📦 Importando as bibliotecas necessárias
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import os

# 📊 Função que gera o gráfico de barras com as horas estudadas
def gerar_grafico(dias, horas):
    fig, ax = plt.subplots()
    ax.bar(dias, horas, color='skyblue')
    ax.set_ylabel('Horas Estudadas')
    ax.set_title('Estudos da Semana')
    ax.set_ylim(0, 12)
    return fig

# 📄 Função que cria o PDF com os dados e o gráfico
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

# 🧠 Função que avalia o desempenho da semana com base na média de estudo
def avaliar_semana(media):
    if media >= 6:
        return "Excelente ritmo de estudos!"
    elif media >= 4:
        return "Bom, mas pode melhorar!"
    else:
        return "Procure se organizar melhor."

# 🖼️ Configuração da interface do Streamlit
st.set_page_config(page_title="Analisador de Estudos", layout="centered")
st.title("📊 Analisador de Estudos Semanais")
st.write("Informe quantas horas você estudou em cada dia da semana. Veja o gráfico e baixe seu relatório em PDF.")

# ✏️ Campo de entrada de texto para o nome do aluno
nome_aluno = st.text_input("Digite seu nome:")

# 📅 Lista com os dias da semana
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
horas_estudo = []

# 📋 Formulário com sliders para cada dia
with st.form("form_estudos"):
    for dia in dias_semana:
        horas = st.slider(f"{dia}:", 0.0, 12.0, step=0.5, key=dia)
        horas_estudo.append(horas)
    submitted = st.form_submit_button("Gerar Análise")

# ✅ Processamento dos dados após envio
if submitted:
    if nome_aluno.strip() == "":
        st.warning("Por favor, digite seu nome para gerar o relatório.")
    else:
        media = np.mean(horas_estudo)
        maximo = np.max(horas_estudo)
        minimo = np.min(horas_estudo)
        avaliacao = avaliar_semana(media)

        st.subheader("📈 Gráfico de Estudo")
        fig = gerar_grafico(dias_semana, horas_estudo)
        st.pyplot(fig)

        # ✅ Caminhos corrigidos para funcionar no Streamlit Cloud
        img_path = "grafico_estudos.png"
        fig.savefig(img_path)

        data = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nome_pdf = f"Relatorio_Estudos_{nome_aluno.replace(' ', '_')}_{data}.pdf"

        gerar_pdf(nome_aluno, dias_semana, horas_estudo, media, maximo, minimo, avaliacao, nome_pdf, img_path)

        with open(nome_pdf, "rb") as file:
            st.success("✅ Relatório gerado com sucesso!")
            st.download_button("📥 Baixar PDF", data=file, file_name=os.path.basename(nome_pdf), mime="application/pdf")
