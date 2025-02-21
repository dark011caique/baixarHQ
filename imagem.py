from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from time import sleep
import wget
import re


# Iniciar WebDriver
driver = webdriver.Chrome()

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


