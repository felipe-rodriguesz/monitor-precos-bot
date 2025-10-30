from monitor import pegar_preco_amazon, salvar_historico
import pandas as pd
import asyncio

precos_coletados = [] 

async def test_pegar_precos_amazon():

    urls = [
        'https://www.amazon.com.br/TechnicTM-Corrida-McLaren-Formula-Constru%C3%A7%C3%A3o/dp/B09JKXYLH7?pd_rd_w=Xx8Cr&content-id=amzn1.sym.edd089b0-afd7-4e66-b221-63bb484cb7a5&pf_rd_p=edd089b0-afd7-4e66-b221-63bb484cb7a5&pf_rd_r=X5RDKFK5GDAVBYE5DTD7&pd_rd_wg=KpDx7&pd_rd_r=485a6a2e-3dad-49e4-9046-98fb6a0bb745&pd_rd_i=B09JKXYLH7',
        'https://www.amazon.com.br/dp/B0DF85X82B/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B0DF85X82B&pd_rd_w=xQ8ue&content-id=amzn1.sym.1868afab-d777-4b70-8899-1b323ad91d95&pf_rd_p=1868afab-d777-4b70-8899-1b323ad91d95&pf_rd_r=F182C0MK6P0KZJ93NBF3&pd_rd_wg=OilN7&pd_rd_r=7cbbf237-0629-4e6d-96b7-7752110fe042&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw',
        'https://www.amazon.com.br/LEGO-Fortnite-Conjunto-Constru%C3%A7%C3%A3o-Videogame/dp/B0DF842F5D/ref=pd_sbs_d_sccl_1_3/140-2650908-9240519?pd_rd_w=u8zjI&content-id=amzn1.sym.53b2f13e-ab3a-40f2-aab9-7e4b988d3762&pf_rd_p=53b2f13e-ab3a-40f2-aab9-7e4b988d3762&pf_rd_r=BBGS892G062AQ4S9QT8S&pd_rd_wg=AQ527&pd_rd_r=7bc13915-8c74-4877-971f-c064d951d0b4&pd_rd_i=B0DF842F5D&psc=1',
        'https://www.amazon.com.br/Echo-Pop-Cor-Preta/dp/B09WXVH7WK?ref=dlx_prime_dg_dcl_B09WXVH7WK_dt_sl7_f7_pi&pf_rd_r=A6T2QXREJM67R74ZHJBD&pf_rd_p=c3796354-b594-4c87-afa1-4368b4265cf7',
        'https://www.amazon.com.br/L%C3%A2mpada-Inteligente-Elgin-compat%C3%ADvel-Google/dp/B088C4QZV2/?_encoding=UTF8&pd_rd_w=YAOIz&content-id=amzn1.sym.fe9dbfab-b1f9-4d7e-bf05-e5e61433e9e9&pf_rd_p=fe9dbfab-b1f9-4d7e-bf05-e5e61433e9e9&pf_rd_r=MPPS73HCXSY2P32FPZV2&pd_rd_wg=zAz1q&pd_rd_r=1bb73a0a-0bf3-496f-8d5d-9b216b95eaae&ref_=pd_hp_d_atf_dealz_m1&th=1'
    ]   

    sucesso = True

    for link in urls:
        preco = await pegar_preco_amazon(link)
        precos_coletados.append(preco)

        if preco is None:
            print(f"Falha ao buscar preço para: {link}")
            sucesso = False
        else:
            print(f"Preço encontrado: R$ {preco:.2f}")
    
    if sucesso:
        print("Sucesso na função de pegar preços! ✅\n")
    else:
        print("\nAlguns preços não foram encontrados. ❌")

    return sucesso

async def test_salvar_historico():

    if (not await test_pegar_precos_amazon()):
        print("Não há preços válidos para salvar. Teste de salvamento abortado.")
        return False

    if not precos_coletados or any(p is None for p in precos_coletados):
        print("Não há preços válidos para salvar. Teste de salvamento abortado.")
        return False

    for p in precos_coletados:
        if p is not None:
            salvar_historico(p, "Produto Teste")
            
    print("Sucesso na função de salvar histórico! ✅")
    return True

async def main_test():
    if await test_salvar_historico():
        print("\nTODOS OS TESTES UNITÁRIOS CONCLUÍDOS COM SUCESSO ✅\n")
    else:
        print("\nERRO NA EXECUÇÃO DOS TESTES ❌\n")

if __name__ == "__main__":
    pd.options.display.float_format = '{:.2f}'.format

    asyncio.run(main_test())