from playwright.async_api import async_playwright, Error
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

HISTORICO = 'historico_precos.csv'

async def pegar_preco_amazon(url):
    async with async_playwright() as p:
        # Lança o navegador (modo headless não abre janela visual)
        browser = await p.chromium.launch(headless=True)
        
        #Simula um navegador real para evitar bloqueios
        context = await browser.new_context(
            user_agent = 'Chrome/91.0.4472.124'
        )

        # Cria uma nova aba
        page = await context.new_page()
        
        try:
            # Navega até a URL e espera o conteúdo carregar
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            await page.wait_for_selector("span.a-price-whole", timeout=20000)
            
            # Pega o conteúdo HTML final da página
            pagina_html = await page.content()
        except Error as e:
            print(f"Erro ao acessar {url}: {e}")
            return None
        finally:
            await browser.close()

    # BeautifulSoup analisa o HTML obtido pelo Playwright
    soup = BeautifulSoup(pagina_html, "html.parser")

    # Encontra o preço inteiro
    preco_inteiro = soup.select_one("span.a-price-whole")
    # Encontra os centavos se tiver
    preco_centavos = soup.select_one("span.a-price-fraction")

    if preco_inteiro:
        preco_texto = preco_inteiro.get_text(strip=True)
        if preco_centavos:
            preco_texto += preco_centavos.get_text(strip=True)
        
        preco_formatado = preco_texto.replace(".", "").replace(",", ".")
        try:
            return float(preco_formatado)
        except ValueError:
            print(f"Não foi possível converter o preço '{preco_formatado}' para número.")
            return None
    else:
        print(f"Preço não encontrado na URL: {url}")
        return None
    
#Salva ou atualiza o histórico de preços em um arquivo CSV
def salvar_historico(preco_atual, nome_produto="Produto"):
    
    # Cria um DataFrame com o dado mais recente
    timestamp = datetime.now()
    novo_dado_df = pd.DataFrame([{
        'data_hora': timestamp,
        'preco_rs': preco_atual
    }])

    # Verifica se o arquivo de histórico já existe
    if os.path.exists(HISTORICO):
        # Se existe, carrega os dados antigos
        historico_df = pd.read_csv(HISTORICO)
        # Concatena os dados antigos com o novo
        historico_atualizado_df = pd.concat([historico_df, novo_dado_df], ignore_index=True)
    else:
        # Se não existe, o novo dado é o histórico completo
        historico_atualizado_df = novo_dado_df

    # Salva o DataFrame atualizado no arquivo CSV, sem o índice
    historico_atualizado_df.to_csv(HISTORICO, index=False)
    
if __name__ == "__main__":
    import asyncio
    URL_TESTE = "https://www.amazon.com.br/Notebook-ANV15-51-7837-Gera%C3%A7%C3%A3o-Nvidia-iluminado/dp/B0DKQ2SSKY/"

    async def testar_monitor():
        # Define como os números float devem ser exibidos pelo Pandas
        pd.options.display.float_format = '{:.2f}'.format
        preco = await pegar_preco_amazon(URL_TESTE)
    
        if preco:
            print(f"Preço atual: R$ {preco:.2f}")
            salvar_historico(preco, "Notebook Gamer")
            print("Histórico salvo com sucesso.")
        else:
            print("Não foi possível obtero o preço.")
    asyncio.run(testar_monitor())