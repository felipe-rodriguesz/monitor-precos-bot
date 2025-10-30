import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from monitor import pegar_preco_amazon, salvar_historico

# Configura o logging para ver erros no terminal
logging.basicConfig( format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO)
logger = logging.getLogger(__name__)

# Estados da conversa com o usuário
(STATE_URL, STATE_PRECO) = range(2)

#------ Comandos do Bot ------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    await update.message.reply_html(
        f"Olá, {user.mention_html()}! 👋\n\n"
        "Eu sou seu assistente de monitoramento de preços.\n\n"
        "Envie /adicionar para começar a monitorar um novo produto.\n"
        "Envie /cancelar a qualquer momento para parar uma operação."
    )
    return ConversationHandler.END

async def adicionar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Certo! Por favor, me envie a URL completa do produto na Amazon que você quer monitorar."
    )
    return STATE_URL

async def receber_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    url_recebida = update.message.text
    
    if "amazon.com.br" not in url_recebida:
        await update.message.reply_text(
            "Essa não parece ser uma URL válida da Amazon Brasil. 🧐\n"
            "Por favor, tente novamente ou envie /cancelar."
        )
        return STATE_URL

    context.user_data['url_para_monitorar'] = url_recebida
    
    await update.message.reply_text(
        "Ótimo! Agora, qual é o preço-alvo que você deseja? \n"
        "Quando o produto atingir esse valor (ou menos), você será notificado.\n\n"
        "Envie apenas o número (ex: 4999.90)"
    )
    return STATE_PRECO


async def receber_preco(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    preco_texto = update.message.text
    
    try:
        preco_desejado = float(preco_texto.replace(",", "."))
    except ValueError:
        await update.message.reply_text(
            "Isso não parece ser um número válido. 😕\n"
            "Por favor, envie apenas o número (ex: 350.50) ou /cancelar."
        )
        return STATE_PRECO

    context.user_data['preco_desejado'] = preco_desejado
    url = context.user_data['url_para_monitorar']
    user = update.effective_user

    await update.message.reply_text(
        f"Perfeito! Produto adicionado.\n"
        f"🎯 Preço-alvo: R$ {preco_desejado:.2f}\n\n"
        "Estou fazendo a **primeira verificação** agora mesmo... 🤖\n"
        "Isso pode levar até 1 minuto."
    )

    # --- INTEGRAÇÃO COM  O SCRAPER ---
    preco_atual = await pegar_preco_amazon(url)
    
    if preco_atual is not None:
        salvar_historico(preco_atual, "Produto_do_Bot")
        
        await update.message.reply_text(
            f"✅ Verificação Concluída!\n\n"
            f"O preço atual do produto é R$ {preco_atual:.2f}.\n\n"
            f"(Seu alvo é R$ {preco_desejado:.2f})"
        )
        
        # Lógica de notificação (para o futuro, mas já podemos checar)
        if preco_atual <= preco_desejado:
            await update.message.reply_text(
                "🎉 Opa! O preço atual já é menor ou igual ao seu alvo! 🎉"
            )
    else:
        await update.message.reply_text(
            "❌ Erro na Verificação\n"
            "Não consegui encontrar o preço na página. "
            "Verifique a URL e tente adicionar o produto novamente."
        )
    
    context.user_data.clear()
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Operação cancelada.", reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END

def main() -> None:
    
    TOKEN = "COLE_SEU_TOKEN_AQUI"
        
    application = Application.builder().token(TOKEN).build()

    # --- Cria o Handler de Conversa ---
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("adicionar", adicionar)],
        states={
            STATE_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_url)],
            STATE_PRECO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_preco)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("cancelar", cancelar))

    print("Bot iniciado! Pressione Ctrl+C para parar.")
    application.run_polling()

if __name__ == "__main__":
    main()