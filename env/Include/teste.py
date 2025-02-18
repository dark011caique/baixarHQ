from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import wget

# Iniciar o WebDriver
driver = webdriver.Chrome()

# Abrir a página principal
driver.get("https://drive.usercontent.google.com/u/0/uc?id=0B8S09qODXLIHb2xBVVo4T0xxcGM&export=download&resourcekey=0-P3NIZb8l-GzDgmtufc6wiA")
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

    # Nome do arquivo (evitar sobrescrever)
    output_file = f"arquivo_{index}.pdf"

    # Baixar o arquivo com wget
    wget.download(download_url, out=output_file)

    # Fechar a aba atual
    driver.close()
    
    # Voltar para a aba original
    driver.switch_to.window(driver.window_handles[0])

    sleep(10)

print("\nDownloads concluídos!")
driver.quit()
