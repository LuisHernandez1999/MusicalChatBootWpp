from config import NUMERO_WHATSAPP, MENSAGEM_INICIAL
from whatsapp import enviar_whatsapp_web

if __name__ == "__main__":
    enviar_whatsapp_web(MENSAGEM_INICIAL, NUMERO_WHATSAPP)