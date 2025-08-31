# 📊 Quant Piloto ETH - Simulação de Mercado com Agentes

Um projeto de simulação de mercado de criptomoedas usando modelagem baseada em agentes (ABM) com dados reais do ETH/USDT, integrado com Reinforcement Learning para estratégias de trading.

## 🎯 Objetivo

Desenvolver e testar modelos de simulação de mercado usando agentes artificiais que interagem entre si, calibrados com dados reais de criptomoedas, e criar um ambiente de trading para treinamento de agentes de IA.

## 📁 Estrutura do Projeto

### 📊 **download_data.py** - Download de Dados Históricos
**Bibliotecas:** `ccxt`, `pandas`, `pyarrow`

**Funcionalidade:**
- Baixa dados OHLCV (Open, High, Low, Close, Volume) do par ETH/USDT da Binance
- Período: Desde 2022-01-01 até a data atual
- Timeframe: 1 minuto
- Salva os dados em formato Parquet para eficiência

**Lógica:**
```python
# Baixa dados em lotes de 1000 registros
# Trata erros de rede e limites da API
# Concatena todos os dados em um DataFrame
# Salva como 'data/ETH_USDT_1m.parquet'
```

---

### 🔍 **check_data.py** - Verificação de Integridade dos Dados
**Bibliotecas:** `pandas`, `datetime`

**Funcionalidade:**
- Verifica se os dados foram baixados corretamente
- Analisa gaps temporais nos dados
- Mostra estatísticas básicas (preço mínimo, máximo, atual)
- Confirma se os dados chegam até a data atual

**Lógica:**
```python
# Carrega o arquivo Parquet
# Calcula período total dos dados
# Identifica gaps usando diff() temporal
# Exibe estatísticas de preços
```

---

### 📈 **view_data.py** - Visualização dos Dados
**Bibliotecas:** `pandas`, `matplotlib`

**Funcionalidade:**
- Cria gráficos dos dados históricos
- Mostra evolução temporal dos preços
- Permite análise visual da volatilidade
- Útil para entender os padrões dos dados

---

### 🤖 **mfa_advanced.py** - Modelo Financeiro Artificial Avançado
**Bibliotecas:** `mesa`, `pandas`, `numpy`

**Funcionalidade:**
- Simulação de mercado usando agentes baseados em agentes (ABM)
- 4 tipos de agentes: Chartistas, Fundamentalistas, Noise Traders, Market Makers
- Calibração com dados reais de volatilidade
- Decisões probabilísticas baseadas em convicção

**Tipos de Agentes:**

1. **ChartistAgent** (40 agentes)
   - Segue tendências de preço
   - Compra quando preço sobe, vende quando desce
   - Decisão probabilística baseada em convicção

2. **FundamentalistAgent** (40 agentes)
   - Estratégia de mean-reversion
   - Compra quando preço está baixo, vende quando alto
   - Usa dados reais para calcular valor fundamental

3. **NoiseTraderAgent** (15 agentes)
   - Ações aleatórias para simular ruído de mercado
   - Adiciona volatilidade realista

4. **MarketMakerAgent** (5 agentes)
   - Fornece liquidez ao mercado
   - Estabiliza preços extremos
   - Compra quando preço cai muito, vende quando sobe muito

**Lógica de Preços:**
```python
# Demanda total = soma das demandas de todos os agentes
# Impacto dinâmico baseado na volatilidade recente
# Mudança de preço = demanda_total * impacto * fator_aleatório
```

---

### 🎮 **trading_env.py** - Ambiente de Trading para RL
**Bibliotecas:** `gymnasium`, `stable-baselines3`, `pandas`, `numpy`

**Funcionalidade:**
- Ambiente de Reinforcement Learning compatível com Gymnasium
- Integra o MFA como simulador de mercado
- 3 ações possíveis: Manter (0), Comprar (1), Vender (2)
- Observação: janela de 60 preços históricos
- Recompensa: mudança no patrimônio líquido

**Interface RL:**
```python
# Espaço de ação: Discrete(3)
# Espaço de observação: Box(60,) - 60 preços históricos
# Patrimônio inicial: $10,000
# Episódio termina em 1000 passos ou patrimônio <= 0
```

**Lógica de Trading:**
```python
# Compra: gasta todo o saldo disponível
# Venda: vende todas as ações possuídas
# Patrimônio = saldo + (ações * preço_atual)
# Recompensa = mudança no patrimônio
```

---

### 🧪 **test_trading_env.py** - Teste do Ambiente
**Bibliotecas:** `trading_env`, `os`

**Funcionalidade:**
- Testa o ambiente de trading executando simulações
- Valida se o ambiente está funcionando corretamente
- Mostra estatísticas de performance
- Útil para debug e validação

## 🛠️ Dependências Principais

### Core Dependencies:
```bash
pip install mesa==3.2.0          # Framework de modelagem baseada em agentes
pip install pandas               # Manipulação de dados
pip install numpy                # Computação numérica
pip install matplotlib           # Visualização
```

### Data & Trading:
```bash
pip install ccxt                 # API de exchanges de criptomoedas
pip install pyarrow              # Formato Parquet para dados
pip install gymnasium            # Ambiente de RL
pip install stable-baselines3    # Algoritmos de RL
```

## 🚀 Como Usar

### 1. Download dos Dados
```bash
python download_data.py
```

### 2. Verificar Dados
```bash
python check_data.py
```

### 3. Visualizar Dados
```bash
python view_data.py
```

### 4. Testar Simulação Básica
```bash
python mfa_advanced.py
```

### 5. Testar Ambiente de Trading
```bash
python trading_env.py
python test_trading_env.py
```

## 📊 Fluxo de Dados

```
1. download_data.py → data/ETH_USDT_1m.parquet
2. check_data.py → Validação dos dados
3. view_data.py → Visualização
4. mfa_advanced.py → Simulação com agentes
5. trading_env.py → Ambiente de RL
6. test_trading_env.py → Testes e validação
```

## 🎯 Aplicações

- **Pesquisa Acadêmica:** Estudo de dinâmicas de mercado
- **Desenvolvimento de Estratégias:** Teste de algoritmos de trading
- **Machine Learning:** Treinamento de agentes de IA
- **Educação:** Aprendizado sobre mercados financeiros

## 🔧 Configurações

### Parâmetros dos Agentes (mfa_advanced.py):
- Chartistas: 40 agentes
- Fundamentalistas: 40 agentes  
- Noise Traders: 15 agentes
- Market Makers: 5 agentes

### Configurações do Ambiente (trading_env.py):
- Janela de observação: 60 períodos
- Patrimônio inicial: $10,000
- Duração do episódio: 1000 passos
- Ações: Manter, Comprar, Vender

## 📈 Resultados Esperados

- Simulação realista de movimentos de preço
- Comportamento emergente de mercado
- Ambiente estável para treinamento de RL
- Dados calibrados com volatilidade real

## 🐛 Troubleshooting

### Problemas Comuns:
1. **Erro de API:** Verificar conexão com internet
2. **Dados incompletos:** Executar `download_data.py` novamente
3. **Erro Mesa:** Verificar versão (3.2.0+)
4. **NaN nos preços:** Ajustar parâmetros de impacto no MFA

## 📝 Notas Técnicas

- Todos os dados são reais (sem dados sintéticos)
- Simulação calibrada com volatilidade histórica
- Ambiente compatível com Stable-Baselines3
- Código otimizado para performance

---

**Desenvolvido para simulação e pesquisa em mercados financeiros usando dados reais de criptomoedas.** 