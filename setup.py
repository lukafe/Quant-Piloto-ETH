#!/usr/bin/env python3
"""
Script de setup para o projeto Quant Piloto ETH
Instala dependências e configura o ambiente
"""

import subprocess
import sys
import os

def install_requirements():
    """Instala as dependências do requirements.txt"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_data_directory():
    """Cria o diretório de dados se não existir"""
    if not os.path.exists("data"):
        os.makedirs("data")
        print("📁 Diretório 'data' criado")
    else:
        print("📁 Diretório 'data' já existe")

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatível")
    return True

def main():
    """Função principal do setup"""
    print("🚀 Setup do Quant Piloto ETH")
    print("=" * 40)
    
    # Verificar versão do Python
    if not check_python_version():
        sys.exit(1)
    
    # Criar diretório de dados
    create_data_directory()
    
    # Instalar dependências
    if not install_requirements():
        sys.exit(1)
    
    print("\n🎉 Setup concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. python download_data.py    # Baixar dados históricos")
    print("2. python check_data.py       # Verificar dados")
    print("3. python mfa_advanced.py     # Testar simulação")
    print("4. python trading_env.py      # Testar ambiente de RL")

if __name__ == "__main__":
    main() 