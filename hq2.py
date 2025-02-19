import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import re
import subprocess

# Função para extrair o ID da URL
def extrair_id(url):
    padrao = r'(?<=/d/)[^/]*'
    match = re.search(padrao, url)
    return match.group(0) if match else None

def baixar_arquivo(url, nome_arquivo):
    session = requests.Session()
    response = session.get(url, stream=True)
    
    # Verifique se o download foi bem-sucedido
    if response.status_code == 200:
        with open(nome_arquivo, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Arquivo {nome_arquivo} baixado com sucesso!")
    else:
        print(f"Erro ao baixar o arquivo: {response.status_code}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_command = f'"{chrome_path}" --remote-debugging-port=9222 --user-data-dir="C:\\ChromeDebug"'

try:
    print("Abrindo o navegador no modo de depuração...")
    subprocess.Popen(chrome_command, shell=True)
except Exception as e:
    print(f"Erro ao abrir o Chrome: {e}")

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:9222")  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://timelinecomics.blogspot.com/2016/02/invincible-image.html#google_vignette")
sleep(5)

links = driver.find_elements(By.XPATH, "//a[@target='_blank']")
sleep(3)

for index, link in enumerate(links):
    link.click()
    sleep(5)  

    driver.switch_to.window(driver.window_handles[-1])
    sleep(3)

    download_url = driver.current_url
    print(f"Baixando de: {download_url}")

    arquivo_id = extrair_id(download_url)
    if arquivo_id:
        link_download = f"https://drive.usercontent.google.com/u/0/uc?id={arquivo_id}&export=download"
        print(f"Link para download: {link_download}")

        output_file = f"Invincible - {index}.pdf"
        
        # Usar a função de download com requests
        baixar_arquivo(link_download, output_file)
    else:
        print("ID do arquivo não encontrado.")

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    sleep(10)

print("\nDownloads concluídos!")
driver.quit()
