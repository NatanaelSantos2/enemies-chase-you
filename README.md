# 🧱 Roguelike - Projeto de Teste para Tutores Python

Este é um pequeno jogo no estilo **roguelike**, desenvolvido com as bibliotecas (`pgzero`, `math`, `random`, e `pygame.Rect`).

## 🎮 Funcionalidades

- Menu principal com botões clicáveis:
  - Iniciar Jogo
  - Ativar/Desativar Som
  - Sair
- Música de fundo e efeitos sonoros
- Herói com animações de movimento e idle
- Inimigos com comportamento inteligente:
  - Patrulham ou seguem o herói se estiverem próximos
  - Nunca ocupam a mesma célula entre si
- Movimento suave em grade (grid) com animação
- Estrutura clara

## 📦 Requisitos

- Python 3.x
- PgZero (instale com `pip install pgzero`)
- PyGame (instale com `pip install pygame`)

## ▶️ Como Rodar

```bash
pgzrun main.py
