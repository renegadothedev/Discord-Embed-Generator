# Discord Embed Generator

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Sobre o Projeto

O **Discord Embed Generator** é uma ferramenta desktop desenvolvida em Python com PyQt6 que permite criar embeds personalizados para o Discord de forma visual e intuitiva. Com uma interface gráfica amigável, você pode visualizar as alterações em tempo real, facilitando a criação de mensagens ricas e atrativas para seus servidores Discord.

## Funcionalidades Principais

- **Preview em Tempo Real**: Visualize instantaneamente como o embed aparecerá no Discord à medida que você edita.
- **Seletor de Cores**: Escolha cores personalizadas para títulos, descrições e outros elementos usando um seletor intuitivo.
- **Exportação Versátil**: Exporte seus embeds para formatos compatíveis com `discord.py`, `discord.js` e JSON puro.
- **Gerenciamento Dinâmico de Fields**: Adicione, remova e organize campos (fields) de forma dinâmica para estruturar seu embed.
- **Interface Intuitiva**: Design limpo e responsivo para uma experiência de usuário fluida.

## Pré-requisitos

Antes de executar o projeto, certifique-se de que você possui os seguintes requisitos instalados:

- **Python 3.10 ou superior**
- **pip** (gerenciador de pacotes do Python)

## Instalação

Siga os passos abaixo para instalar e configurar o projeto em seu ambiente local:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/renegadothedev/Discord-Embed-Generator.git
   cd Discord-Embed-Generator
   ```

2. **Crie um ambiente virtual** (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## Como Usar

Após a instalação, execute o aplicativo da seguinte forma:

1. Ative o ambiente virtual (se criado):
   ```bash
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. Execute o aplicativo principal:
   ```python
   python main.py
   ```

A interface gráfica será aberta. Use os controles para configurar seu embed:
- Insira o título, descrição e outras propriedades no painel esquerdo.
- Visualize o resultado em tempo real no painel direito.
- Adicione campos dinamicamente e ajuste cores conforme necessário.
- Exporte o embed no formato desejado usando o botão de exportação.

## Estrutura do Projeto

```
Discord-Embed-Generator/
├── main.py                 # Ponto de entrada da aplicação
├── README.md               # Documentação do projeto
├── logic/
│   ├── __init__.py
│   └── exporter.py         # Lógica de exportação para diferentes formatos
├── ui/
│   ├── __init__.py
│   ├── components.py       # Componentes da interface
│   ├── main_window.py      # Janela principal da aplicação
│   └── styles.py           # Estilos e temas da UI
└── utils/
    ├── __init__.py
    └── helpers.py          # Funções utilitárias auxiliares
```

## Captura de Tela

![Captura de Tela do Discord Embed Generator](https://via.placeholder.com/800x600.png?text=Insira+a+imagem+aqui)

*Substitua o link acima pela URL da imagem real da interface do aplicativo.*

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Créditos

Agradecimentos especiais à comunidade Python e PyQt6 por fornecerem ferramentas poderosas para desenvolvimento de aplicações desktop. Inspirado em ferramentas similares para criação de embeds Discord.
