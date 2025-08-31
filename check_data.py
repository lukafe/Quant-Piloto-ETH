from datetime import datetime
import pandas as pd

# Carrega os dados
df = pd.read_parquet('data/ETH_USDT_1m.parquet')

# Informações básicas
print("=" * 60)
print("VERIFICAÇÃO DOS DADOS BAIXADOS")
print("=" * 60)

# Período dos dados
data_inicio = df.index.min()
data_fim = df.index.max()
total_registros = len(df)
dias_de_dados = (data_fim - data_inicio).days

print(f"📅 Período dos dados:")
print(f"   Início: {data_inicio}")
print(f"   Fim: {data_fim}")
print(f"   Total de registros: {total_registros:,}")
print(f"   Dias de dados: {dias_de_dados} dias")

# Verificar se chegou até hoje
data_atual = datetime.now()
ultimo_dado = data_fim.to_pydatetime()
diferenca = data_atual - ultimo_dado
horas_atras = diferenca.total_seconds() / 3600

print(f"\n⏰ Atualização:")
print(f"   Data atual: {data_atual.strftime('%Y-%m-%d %H:%M')}")
print(f"   Último dado: {ultimo_dado.strftime('%Y-%m-%d %H:%M')}")
print(f"   Diferença: {horas_atras:.1f} horas atrás")

# Verificar se há gaps nos dados
print(f"\n🔍 Análise de continuidade:")
df_sorted = df.sort_index()
time_diff = df_sorted.index.to_series().diff()
expected_diff = pd.Timedelta(minutes=1)
gaps = time_diff[time_diff > expected_diff]

if len(gaps) > 0:
    print(f"   ⚠️  Encontrados {len(gaps)} gaps nos dados:")
    for gap_time, gap_duration in gaps.head(10).items():
        print(f"      Gap em {gap_time}: {gap_duration}")
else:
    print(f"   ✅ Dados contínuos sem gaps detectados")

# Estatísticas básicas
print(f"\n📊 Estatísticas dos preços:")
print(f"   Preço mínimo: ${df['low'].min():,.2f}")
print(f"   Preço máximo: ${df['high'].max():,.2f}")
print(f"   Preço atual: ${df['close'].iloc[-1]:,.2f}")

print(f"\n📁 Arquivo salvo: data/ETH_USDT_1m.parquet ({total_registros:,} registros)")
print("=" * 60) 