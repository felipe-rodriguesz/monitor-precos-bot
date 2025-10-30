# Projeto: Monitor de Alertas de Preços

## 1. Problema Identificado

O projeto busca solucionar dois problemas principais:
* Muitos usuários de marketplaces perdem promoções por não as detectarem a tempo, já que elas esgotam rapidamente.
* Cambistas utilizam sistemas automatizados para se aproveitar de variações de preço, prejudicando o usuário final.

## 2. Solução Proposta

Criar uma ferramenta que monitora flutuações de preço em produtos especificados pelo usuário e o notifica quando o valor atingir um limite desejado.

Na sua versão final, a ferramenta será disponibilizada como um bot no Telegram, por onde o usuário poderá controlar quais produtos monitorar e receber os alertas.

## 3. Versão Mínima Atual (Protótipo)

Nesta etapa, o projeto evoluiu de um script de teste para um protótipo funcional com interface de usuário via bot do Telegram. A estrutura atual é:

* **`monitor.py`**: Contém a lógica de "backend".
    * `pegar_preco_amazon()`: Função que utiliza Playwright e BeautifulSoup para extrair o preço atual de um produto.
    * `salvar_historico()`: Função que utiliza Pandas para registrar o preço capturado em um arquivo `historico_precos.csv`.

* **`testes.py`**: (Script auxiliar) Usado pela equipe para testes internos em lote, garantindo que a lógica de `monitor.py` continue funcional.

* **`bot.py`**: Script principal que atua como a **demonstração mínima funcional**.
    * Ele se conecta à API do Telegram e recebe os comandos do usuário.
    * Implementa o comando `/adicionar`, que guia o usuário na inserção de uma URL e um preço-alvo.
    * Ao final, ele chama as funções do `monitor.py` para executar o scraping em tempo real e salvar a primeira verificação no histórico.

## 4. Manual Técnico (Como Executar a Demo do Bot)

Para executar esta demonstração mínima com a interface do bot, siga os passos:

1.  Clone o repositório do GitHub.
2.  Acesse a pasta do projeto e crie/ative um ambiente virtual.
3.  Instale as dependências (incluindo a nova biblioteca do bot):
    ```bash
    pip install -r requirements.txt
    ```
4.  Instale os navegadores necessários para o Playwright:
    ```bash
    playwright install
    ```
5.  **Configurar o Token do Bot:**
    * Abra o arquivo `bot.py`.
    * Encontre a linha que diz: `TOKEN = "COLE_SEU_TOKEN_AQUI"`
    * Substitua `"COLE_SEU_TOKEN_AQUI"` pelo token que você pegou do BotFather.
    * Salve o arquivo.

6.  **Execute o Bot:**
    ```bash
    python bot.py
    ```
7.  **Demonstração:**
    * Abra o aplicativo do Telegram e encontre o bot que você criou.
    * Envie o comando `/start`.
    * Envie o comando `/adicionar` e siga as instruções, enviando uma URL da Amazon e um preço-alvo.
    * O bot irá confirmar e, em seguida, rodar o scraper para buscar o preço atual.