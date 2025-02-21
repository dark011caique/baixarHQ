from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import wget
import re
import subprocess

# Caminho do usuário do Chrome
chrome_user_data_dir = r"C:\Users\Win10\AppData\Local\Google\Chrome\User Data"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Comando para abrir o Chrome no modo de depuração
chrome_command = f'"{chrome_path}" --remote-debugging-port=9222 --user-data-dir="C:\\ChromeDebug"'

try:
    print("Abrindo o navegador no modo de depuração...")
    subprocess.Popen(chrome_command, shell=True)
except Exception as e:
    print(f"Erro ao abrir o Chrome: {e}")

# Configuração do Selenium para se conectar ao Chrome aberto
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:9222")  # Conecta à porta de depuração
options.add_argument(f"user-data-dir={chrome_user_data_dir}")  # Usar o diretório de dados do usuário

# Iniciar WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Abrir a página principal
driver.get("https://timelinecomics.blogspot.com/2016/02/invincible-image.html#google_vignette")
sleep(5)

# Encontrar todas as imagens
links = driver.find_elements(By.XPATH, "//*[@id='post-body-6986350782410519664']//img")

# Criar lista de URLs das imagens e modificar para resolução máxima
image_urls = []
for img in links:
    img_url = img.get_attribute("src")

    # Substituir qualquer tamanho (sXXX) por s1600 para pegar a maior resolução
    img_url_hd = re.sub(r'/s\d+/', '/s1600/', img_url)
    
    image_urls.append(img_url_hd)

print(f"Encontradas {len(image_urls)} imagens para baixar.")

# Baixar as imagens
for index, url in enumerate(image_urls):
    try:
        print(f"Baixando: {url}")
        wget.download(url, out=f"imagem_{index}.jpg")
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

print("\nDownloads concluídos!")
driver.quit()


