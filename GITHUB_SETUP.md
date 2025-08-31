# 🚀 Guia para Configurar o Repositório no GitHub

Este guia te ajudará a colocar o projeto **Quant Piloto ETH** no GitHub.

## 📋 Pré-requisitos

1. **Conta no GitHub**: [github.com](https://github.com)
2. **Git instalado**: [git-scm.com](https://git-scm.com/downloads)
3. **Python 3.8+**: Já deve estar instalado

## 🔧 Passo a Passo

### 1. Inicializar o Repositório Git Local

Execute o script de inicialização:

```bash
python init_git.py
```

Isso irá:
- ✅ Inicializar o repositório Git
- ✅ Adicionar todos os arquivos
- ✅ Fazer o commit inicial

### 2. Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Configure o repositório:
   - **Repository name**: `quant-piloto-eth` (ou outro nome)
   - **Description**: `Simulação de mercado de criptomoedas usando modelagem baseada em agentes`
   - **Visibility**: Public ou Private (sua escolha)
   - **❌ NÃO marque**: "Add a README file"
   - **❌ NÃO marque**: "Add .gitignore"
   - **❌ NÃO marque**: "Choose a license"
3. Clique em **"Create repository"**

### 3. Conectar com o GitHub

Após criar o repositório, o GitHub mostrará comandos. Execute:

```bash
# Renomear branch para main
git branch -M main

# Adicionar remote (substitua SEU_USUARIO pelo seu username)
git remote add origin https://github.com/SEU_USUARIO/quant-piloto-eth.git

# Enviar para o GitHub
git push -u origin main
```

### 4. Verificar (Opcional)

Se você quiser fazer tudo de uma vez, pode usar o script com a URL do repositório:

```bash
python init_git.py https://github.com/SEU_USUARIO/quant-piloto-eth.git
```

## 📁 Estrutura que será enviada

```
quant-piloto-eth/
├── README.md              # Documentação principal
├── requirements.txt       # Dependências Python
├── setup.py              # Script de instalação
├── .gitignore            # Arquivos ignorados pelo Git
├── LICENSE               # Licença MIT
├── init_git.py           # Script de inicialização Git
├── download_data.py      # Download de dados históricos
├── check_data.py         # Verificação de dados
├── view_data.py          # Visualização de dados
├── mfa_advanced.py       # Modelo de simulação avançado
├── trading_env.py        # Ambiente de RL
├── test_trading_env.py   # Testes do ambiente
└── data/                 # Diretório de dados (vazio)
```

## 🎯 Após o Upload

1. **README.md** será exibido na página principal
2. **Badges** podem ser adicionados (build status, versão, etc.)
3. **Issues** podem ser criados para bugs/features
4. **Releases** podem ser feitos para versões estáveis

## 🔄 Atualizações Futuras

Para enviar atualizações:

```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

## 📊 GitHub Pages (Opcional)

Para criar uma página web do projeto:

1. Vá em **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** → **/ (root)**
4. Salve

## 🏷️ Tags e Releases

Para criar uma versão:

```bash
git tag -a v1.0.0 -m "Versão 1.0.0"
git push origin v1.0.0
```

## 📈 Estatísticas do Repositório

O GitHub mostrará automaticamente:
- ⭐ Stars
- 👀 Views
- 📥 Downloads
- 🔄 Forks

## 🆘 Problemas Comuns

### Erro de Autenticação
```bash
# Configurar credenciais
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### Erro de Push
```bash
# Se o repositório já existe
git pull origin main --allow-unrelated-histories
git push origin main
```

### Arquivo Grande
Se o arquivo de dados for muito grande:
```bash
# Adicionar ao .gitignore
echo "data/*.parquet" >> .gitignore
```

---

**🎉 Parabéns! Seu projeto está no GitHub e pronto para ser compartilhado!** 