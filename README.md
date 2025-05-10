# Open Flow

Open Flow é uma aplicação de transcrição automática de áudio para texto, focada em usabilidade e produtividade. O projeto permite gravar áudio do microfone, transcrever automaticamente utilizando modelos de IA (Whisper), e colar o texto transcrito diretamente onde o usuário estiver digitando, tudo isso com um atalho de teclado e rodando em background na bandeja do sistema.

## Funcionalidades
- Gravação de áudio via atalho de teclado configurável
- Transcrição automática utilizando o modelo Whisper
- Copia e cola automática do texto transcrito
- Interface discreta na bandeja do sistema (System Tray)
- Suporte ao idioma Português

## Como funciona
1. O usuário pressiona o atalho de teclado (`Ctrl+Alt` por padrão) para iniciar a gravação.
2. Pressiona novamente o atalho para parar a gravação.
3. O áudio é transcrito automaticamente e o texto é colado na área de trabalho ativa.
4. O programa permanece rodando em background, acessível pela bandeja do sistema.

## Estrutura do Projeto
```
open-flow/
├── main.py                # Ponto de entrada da aplicação
├── pyproject.toml         # Configuração e dependências do projeto
├── src/
│   ├── core/
│   │   ├── transcriber.py     # Lógica de gravação e transcrição
│   │   └── system_tray.py    # Integração com a bandeja do sistema
│   ├── config/
│   │   └── settings.py       # Configurações principais (atalho, modelo, idioma)
│   ├── utils/                # (Reservado para utilitários)
│   └── __init__.py
├── resources/
│   └── icons/                # Ícones para a bandeja do sistema (pasta reservada)
└── README.md
```

## Observações
- O projeto está em fase inicial e pode ser expandido para suportar outros idiomas, atalhos customizáveis e integração com outros sistemas.
- Para adicionar um ícone personalizado à bandeja, coloque um arquivo de imagem em `resources/icons/` e ajuste o caminho em `system_tray.py`.

---

## Roadmap

- [ ] Criar um instalador para o aplicativo (provavelmente usando o PyInstaller)
- [ ] Adicionar a possibilidade de transcrever usando o serviço online da OpenAI
- [ ] Adicionar a capacidade de revisão de transcrição através de um Large Language Model (LLM)
- [ ] Implementar uma tela de configuração para o usuário:
  - [ ] Permitir definir um prompt base para orientar como os textos serão transcritos e revisados
  - [ ] Permitir criar e editar uma lista de palavras que devem ser transcritas/traduzidas de forma específica
  - [ ] Permitir escolha entre modelo local ou serviço online (OpenAI) para transcrição
  - [ ] Permitir escolha de idioma
  - [ ] Permitir escolha do tamanho do modelo de transcrição
  - [ ] Permitir visualizar e gerenciar o histórico de transcrições
- [ ] Adicionar um modo de edição em que o usuário pode copiar um texto selecionado e modificá-lo conforme instruções dadas via áudio

Esses itens estão planejados para as próximas versões e ajudarão a tornar o Open Flow ainda mais completo e personalizável.

Desenvolvido por Fiori Bazarello.
