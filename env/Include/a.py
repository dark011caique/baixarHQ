from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import wget
import re

# Função para extrair o ID da URL
def extrair_id(url):
    padrao = r'(?<=/d/)[^/]*'
    match = re.search(padrao, url)
    return match.group(0) if match else None

# Iniciar o WebDriver
driver = webdriver.Chrome()

# Abrir a página principal
driver.get("https://timelinecomics.blogspot.com/2016/02/invincible-image.html#google_vignette")
sleep(5)

# Encontrar todos os links com target="_blank"
links = driver.find_elements(By.XPATH, "//a[@target='_blank']")
sleep(3)

# Iterar sobre os links encontrados
for index, link in enumerate(links):
    # Abrir o link em uma nova aba
    link.click()
    sleep(5)  # Esperar a página carregar

    # Mudar para a nova aba
    driver.switch_to.window(driver.window_handles[-1])
    sleep(3)

    # Capturar a URL atual
    download_url = driver.current_url
    print(f"Baixando de: {download_url}")

    # Extrair o ID da URL
    arquivo_id = extrair_id(download_url)
    if arquivo_id:
        link_download = f"https://drive.usercontent.google.com/u/0/uc?id={arquivo_id}&export=download&resourcekey=0-P3NIZb8l-GzDgmtufc6wiA"
        print(f"Link para download: {link_download}")

        # Nome do arquivo (evitar sobrescrever)
        output_file = f"Invincible - 2003{index}.pdf"

        # Baixar o arquivo com wget
        wget.download(link_download, out=output_file)
    else:
        print("ID do arquivo não encontrado.")

    # Fechar a aba atual
    driver.close()
    
    # Voltar para a aba original
    driver.switch_to.window(driver.window_handles[0])

    sleep(10)

print("\nDownloads concluídos!")
driver.quit()
