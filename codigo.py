# 📦 Importando as bibliotecas necessárias
import streamlit as st                     # Para criar a interface web
import numpy as np                         # Para calcular média, máximo e mínimo
import matplotlib.pyplot as plt            # Para gerar o gráfico
from fpdf import FPDF                      # Para criar o PDF
from datetime import datetime              # Para gerar nome único baseado na data/hora
import os                                  # Para lidar com o nome do arquivo PDF

# 📊 Função que gera o gráfico de barras com as horas estudadas
def gerar_grafico(dias, horas):
    fig, ax = plt.subplots()                         # Cria uma figura e um eixo
    ax.bar(dias, horas, color='skyblue')             # Gráfico de barras com cor azul clara
    ax.set_ylabel('Horas Estudadas')                 # Rótulo do eixo Y
    ax.set_title('Estudos da Semana')                # Título do gráfico
    ax.set_ylim(0, 12)                               # Define o limite do eixo Y (0 a 12 horas)
    return fig                                       # Retorna a figura gerada

# 📄 Função que cria o PDF com os dados e o gráfico
def gerar_pdf(nome, dias, horas, media, maximo, minimo, avaliacao, nome_pdf, imagem):
    pdf = FPDF()                                     # Instancia o PDF
    pdf.add_page()                                   # Adiciona uma nova página
    pdf.set_font("Arial", size=12)                   # Define a fonte padrão

    pdf.cell(200, 10, txt="Relatório de Estudos Semanais", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Aluno: {nome}", ln=True)

    for dia, hora in zip(dias, horas):               # Escreve cada dia e horas correspondentes
        pdf.cell(200, 10, txt=f"{dia}: {hora} horas", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Média diária: {media:.2f} horas", ln=True)
    pdf.cell(200, 10, txt=f"Máximo: {maximo:.2f} horas", ln=True)
    pdf.cell(200, 10, txt=f"Mínimo: {minimo:.2f} horas", ln=True)
    pdf.cell(200, 10, txt=f"Avaliação: {avaliacao}", ln=True)

    pdf.image(imagem, x=30, w=150)                   # Adiciona o gráfico salvo

    pdf.output(nome_pdf)                             # Salva o PDF com o nome definido

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

# 🧾 Título e descrição
st.title("📊 Analisador de Estudos Semanais")
st.write("Informe quantas horas você estudou em cada dia da semana. Veja o gráfico e baixe seu relatório em PDF.")

# ✏️ Campo de entrada de texto para o nome do aluno
nome_aluno = st.text_input("Digite seu nome:")

# 📅 Lista com os dias da semana
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
horas_estudo = []  # Lista para armazenar as horas de estudo

# 📋 Formulário com sliders para cada dia
with st.form("form_estudos"):
    for dia in dias_semana:
        # Slider de 0 a 12h, com passos de 0.5h
        horas = st.slider(f"{dia}:", 0.0, 12.0, step=0.5, key=dia)
        horas_estudo.append(horas)
    # Botão de envio do formulário
    submitted = st.form_submit_button("Gerar Análise")

# ✅ Processamento dos dados após envio
if submitted:
    # Verifica se o nome foi preenchido
    if nome_aluno.strip() == "":
        st.warning("Por favor, digite seu nome para gerar o relatório.")
    else:
        # Calcula estatísticas com NumPy
        media = np.mean(horas_estudo)
        maximo = np.max(horas_estudo)
        minimo = np.min(horas_estudo)

        # Faz uma avaliação da semana
        avaliacao = avaliar_semana(media)

        # 🖼️ Mostra o gráfico
        st.subheader("📈 Gráfico de Estudo")
        fig = gerar_grafico(dias_semana, horas_estudo)
        st.pyplot(fig)

        # Salva o gráfico como imagem temporária
        img_path = "/mnt/data/grafico_estudos.png"
        fig.savefig(img_path)

        # Define o nome do PDF com a data e hora atual
        data = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nome_pdf = f"/mnt/data/Relatorio_Estudos_{nome_aluno.replace(' ', '_')}_{data}.pdf"

        # Gera o PDF com os dados
        gerar_pdf(nome_aluno, dias_semana, horas_estudo, media, maximo, minimo, avaliacao, nome_pdf, img_path)

        # Mostra botão de download do PDF
        with open(nome_pdf, "rb") as file:
            st.success("✅ Relatório gerado com sucesso!")
            st.download_button("📥 Baixar PDF", data=file, file_name=os.path.basename(nome_pdf), mime="application/pdf")
