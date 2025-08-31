# trading_env.py

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
import os

# Importa o nosso simulador de mercado da iteração anterior
from mfa_advanced import MarketModel, load_real_data

class TradingEnv(gym.Env):
    """
    Um ambiente de trading para Reinforcement Learning que encapsula nosso MFA.
    Segue a interface padrão do Gymnasium.
    """
    metadata = {'render_modes': ['human']}

    def __init__(self, real_prices_data, window_size=60):
        super().__init__()

        self.real_prices_data = real_prices_data
        self.window_size = window_size
        self.simulation_steps = 1000 # Duração de cada episódio de treinamento

        # --- 1. Definir os Espaços de Ação e Observação ---
        # 3 ações discretas: 0=Manter, 1=Comprar, 2=Vender
        self.action_space = spaces.Discrete(3)

        # O agente observa uma janela de preços passados.
        # Usamos um Box com valores entre 0 e infinito (preços não podem ser negativos)
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(self.window_size,), dtype=np.float32
        )

        # Inicializa o estado do ambiente
        self.current_step = 0
        self.balance = 10000  # Saldo inicial em dinheiro
        self.shares_held = 0
        self.net_worth = self.balance
        self.total_reward = 0

    def _get_obs(self):
        """Retorna a observação atual (a janela de preços)."""
        # Pega os últimos `window_size` preços do histórico do nosso simulador
        obs = self.market_model.price_history[-self.window_size:]
        return np.array(obs, dtype=np.float32)

    def _get_info(self):
        """Retorna informações de diagnóstico."""
        return {
            "net_worth": self.net_worth,
            "shares_held": self.shares_held,
            "balance": self.balance,
            "total_reward": self.total_reward
        }

    def reset(self, seed=None, options=None):
        """Reinicia o ambiente para um novo episódio."""
        super().reset(seed=seed)

        # Cria uma nova instância do nosso simulador de mercado
        self.market_model = MarketModel(
            n_chartists=40, n_fundamentalists=40, n_noise=15, n_makers=5,
            real_prices_series=self.real_prices_data
        )

        # Reseta o estado do portfólio
        self.current_step = 0
        self.balance = 10000
        self.shares_held = 0
        self.net_worth = self.balance
        self.total_reward = 0

        # Pega a observação e info iniciais
        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        """Executa um passo no ambiente."""
        # Validação da ação
        if not self.action_space.contains(action):
            raise ValueError(f"Ação inválida: {action}. Deve ser 0, 1 ou 2.")
        
        # Guarda o patrimônio líquido antes da ação para calcular a recompensa
        prev_net_worth = self.net_worth
        
        # --- Executa a Ação do Agente ---
        # 0=Manter, 1=Comprar, 2=Vender
        current_price = self.market_model.current_price
        
        if action == 1: # Comprar
            # Compra o máximo que puder com o saldo
            if self.balance > 0:
                shares_to_buy = self.balance / current_price
                self.shares_held += shares_to_buy
                self.balance = 0
        elif action == 2: # Vender
            # Vende todas as ações que tiver
            if self.shares_held > 0:
                self.balance += self.shares_held * current_price
                self.shares_held = 0

        # --- Avança o Simulador de Mercado ---
        self.market_model.step()
        self.current_step += 1

        # --- Calcula o Estado e a Recompensa ---
        # Atualiza o patrimônio líquido
        self.net_worth = self.balance + (self.shares_held * self.market_model.current_price)
        
        # A recompensa é a mudança no patrimônio líquido
        reward = self.net_worth - prev_net_worth
        self.total_reward += reward

        # --- Prepara o Retorno ---
        observation = self._get_obs()
        info = self._get_info()
        
        # Define se o episódio terminou
        terminated = self.net_worth <= 0 or self.current_step >= self.simulation_steps
        truncated = False # Não estamos usando truncamento por tempo aqui

        return observation, reward, terminated, truncated, info

    def render(self, mode='human'):
        """Renderiza o estado atual (opcional, para visualização)."""
        profit = self.net_worth - 10000
        action_names = ["Manter", "Comprar", "Vender"]
        print(f"Passo: {self.current_step}, "
              f"Patrimônio Líquido: {self.net_worth:.2f}, "
              f"Lucro/Prejuízo: {profit:.2f}, "
              f"Recompensa Total: {self.total_reward:.2f}, "
              f"Preço Atual: ${self.market_model.current_price:.2f}, "
              f"Ações: {self.shares_held:.4f}, "
              f"Saldo: ${self.balance:.2f}")

# --- Bloco de Validação do Ambiente ---
if __name__ == '__main__':
    from stable_baselines3.common.env_checker import check_env

    print("Carregando dados reais para inicializar o ambiente...")
    real_data = load_real_data(os.path.join('data', 'ETH_USDT_1m.parquet'))

    if real_data is not None:
        print("Criando instância do TradingEnv...")
        env = TradingEnv(real_prices_data=real_data)

        print("\nExecutando o validador de ambiente do Stable-Baselines3...")
        # check_env irá rodar uma série de testes para garantir
        # que nosso ambiente segue a interface do Gymnasium corretamente.
        check_env(env)

        print("\n" + "="*50)
        print("Validação do ambiente concluída com sucesso!")
        print("Nosso 'ginásio' está pronto para treinar um agente de IA.")
        print("="*50)