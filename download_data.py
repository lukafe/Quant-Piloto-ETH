# download_data.py

import ccxt
import pandas as pd
from datetime import datetime
import time
import os

def download_historical_data(symbol, timeframe, since_date, output_folder='data'):
    """
    Baixa dados históricos OHLCV de uma exchange e os salva em formato Parquet.

    :param symbol: O par de moedas (ex: 'ETH/USDT')
    :param timeframe: O intervalo de tempo (ex: '1m', '5m', '1h')
    :param since_date: A data de início no formato 'YYYY-MM-DD'
    :param output_folder: A pasta onde os dados serão salvos
    """
    # --- 1. Inicialização e Configuração ---
    exchange = ccxt.binance({
        'rateLimit': 1200,  # Respeita o limite da API
        'enableRateLimit': True
    })

    # Converte a data de início para um timestamp em milissegundos, que é o que a API espera
    since_timestamp = exchange.parse8601(f'{since_date}T00:00:00Z')
    limit_per_request = 1000  # Número máximo de velas por requisição (padrão da Binance)
    all_ohlcv = []

    print("-" * 50)
    print(f"Iniciando download de dados para {symbol} no timeframe de {timeframe}")
    print(f"A partir de: {since_date}")
    print("-" * 50)

    # --- 2. O Loop de Coleta de Dados ---
    while True:
        try:
            # Busca o próximo "pedaço" de dados
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since_timestamp, limit_per_request)

            # Condição de parada: se a API não retornar mais dados, saímos do loop
            if len(ohlcv) == 0:
                print("Não há mais dados a serem baixados. Concluindo.")
                break

            # O primeiro e o último timestamp do lote recebido
            first_ts = ohlcv[0][0]
            last_ts = ohlcv[-1][0]
            
            print(f"Recebidos {len(ohlcv)} candles de {datetime.utcfromtimestamp(first_ts/1000)} até {datetime.utcfromtimestamp(last_ts/1000)}")

            # Atualiza o 'since_timestamp' para a próxima iteração.
            # A próxima busca começará a partir do último timestamp recebido + 1 milissegundo.
            since_timestamp = last_ts + 1
            
            all_ohlcv.extend(ohlcv)
            
            # Uma pequena pausa para ser gentil com a API
            time.sleep(exchange.rateLimit / 1000)

        except ccxt.NetworkError as e:
            print(f"Erro de rede: {e}. Tentando novamente em 30 segundos...")
            time.sleep(30)
        except ccxt.ExchangeError as e:
            print(f"Erro da exchange: {e}. Tentando novamente em 60 segundos...")
            time.sleep(60)
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}. Abortando.")
            break

    print("\nDownload completo.")

    # --- 3. Processamento e Armazenamento ---
    if not all_ohlcv:
        print("Nenhum dado foi baixado. Verifique os parâmetros.")
        return

    # Converte a lista de listas em um DataFrame do Pandas
    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # Remove duplicatas que podem ocorrer em raras ocasiões
    df.drop_duplicates(subset='timestamp', inplace=True)

    # Converte o timestamp de milissegundos para um formato de data legível e o define como índice
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    # Garante que os dados estejam ordenados cronologicamente
    df.sort_index(inplace=True)

    print(f"\nTotal de {len(df)} candles únicos processados.")
    print("Amostra dos dados:")
    print(df.head())
    print(df.tail())

    # Cria a pasta de saída se ela não existir
    os.makedirs(output_folder, exist_ok=True)
    
    # Salva em formato Parquet para eficiência
    output_file = os.path.join(output_folder, f"{symbol.replace('/', '_')}_{timeframe}.parquet")
    df.to_parquet(output_file)

    print(f"\nDados salvos com sucesso em: '{output_file}'")


if __name__ == '__main__':
    # --- Parâmetros de Execução ---
    # Par de moedas que queremos baixar
    TARGET_SYMBOL = 'ETH/USDT'
    # Timeframe das velas
    TARGET_TIMEFRAME = '1m'
    # Data de início do histórico
    START_DATE = '2022-01-01'

    download_historical_data(TARGET_SYMBOL, TARGET_TIMEFRAME, START_DATE)