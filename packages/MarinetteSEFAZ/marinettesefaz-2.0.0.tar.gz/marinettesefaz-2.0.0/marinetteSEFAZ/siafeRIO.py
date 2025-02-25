from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def login_siafe(nav: webdriver.Firefox, login, senha_siafe):
    nav.get("https://siafe2.fazenda.rj.gov.br/Siafe/faces/login.jsp")

    usuario = nav.find_element(By.XPATH, value='//*[@id="loginBox:itxUsuario::content"]')
    usuario.send_keys(login)

    senha = nav.find_element(By.XPATH, value='//*[@id="loginBox:itxSenhaAtual::content"]')
    senha.send_keys(senha_siafe)
    
    btn_login = nav.find_element(By.XPATH, value='//*[@id="loginBox:btnConfirmar"]')
    btn_login.click()

    try:
        WebDriverWait(nav,2).until(EC.element_to_be_clickable((By.XPATH, "//a[@class = 'x12k']"))).click()        
    except TimeoutException:
        pass

    nav.maximize_window()
    
    pop_up(nav)
    
def pop_up(nav):
    try:
        WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="pt1:warnMessageDec:newWarnMessagePopup::content"]//*[@id="pt1:warnMessageDec:frmExec:btnNewWarnMessageOK"]'))).click()
    except TimeoutException:
        None