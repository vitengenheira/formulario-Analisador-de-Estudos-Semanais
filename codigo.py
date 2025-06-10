# 📦 Importando as bibliotecas necessárias
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime
import os

# 📊 Função que gera o gráfico interativo com Plotly
@st.cache_data
def gerar_grafico(dias, horas):
    fig = go.Figure(data=[
        go.Bar(x=dias, y=horas, marker_color='skyblue')
    ])
    fig.update_layout(
        title='Estudos da Semana',
        xaxis_title='Dias da Semana',
        yaxis_title='Horas Estudadas',
        yaxis=dict(range=[0, 12]),
        template='plotly_white'
    )
    return fig

# 📄 Função que cria o PDF com os dados e o gráfico (salvo como imagem)
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

# 🧠 Função de avaliação personalizada
def avaliar_semana(media):
    if media >= 6:
        return "Excelente ritmo de estudos! Continue assim e você estará cada vez mais perto dos seus objetivos. 💪📘"
    elif media >= 4:
        return "Bom trabalho, mas você pode melhorar! Tente organizar melhor sua rotina para ganhar mais consistência. 🚀"
    else:
        return "Você estudou pouco essa semana. Procure estabelecer metas diárias e focar no seu objetivo. Você consegue! 🌱📚"

# 🖼️ Configuração do Streamlit
st.set_page_config(page_title="Analisador de Estudos", layout="centered")
st.title("📊 Analisador de Estudos Semanais")
st.write("Informe quantas horas você estudou em cada dia da semana. Veja o gráfico e baixe seu relatório em PDF.")

# ✏️ Entrada do nome
nome_aluno = st.text_input("Digite seu nome:")

# 📅 Dias da semana e entrada de dados
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
horas_estudo = []

# 📋 Formulário
with st.form("form_estudos"):
    for dia in dias_semana:
        horas = st.slider(f"{dia}:", 0.0, 12.0, step=0.5, key=dia)
        horas_estudo.append(horas)
    submitted = st.form_submit_button("Gerar Análise")

# ✅ Processamento ao enviar
if submitted:
    if nome_aluno.strip() == "":
        st.warning("Por favor, digite seu nome para gerar o relatório.")
    else:
        st.write("🔄 Processando dados...")

        media = np.mean(horas_estudo)
        maximo = np.max(horas_estudo)
        minimo = np.min(horas_estudo)
        avaliacao = avaliar_semana(media)

        # 📋 Avaliação imediata
        st.subheader("📋 Avaliação da Semana")
        st.markdown(f"""
**Média de estudo por dia:** {media:.2f} horas  
**Resumo:** {avaliacao}
""")

        # 📈 Gráfico
        st.write("📊 Gerando gráfico...")
        fig = gerar_grafico(dias_semana, horas_estudo)
        st.subheader("📈 Gráfico de Estudo")
        st.plotly_chart(fig, use_container_width=True)

        # Exportar gráfico como imagem temporária
        img_path = "grafico_estudos.png"
        fig.write_image(img_path, format="png")

        # Gerar PDF
        data = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nome_pdf = f"Relatorio_Estudos_{nome_aluno.replace(' ', '_')}_{data}.pdf"

        st.write("📄 Gerando PDF...")
        gerar_pdf(nome_aluno, dias_semana, horas_estudo, media, maximo, minimo, avaliacao, nome_pdf, img_path)

        with open(nome_pdf, "rb") as file:
            st.success("✅ Relatório gerado com sucesso!")
            st.download_button("📥 Baixar PDF", data=file, file_name=os.path.basename(nome_pdf), mime="application/pdf")
