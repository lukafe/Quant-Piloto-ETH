# mfa_advanced.py

from mesa import Agent, Model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Carregando os Dados Reais (sem alterações) ---
def load_real_data(file_path):
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo de dados '{file_path}' não encontrado.")
        return None
    df = pd.read_parquet(file_path)
    return df['close']

# --- Definições dos Agentes (com MarketMaker e lógica probabilística) ---

class MarketAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.demand = 0

    def step(self):
        pass

class ChartistAgent(MarketAgent):
    """Grafista com decisão probabilística."""
    def __init__(self, model, lookback_period=10, conviction=0.75):
        super().__init__(model)
        self.lookback_period = lookback_period
        self.conviction = conviction # Confiança base do agente

    def step(self):
        history = self.model.price_history
        if len(history) < self.lookback_period:
            self.demand = 0
            return
        
        recent_prices = history[-self.lookback_period:]
        # Ação é baseada na tendência, mas a decisão é probabilística
        if recent_prices[-1] > recent_prices[0]: # Tendência de alta
            if self.model.random.random() < self.conviction:
                self.demand = 1
            else:
                self.demand = 0
        else: # Tendência de baixa
            if self.model.random.random() < self.conviction:
                self.demand = -1
            else:
                self.demand = 0

class FundamentalistAgent(MarketAgent):
    """Fundamentalista com decisão probabilística."""
    def __init__(self, model, fundamental_period=200, conviction=0.75):
        super().__init__(model)
        self.fundamental_period = fundamental_period
        self.conviction = conviction

    def step(self):
        real_data_index = self.model.step_count
        if real_data_index < self.fundamental_period or real_data_index >= len(self.model.real_prices):
            self.demand = 0
            return
            
        fundamental_value = self.model.real_prices.iloc[real_data_index - self.fundamental_period : real_data_index].mean()
        current_price = self.model.current_price

        if current_price < fundamental_value: # Preço "barato"
            if self.model.random.random() < self.conviction:
                self.demand = 1
            else:
                self.demand = 0
        else: # Preço "caro"
            if self.model.random.random() < self.conviction:
                self.demand = -1
            else:
                self.demand = 0

class NoiseTraderAgent(MarketAgent):
    """Trader de Ruído (sem alterações)."""
    def step(self):
        self.demand = self.model.random.choice([-1, 0, 1]) # Adicionada a opção de não fazer nada

class MarketMakerAgent(MarketAgent):
    """
    NOVO AGENTE: O Estabilizador.
    Age contra a demanda líquida para prover liquidez e reduzir a volatilidade.
    """
    def __init__(self, model, strength=0.5):
        super().__init__(model)
        self.strength = strength # Quão forte ele age contra o mercado

    def step(self):
        # Este agente age DEPOIS dos outros, então sua lógica vai no 'advance' do modelo
        pass

    def act(self, net_demand):
        # Age na direção oposta à demanda líquida, com uma certa força
        self.demand = -net_demand * self.strength

# --- Modelo de Mercado Avançado ---

class MarketModel(Model):
    def __init__(self, n_chartists, n_fundamentalists, n_noise, n_makers, real_prices_series):
        super().__init__()
        self.real_prices = real_prices_series
        self.step_count = 0
        
        self.initial_history_size = 200
        self.price_history = self.real_prices.iloc[:self.initial_history_size].tolist()
        self.current_price = self.price_history[-1]
        self.step_count = self.initial_history_size
        
        # Fator de impacto muito menor para evitar overflow
        real_volatility = self.real_prices.pct_change().std()
        self.base_impact = real_volatility * 0.01  # Reduzido drasticamente
        self.impact_factor = self.base_impact

        # Criar os agentes usando a nova API
        self.market_makers = []
        
        for i in range(n_chartists):
            agent = ChartistAgent(self)
            
        for i in range(n_fundamentalists):
            agent = FundamentalistAgent(self)
            
        for i in range(n_noise):
            agent = NoiseTraderAgent(self)
            
        for i in range(n_makers):
            maker = MarketMakerAgent(self)
            self.market_makers.append(maker) # Market makers agem separadamente

    def step(self):
        # 1. Ativa os traders normais usando a nova API
        self.agents.shuffle_do("step")
        
        # 2. Calcula a demanda líquida dos traders
        trader_demand = sum(agent.demand for agent in self.agents)
        
        # 3. Os Market Makers reagem a essa demanda
        for maker in self.market_makers:
            maker.act(trader_demand)
        maker_demand = sum(maker.demand for maker in self.market_makers)

        # 4. Calcula a demanda final e atualiza o preço
        total_demand = trader_demand + maker_demand
        
        # 5. Ajuste dinâmico do impacto com validações
        if len(self.price_history) > 20:
            recent_prices = pd.Series(self.price_history[-20:])
            recent_vol = recent_prices.pct_change().std()
            # Validação para evitar divisão por zero ou valores inválidos
            if pd.notna(recent_vol) and recent_vol > 0:
                self.impact_factor = self.base_impact / (1 + recent_vol * 100)  # Reduzido o multiplicador
            else:
                self.impact_factor = self.base_impact

        # Limitar a demanda total para evitar overflow
        total_demand = np.clip(total_demand, -50, 50)
        
        # Aplicar mudança de preço com validações
        price_change_factor = np.exp(total_demand * self.impact_factor)
        
        # Validar se o fator é válido
        if np.isfinite(price_change_factor) and price_change_factor > 0:
            self.current_price *= price_change_factor
        
        # Adicionar ruído apenas se o preço for válido
        if np.isfinite(self.current_price) and self.current_price > 0:
            noise_factor = 1 + np.random.normal(0, 0.0005)
            self.current_price *= noise_factor
        
        # Validação final do preço
        if not np.isfinite(self.current_price) or self.current_price <= 0:
            self.current_price = self.price_history[-1]  # Usar o último preço válido

        self.price_history.append(self.current_price)
        self.step_count += 1

# --- Bloco de Execução ---
if __name__ == '__main__':
    real_prices_data = load_real_data(os.path.join('data', 'ETH_USDT_1m.parquet'))
    
    if real_prices_data is not None:
        # Parâmetros: Agora com Market Makers
        N_STEPS = 1000
        N_CHARTISTS = 40
        N_FUNDAMENTALISTS = 40
        N_NOISE_TRADERS = 15
        N_MARKET_MAKERS = 5 # Um pequeno número de market makers já tem um grande efeito

        print("Iniciando a simulação do MFA Avançado (Estabilizado)...")
        print(f"Dados reais carregados: {len(real_prices_data):,} registros")
        
        model = MarketModel(N_CHARTISTS, N_FUNDAMENTALISTS, N_NOISE_TRADERS, N_MARKET_MAKERS, real_prices_data)
        print(f"Modelo criado com {len(model.agents)} agentes normais + {len(model.market_makers)} market makers")
        
        for i in range(N_STEPS):
            model.step()
            if (i + 1) % 100 == 0:
                print(f"Passo {i+1}/{N_STEPS} concluído. Preço atual: ${model.current_price:.2f}")

        print("Simulação finalizada.")
        generated_prices = model.price_history

        # --- Visualização Comparativa ---
        plt.figure(figsize=(15, 7))
        plt.plot(generated_prices, label='Preço Gerado pelo MFA (Avançado)', linewidth=1.5, zorder=2)
        real_segment_to_plot = real_prices_data.iloc[:len(generated_prices)]
        plt.plot(real_segment_to_plot.values, label='Preço Real do ETH (Referência)', linestyle='--', color='gray', linewidth=1, zorder=1)
        plt.title("Preço Sintético (Estabilizado) vs. Preço Real")
        plt.xlabel("Passos de Tempo")
        plt.ylabel("Preço")
        plt.legend()
        plt.grid(True)
        plt.show()