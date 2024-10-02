from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app = Flask(__name__)
app.secret_key = 'secretkey'

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Lista para armazenar os dados dos arquivos carregados
dados_lista = []

# Função para carregar e analisar os dados de estoque
def carregar_estoque(arquivo):
    data = pd.read_csv(arquivo, skiprows=1, names=['Data', 'Produto', 'Quantidade', 'Vendas'])
    data['Quantidade'] = pd.to_numeric(data['Quantidade'], errors='coerce')
    data['Vendas'] = pd.to_numeric(data['Vendas'], errors='coerce')
    data = data.dropna(subset=['Quantidade', 'Vendas'])
    return data

# Função para calcular vendas por dia, semana e mês
def calcular_vendas(data):
    data['Data'] = pd.to_datetime(data['Data'])
    daily_sales = data.groupby('Data')['Vendas'].sum().reset_index()
    weekly_sales = data.resample('W-Mon', on='Data').sum()['Vendas'].reset_index()
    monthly_sales = data.resample('M', on='Data').sum()['Vendas'].reset_index()
    return daily_sales, weekly_sales, monthly_sales

# Função para somar as vendas de todos os arquivos carregados
def calcular_vendas_totais(dados_lista):
    # Junta os dados de todos os arquivos carregados
    all_data = pd.concat(dados_lista)
    all_data['AnoMes'] = all_data['Data'].dt.strftime('%d/%Y')  # Formata a data
    total_sales = all_data.groupby('AnoMes')['Vendas'].sum().reset_index()
    return total_sales

# Página inicial de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if email == EMAIL and senha == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('estoque'))
        else:
            return render_template('login.html', erro="Email ou senha inválidos")
    return render_template('login.html')

# Página de estoque
@app.route('/estoque', methods=['GET', 'POST'])
def estoque():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Se um arquivo CSV foi enviado
    if request.method == 'POST':
        file = request.files['csv_file']
        if file and file.filename.endswith('.csv'):
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)

            # Carregar e adicionar os dados ao lista
            data = carregar_estoque(file_path)
            dados_lista.append(data)

            # Gráfico de Estoque
            img = BytesIO()
            plt.figure(figsize=(10, 5))
            try:
                data.groupby('Produto')['Quantidade'].sum().plot(kind='bar', color='skyblue')
            except IndexError:
                return "Erro: Não há dados suficientes para plotar o gráfico."
            plt.title('Quantidade de Produtos em Estoque')
            plt.xlabel('Produto')
            plt.ylabel('Quantidade')
            plt.tight_layout()
            plt.savefig(img, format='png')
            img.seek(0)
            graph_url = base64.b64encode(img.getvalue()).decode('utf8')

            daily_sales, weekly_sales, monthly_sales = calcular_vendas(data)

            # Gráfico de Vendas Totais por Mês (recalcular com dados atualizados)
            total_sales = calcular_vendas_totais(dados_lista)

            monthly_sales_img = BytesIO()
            plt.figure(figsize=(10, 5))
            total_sales.plot(x='AnoMes', y='Vendas', kind='line', marker='o', color='green')
            plt.title('Vendas Totais por Mês')
            plt.xlabel('Mês/Ano')
            plt.ylabel('Vendas Totais')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(monthly_sales_img, format='png')
            monthly_sales_img.seek(0)
            monthly_sales_graph_url = base64.b64encode(monthly_sales_img.getvalue()).decode('utf8')

            return render_template('estoque.html',
                                   table=data.to_html(),
                                   daily_sales_table=daily_sales.to_html(),
                                   weekly_sales_table=weekly_sales.to_html(),
                                   monthly_sales_table=monthly_sales.to_html(),
                                   graph_url=graph_url,
                                   monthly_sales_graph_url=monthly_sales_graph_url)

    # Carrega os dados de estoque (padrão)
    if dados_lista:
        data = dados_lista[-1]
    else:
        data = carregar_estoque('estoque0110.csv')
        dados_lista.append(data)

    # Gráfico de Estoque
    img = BytesIO()
    plt.figure(figsize=(10, 5))
    try:
        data.groupby('Produto')['Quantidade'].sum().plot(kind='bar', color='skyblue')
    except IndexError:
        return "Erro: Não há dados suficientes para plotar o gráfico."
    plt.title('Quantidade de Produtos em Estoque')
    plt.xlabel('Produto')
    plt.ylabel('Quantidade')
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')

    daily_sales, weekly_sales, monthly_sales = calcular_vendas(data)

    # Gráfico de Vendas Totais por Mês (recalcular com dados atualizados)
    total_sales = calcular_vendas_totais(dados_lista)

    monthly_sales_img = BytesIO()
    plt.figure(figsize=(10, 5))
    total_sales.plot(x='AnoMes', y='Vendas', kind='line', marker='o', color='green')
    plt.title('Vendas Totais por Mês')
    plt.xlabel('Mês/Ano')
    plt.ylabel('Vendas Totais')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(monthly_sales_img, format='png')
    monthly_sales_img.seek(0)
    monthly_sales_graph_url = base64.b64encode(monthly_sales_img.getvalue()).decode('utf8')

    return render_template('estoque.html',
                           table=data.to_html(),
                           daily_sales_table=daily_sales.to_html(),
                           weekly_sales_table=weekly_sales.to_html(),
                           monthly_sales_table=monthly_sales.to_html(),
                           graph_url=graph_url,
                           monthly_sales_graph_url=monthly_sales_graph_url)

# Função para logout
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
