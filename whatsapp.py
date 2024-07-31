import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import NUMERO_WHATSAPP
from youtube import get_youtube_playlist

def localizar_elemento(navegador, xpath):
    """Localiza um elemento usando XPath e retorna o WebElement."""
    return navegador.find_element(By.XPATH, xpath)

def enviar_whatsapp_web(mensagem, numero):
    """Envia uma mensagem inicial pelo WhatsApp Web."""
    chrome_driver_path = r'C:\Users\Usuario\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--remote-debugging-port=9222")
    service = Service(chrome_driver_path)
    navegador = webdriver.Chrome(service=service, options=chrome_options)
    navegador.get("https://web.whatsapp.com/")
    try:
        wait = WebDriverWait(navegador, 120)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        print("QR Code escaneado com sucesso.")
        search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
        search_box = navegador.find_element(By.XPATH, search_xpath)
        search_box.send_keys(numero)
        time.sleep(5)
        search_box.send_keys(Keys.RETURN)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')))
        print("Campo de mensagem encontrado.")
        input_box_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
        input_box = localizar_elemento(navegador, input_box_xpath)
        action = ActionChains(navegador)
        action.move_to_element(input_box).click().send_keys(mensagem).send_keys(Keys.RETURN).perform()
        print("Mensagem inicial enviada com sucesso.")
        esperar_resposta_e_enviar_playlist(navegador, wait, input_box_xpath)
    except TimeoutException:
        print("Tempo de espera expirado. Elemento não encontrado.")
    except NoSuchElementException:
        print("Elemento não encontrado. Verifique o XPath utilizado.")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
    finally:
        time.sleep(120)
        navegador.quit()

def identificar_vibe(mensagem_texto):
    """Identifica a vibe do usuário com base em palavras-chave e variações."""
    mensagem_texto = mensagem_texto.lower()
    if any(v in mensagem_texto for v in ["triste", "deprimido", "desanimado", "muito triste", "bad", "mal"]):
        return "triste"
    elif any(v in mensagem_texto for v in ["feliz", "alegre", "animado", "muito feliz", "good", "bom"]):
        return "feliz"
    elif any(v in mensagem_texto for v in ["reflexiva", "pensativo", "pensativa", "reflexão", "ponderativo"]):
        return "reflexiva"
    elif any(v in mensagem_texto for v in ["animada", "entusiasmado", "animado", "eufórico", "empolgado"]):
        return "animada"
    else:
        return None

def esperar_resposta_e_enviar_playlist(navegador, wait, input_box_xpath):
    """Espera pela resposta do usuário e envia uma playlist com base na vibe identificada."""
    try:
        ultima_mensagem_xpath = '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[last()]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span'
        vibe = None
        ultima_mensagem_texto = ""

        while True:
            try:
                ultima_mensagem = wait.until(EC.presence_of_element_located((By.XPATH, ultima_mensagem_xpath)))
                mensagem_texto = ultima_mensagem.text.lower()
                if mensagem_texto == ultima_mensagem_texto:
                    continue
                ultima_mensagem_texto = mensagem_texto
                print(f"Mensagem recebida: {mensagem_texto}")

                if mensagem_texto == "oi, sou baby joe! como está sua vibe hoje? triste, feliz, reflexiva ou animada?":
                    continue

                vibe = identificar_vibe(mensagem_texto)
                if vibe:
                    print(f"Vibe identificada: {vibe}")
                    break
                time.sleep(5)
            except TimeoutException:
                continue

        if vibe:
            playlist = get_youtube_playlist(vibe)
            for video in playlist:
                try:
                    input_box = localizar_elemento(navegador, input_box_xpath)
                    action = ActionChains(navegador)
                    action.move_to_element(input_box).click().send_keys(video).send_keys(Keys.RETURN).perform()
                    time.sleep(2)  # Espera entre o envio de cada vídeo
                except Exception as e:
                    print(f"Erro ao enviar vídeo: {e}")
            print("Playlist enviada com sucesso.")
            input_box = localizar_elemento(navegador, input_box_xpath)
            action = ActionChains(navegador)
            action.move_to_element(input_box).click().send_keys("Aproveite a playlist! Curta essas músicas e relaxe! 🎶😎").send_keys(Keys.RETURN).perform()
            time.sleep(5)  # Espera antes de enviar a próxima mensagem
            input_box = localizar_elemento(navegador, input_box_xpath)
            action = ActionChains(navegador)
            action.move_to_element(input_box).click().send_keys("Quer mais músicas? Deixe-me saber!").send_keys(Keys.RETURN).perform()
            esperar_resposta_para_nova_playlist(navegador, wait, input_box_xpath, vibe)
        else:
            print("Não consegui identificar a vibe do usuário.")
            esperar_resposta_para_nova_playlist(navegador, wait, input_box_xpath, vibe)
        
    except NoSuchElementException as e:
        print(f"Erro ao procurar elemento: {e}")
    except Exception as e:
        print(f"Erro geral: {e}")

def esperar_resposta_para_nova_playlist(navegador, wait, input_box_xpath, vibe):
    """Espera pela resposta do usuário e envia uma nova playlist ou encerra a interação."""
    resposta_dada = False  # Flag para verificar se já enviou uma nova playlist
    ultima_mensagem_texto = ""
    while True:
        try:
            ultima_mensagem_xpath = '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[last()]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span'
            ultima_mensagem = wait.until(EC.presence_of_element_located((By.XPATH, ultima_mensagem_xpath)))
            mensagem_texto = ultima_mensagem.text.lower()
            if mensagem_texto == ultima_mensagem_texto:
                continue
            ultima_mensagem_texto = mensagem_texto
            print(f"Nova mensagem recebida: {mensagem_texto}")

            if any(negacao in mensagem_texto for negacao in ["não", "nao", "n", "negativo", "no"]):
                input_box = localizar_elemento(navegador, input_box_xpath)
                action = ActionChains(navegador)
                action.move_to_element(input_box).click().send_keys("Valeu por usar o Baby Joe! Até a próxima! 👋").send_keys(Keys.RETURN).perform()
                print("Mensagem de despedida enviada.")
                break
            elif "sim" in mensagem_texto:
                if not resposta_dada:  # Verifica se já enviou uma nova playlist
                    nova_playlist = get_youtube_playlist(vibe)
                    for video in nova_playlist:
                        try:
                            input_box = localizar_elemento(navegador, input_box_xpath)
                            action = ActionChains(navegador)
                            action.move_to_element(input_box).click().send_keys(video).send_keys(Keys.RETURN).perform()
                            time.sleep(2)
                        except Exception as e:
                            print(f"Erro ao enviar vídeo: {e}")
                    print("Nova playlist enviada com sucesso.")
                    input_box = localizar_elemento(navegador, input_box_xpath)
                    action = ActionChains(navegador)
                    action.move_to_element(input_box).click().send_keys("Aqui vai mais uma dose de música boa! Aproveite! 🎵😊").send_keys(Keys.RETURN).perform()
                    time.sleep(5)
                    input_box = localizar_elemento(navegador, input_box_xpath)
                    action = ActionChains(navegador)
                    action.move_to_element(input_box).click().send_keys("Quer mais músicas? Deixe-me saber!").send_keys(Keys.RETURN).perform()
                    resposta_dada = True  # Marca que a nova playlist foi enviada
                    print("Mensagem de nova playlist enviada.")
                else:
                    # Se já enviou uma nova playlist, encerra a interação
                    input_box = localizar_elemento(navegador, input_box_xpath)
                    action = ActionChains(navegador)
                    action.move_to_element(input_box).click().send_keys("Valeu por usar o Baby Joe! Até a próxima! 👋").send_keys(Keys.RETURN).perform()
                    print("Mensagem de despedida enviada.")
                    break
            time.sleep(5)  # Aguarda antes de verificar novas mensagens
        except TimeoutException:
            continue

if __name__ == "__main__":
    mensagem_inicial = "Oi, sou Baby Joe! Como está sua vibe hoje? Triste, feliz, reflexiva ou animada?"
    enviar_whatsapp_web(mensagem_inicial, NUMERO_WHATSAPP)
