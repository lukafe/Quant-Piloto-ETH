# view_data.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def visualize_data(file_path):
    """
    Carrega e visualiza os dados de um arquivo Parquet.

    :param file_path: O caminho para o arquivo.parquet
    """
    # --- 1. Verificação e Carregamento ---
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        print("Por favor, execute o script 'download_data.py' primeiro.")
        return

    print(f"Carregando dados de '{file_path}'...")
    try:
        df = pd.read_parquet(file_path)
        print("Dados carregados com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return

    # --- 2. Inspeção Básica no Terminal ---
    print("\n" + "="*50)
    print("1. INSPEÇÃO BÁSICA DOS DADOS")
    print("="*50)

    # Mostra as primeiras 5 linhas para entendermos a estrutura
    print("\nPrimeiras 5 linhas (head):")
    print(df.head())

    # Mostra as últimas 5 linhas para verificar a data final
    print("\nÚltimas 5 linhas (tail):")
    print(df.tail())

    # Mostra um resumo técnico: número de entradas, colunas, tipos de dados e uso de memória
    print("\nInformações sobre o DataFrame (info):")
    df.info()

    # --- 3. Inspeção Visual com Gráfico ---
    print("\n" + "="*50)
    print("2. INSPEÇÃO VISUAL (GRÁFICO)")
    print("="*50)
    print("Gerando o gráfico de preços... Feche a janela do gráfico para finalizar o script.")

    # Configura o tamanho da figura para melhor visualização
    plt.figure(figsize=(15, 7))

    # Plota a coluna 'close' usando o índice (timestamp) como eixo X
    plt.plot(df.index, df['close'], label='Preço de Fechamento (Close)', color='blue', linewidth=0.7)

    # Adiciona títulos e legendas para clareza
    plt.title(f'Histórico de Preço ETH/USDT ({len(df)} minutos de dados)')
    plt.xlabel('Data')
    plt.ylabel('Preço (USDT)')
    plt.legend()
    plt.grid(True) # Adiciona uma grade para facilitar a leitura dos valores

    # Melhora a formatação do eixo de datas
    plt.tight_layout()

    # Exibe o gráfico
    plt.show()

    print("\nVisualização concluída.")


if __name__ == '__main__':
    # O caminho para o arquivo que foi criado pelo script de download
    DATA_FILE_PATH = os.path.join('data', 'ETH_USDT_1m.parquet')
    
    visualize_data(DATA_FILE_PATH)