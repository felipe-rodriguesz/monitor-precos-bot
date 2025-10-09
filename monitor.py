from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# URL do produto na Amazon
URL = "https://www.amazon.com.br/Notebook-ANV15-51-7837-Gera%C3%A7%C3%A3o-Nvidia-iluminado/dp/B0DKQ2SSKY/ref=asc_df_B0DKQ2SSKY?mcid=8a8b7c3465bc3933a8da119aaa1fd039&tag=googleshopp00-20&linkCode=df0&hvadid=709884378364&hvpos=&hvnetw=g&hvrand=1003484426730611769&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9102174&hvtargid=pla-2419062133083&psc=1&language=pt_BR&gad_source=4"
HISTORICO = 'historico_precos.csv'

def pegar_preco_amazon(url):
    with sync_playwright() as p:
        # Lança o navegador (modo headless não abre janela visual)
        browser = p.chromium.launch(headless=True)
        
        #Simula um navegador real para evitar bloqueios
        context = browser.new_context(
            user_agent='Chrome/91.0.4472.124'
        )

        # Cria uma nova aba
        page = context.new_page()
        
        # Navega até a URL e espera o conteúdo carregar
        page.goto(url, wait_until='domcontentloaded', timeout=60000)

        # Pega o conteúdo HTML final da página
        pagina_html = page.content()
        browser.close()

    # BeautifulSoup analisa o HTML obtido pelo Playwright
    soup = BeautifulSoup(pagina_html, "html.parser")

    # Encontra o preço inteiro
    preco_inteiro = soup.select_one("span.a-price-whole")
    # Encontra os centavos se tiver
    preco_centavos = soup.select_one("span.a-price-fraction")

    if preco_inteiro:
        preco_texto = preco_inteiro.get_text().strip()

        if preco_centavos:
        # Se encontrar centavos adiciona
            preco_texto += preco_centavos.get_text().strip()
        
        # Remove separadores e converte para float
        preco_formatado = preco_texto.replace(".", "").replace(",", ".")
        preco_num = float(preco_formatado)

        return preco_num
    else:
        return None
    
#Salva ou atualiza o histórico de preços em um arquivo CSV
def salvar_historico(preco_atual):
    
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
    print(f"Histórico de preços salvo em '{HISTORICO}'")
    
if __name__ == "__main__":
    # Define como os números float devem ser exibidos pelo Pandas
    pd.options.display.float_format = '{:.2f}'.format
    preco = pegar_preco_amazon()
    
    if preco:
        print(f"Preço atual: R$ {preco:.2f}")
        salvar_historico(preco)
        
        # Exibe o histórico atualizado no final
        print("\n--- Histórico Completo ---")
        df_final = pd.read_csv(HISTORICO)
        print(df_final)

    else:
        print("Não consegui encontrar o preço na página.")
