# test_trading_env.py

import os
from trading_env import TradingEnv, load_real_data

def test_trading_environment():
    """Testa o ambiente de trading executando alguns passos de simulação."""
    
    print("Carregando dados reais...")
    real_data = load_real_data(os.path.join('data', 'ETH_USDT_1m.parquet'))
    
    if real_data is None:
        print("❌ Erro: Não foi possível carregar os dados reais.")
        return False
    
    print(f"✅ Dados carregados: {len(real_data):,} registros")
    
    print("\nCriando ambiente de trading...")
    env = TradingEnv(real_prices_data=real_data)
    print("✅ Ambiente criado com sucesso")
    
    print(f"\nConfiguração do ambiente:")
    print(f"  - Espaço de ação: {env.action_space}")
    print(f"  - Espaço de observação: {env.observation_space}")
    print(f"  - Tamanho da janela: {env.window_size}")
    
    print("\nExecutando teste de simulação...")
    
    # Reset do ambiente
    observation, info = env.reset()
    print(f"✅ Reset executado. Patrimônio inicial: ${info['net_worth']:.2f}")
    
    # Executar alguns passos
    total_reward = 0
    for step in range(10):
        # Ação aleatória (0=Manter, 1=Comprar, 2=Vender)
        action = env.action_space.sample()
        
        # Executar passo
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        
        # Renderizar estado
        env.render()
        
        if terminated:
            print(f"⚠️  Episódio terminou no passo {step + 1}")
            break
    
    print(f"\n📊 Resumo do teste:")
    print(f"  - Passos executados: {step + 1}")
    print(f"  - Patrimônio final: ${info['net_worth']:.2f}")
    print(f"  - Recompensa total: ${total_reward:.2f}")
    print(f"  - Lucro/Prejuízo: ${info['net_worth'] - 10000:.2f}")
    
    print("\n🎉 Teste do ambiente de trading concluído com sucesso!")
    return True

if __name__ == "__main__":
    test_trading_environment() 