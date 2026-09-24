# Monitor de preços da Amazon Brasil

Protótipo em Python que consulta o preço de um produto da Amazon Brasil e permite verificar pelo Telegram se ele chegou ao valor desejado.

## Problema e solução

Encontrar uma oferta no momento certo pode ser difícil. Este projeto demonstra uma forma de consultar o preço de um produto a partir de sua URL, registrar a consulta localmente e apresentar o resultado em uma conversa com um bot do Telegram.

## Como funciona

1. A pessoa inicia o bot com `/start` e escolhe `/adicionar`.
2. O bot solicita uma URL da Amazon Brasil e um preço-alvo.
3. `monitor.py` abre a página com Playwright e procura o preço no HTML usando BeautifulSoup.
4. Quando encontra um preço, o bot o compara com o alvo e responde no Telegram.
5. A consulta é acrescentada a `historico_precos.csv` no diretório de execução.

Cada solicitação faz uma verificação imediata. O protótipo não mantém uma lista persistente de produtos para consultas futuras e não executa verificações periódicas.

## Funcionalidades atuais

- Comandos `/start`, `/adicionar` e `/cancelar` no Telegram.
- Coleta de URL da Amazon Brasil e preço-alvo durante uma conversa.
- Consulta do preço atual por scraping de página.
- Resposta no Telegram com o preço encontrado e indicação quando ele é menor ou igual ao alvo.
- Registro local de data, preço e nome do produto em CSV.
- Script manual `testes.py` que tenta consultar uma lista fixa de produtos da Amazon.

O scraping depende da estrutura atual das páginas da Amazon e pode falhar por mudanças no site, bloqueios ou indisponibilidade da página. `testes.py` acessa a internet e não é uma suíte isolada de testes unitários.

## Tecnologias

- **Python**: implementação do bot e da lógica de consulta.
- **Playwright**: abre a página da Amazon em Chromium headless e aguarda o elemento de preço.
- **BeautifulSoup**: interpreta o HTML carregado e extrai as partes inteira e fracionária do preço.
- **pandas**: monta e acrescenta os registros ao arquivo CSV local.
- **python-telegram-bot**: recebe comandos e mensagens via polling e conduz a conversa com o usuário.
- **python-dotenv**: carrega a configuração local do arquivo `.env`.

Não há banco de dados. O histórico é um arquivo CSV local.

## Requisitos

- Python 3.10 ou superior.
- Um bot do Telegram e seu token, criado pelo [@BotFather](https://t.me/BotFather).
- Acesso à internet para o Telegram e para as páginas da Amazon.

## Instalação e execução

Clone o repositório e entre na pasta do projeto. Os comandos abaixo usam bash:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
playwright install chromium
```

No Windows PowerShell, ative o ambiente com `.venv\Scripts\Activate.ps1`.

Copie `.env.example` para `.env` e preencha o token do bot:

```env
TELEGRAM_BOT_TOKEN=seu_token_do_botfather
```

O `.env` é carregado localmente e está excluído do Git. Não publique nem compartilhe esse arquivo ou o token. Como alternativa, configure `TELEGRAM_BOT_TOKEN` diretamente no ambiente em que o programa será executado.

Inicie o bot:

```bash
python bot.py
```

No Telegram, envie `/start` e depois `/adicionar`. Informe uma URL completa de produto da Amazon Brasil e o preço-alvo. Para encerrar uma etapa da conversa, envie `/cancelar`.

## Execução do script auxiliar

`testes.py` realiza consultas reais para URLs definidas no próprio arquivo e, se todas forem bem-sucedidas, acrescenta os resultados ao histórico. Pode levar algum tempo e depende da rede e do site:

```bash
python testes.py
```

Para testar apenas o scraper diretamente, `monitor.py` também contém uma execução de demonstração com uma URL definida no código:

```bash
python monitor.py
```

## Arquivos do projeto

| Arquivo | Responsabilidade |
| --- | --- |
| `bot.py` | Interface de conversa no Telegram e fluxo de consulta imediata. |
| `monitor.py` | Scraping da Amazon e gravação do histórico CSV. |
| `testes.py` | Verificação manual em lote com URLs fixas e acesso à internet. |
| `requirements.txt` | Dependências Python do projeto. |
| `.env.example` | Modelo local da variável de ambiente necessária ao bot. |

## Limitações conhecidas

- O scraper depende dos seletores HTML usados atualmente pela Amazon e consulta somente páginas da Amazon Brasil.
- O bot faz uma consulta por solicitação; não salva uma lista de produtos nem monitora preços continuamente.
- O histórico fica no diretório de execução e é ignorado pelo Git.
- Os scripts de consulta precisam de Chromium instalado pelo Playwright.
