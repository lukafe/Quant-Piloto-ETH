#!/usr/bin/env python3
"""
Script para inicializar o repositório Git e preparar para o GitHub
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Executa um comando e trata erros"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        if e.stdout:
            print(f"Saída: {e.stdout}")
        if e.stderr:
            print(f"Erro: {e.stderr}")
        return False

def check_git_installed():
    """Verifica se o Git está instalado"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git_repository():
    """Inicializa o repositório Git"""
    print("🚀 Inicializando repositório Git para Quant Piloto ETH")
    print("=" * 50)
    
    # Verificar se Git está instalado
    if not check_git_installed():
        print("❌ Git não está instalado. Por favor, instale o Git primeiro:")
        print("   https://git-scm.com/downloads")
        return False
    
    # Inicializar repositório Git
    if not run_command("git init", "Inicializando repositório Git"):
        return False
    
    # Adicionar arquivos
    if not run_command("git add .", "Adicionando arquivos ao staging"):
        return False
    
    # Commit inicial
    if not run_command('git commit -m "Initial commit: Quant Piloto ETH - Simulação de Mercado com Agentes"', "Fazendo commit inicial"):
        return False
    
    print("\n🎉 Repositório Git inicializado com sucesso!")
    print("\n📋 Próximos passos para o GitHub:")
    print("1. Vá para https://github.com/new")
    print("2. Crie um novo repositório (ex: quant-piloto-eth)")
    print("3. NÃO inicialize com README, .gitignore ou LICENSE (já temos)")
    print("4. Execute os comandos que aparecerão na tela:")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/SEU_USUARIO/quant-piloto-eth.git")
    print("   git push -u origin main")
    
    return True

def setup_github_remote(repo_url):
    """Configura o remote do GitHub"""
    print(f"\n🔗 Configurando remote do GitHub: {repo_url}")
    
    if not run_command(f"git remote add origin {repo_url}", "Adicionando remote origin"):
        return False
    
    if not run_command("git branch -M main", "Renomeando branch para main"):
        return False
    
    if not run_command("git push -u origin main", "Fazendo push inicial"):
        return False
    
    print("🎉 Repositório enviado para o GitHub com sucesso!")
    return True

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        # Se foi fornecido URL do repositório
        repo_url = sys.argv[1]
        if not init_git_repository():
            sys.exit(1)
        if not setup_github_remote(repo_url):
            sys.exit(1)
    else:
        # Apenas inicializar Git
        if not init_git_repository():
            sys.exit(1)

if __name__ == "__main__":
    main() 