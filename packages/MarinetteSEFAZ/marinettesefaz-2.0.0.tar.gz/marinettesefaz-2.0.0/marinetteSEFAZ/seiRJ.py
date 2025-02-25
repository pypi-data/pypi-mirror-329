import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,ElementNotInteractableException,NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
import re
from re import Match
from datetime import date

LINHA_SEI =  "//tbody//tr"
FECHAR_ABA_SEI = "//div[@class = 'sparkling-modal-close']"


class Processo:
    """
    Classe pra representar um processo SEI
    
    Attributes:
        numero(str): Número do processo SEI.
        elemento(WebElement): WebElement que representa esse processo num bloco. Seu XPATH é "//tbody//tr[@id='trPos0']".
        texto(str): O texto dentro do elemento de processo.
        link(WebElement): O link que abre o processo.
    """
    
    
    def __init__(self,numero,elemento,texto,link):
        self.numero = numero
        self.texto = texto
        self.elemento = elemento
        self.link = link

    def abrir(self):
        """
        Clica no processo pra abrir ele.
        """
        
        self.link.click()
        
class CaixaDeTextoCheiaException(Exception):
    """Caixa de Texto Cheia"""
    
class ElementoNaoEncontradoException(Exception):
    """Elemento não encontrado"""

class BlocoNaoEncontradoException(Exception):
    """Bloco não encontrado"""

class CondicaoNaoEncontradaException(Exception):
    """Condição de XPATH não encontrada"""

class ProcessoJaIncluidoException(Exception):
    """Processo já se enconrta no bloco interno"""

def login_sei(nav: webdriver.Firefox, login:str, senha:str,nome_coordenacao:str = None) -> None:
    """
    Loga no SEI-RJ e, caso necessário, troca a coordenação.
    
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        login (str): Login do usuário.
        senha (str): Senha do usuário.
        nome_coordenacao (str): Nome da coordenação a ser trocada (default = None).
    """
    nav.get("https://sei.rj.gov.br/sip/login.php?sigla_orgao_sistema=ERJ&sigla_sistema=SEI")
    
    usuario = nav.find_element(By.XPATH, value='//*[@id="txtUsuario"]')
    usuario.send_keys(login)

    campo_senha = nav.find_element(By.XPATH, value='//*[@id="pwdSenha"]')
    campo_senha.send_keys(senha)

    exercicio = Select(nav.find_element(By.XPATH, value='//*[@id="selOrgao"]'))
    exercicio.select_by_visible_text('SEFAZ')

    btn_login = nav.find_element(By.XPATH, value='//*[@id="Acessar"]')
    btn_login.click()

    nav.maximize_window()
    
    WebDriverWait(nav,8).until(EC.presence_of_element_located, (By.XPATH, "//div[text() = 'Controle de Processos']"))
    
    nav.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE) 
    
    if nome_coordenacao:
        trocar_coordenacao(nav, nome_coordenacao)
     
def trocar_coordenacao(nav: webdriver.Firefox, nome_coordenacao:str) -> None:
    """
    Troca a coordenação no SEI-RJ.
    
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        nome_coordenacao (str): Nome da coordenação a ser trocada.
    """
    coordenacao =     WebDriverWait(nav,10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[@id = 'lnkInfraUnidade']")))[1]
    if coordenacao.get_attribute("innerHTML") != nome_coordenacao:
        coordenacao.click()
        WebDriverWait(nav,5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Trocar Unidade')]")))
        nav.find_element(By.XPATH, "//td[text() = '"+nome_coordenacao+"' ]").click() 
        
def criar_processo(processo: WebElement) -> Processo:
    """
    Cria um objeto do tipo Processo ao receber um elemento WebElement derivado do seguinte XPath "//tbody//tr[@id='trPos0']".
    \nJanela: BLOCO
    Args:
        processo (WebElement): Elemento do processo.
    Returns:
        processo (Processo): Objeto do tipo Processo, contendo o número, o texto, o elemento e o link do processo.
    """
    link = processo.find_element(By.XPATH, ".//td[3]//a")
    texto = processo.text
    numero = link.text
    return Processo(numero,processo,texto,link)

def abrir_pastas(nav: webdriver.Firefox) -> None:
    """
    Abre todas as pastas de documentos na árvore de documetos do processo SEI-RJ.
    Funciona apenas dentro de uma guia de processo.
    \nJanela: PROCESSO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
    """
    nav.switch_to.default_content()
    WebDriverWait(nav,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
    lista_docs = WebDriverWait(nav,5).until(EC.presence_of_element_located((By.ID, "divArvore")))
    pastas = lista_docs.find_elements(By.XPATH, '//a[contains(@id, "joinPASTA")]//img[contains(@title, "Abrir")]')
    
    for doc in pastas:
        doc.click() 
        WebDriverWait(nav,5).until(EC.presence_of_element_located((By.XPATH, "//*[text() = 'Aguarde...']")))
        WebDriverWait(nav,5).until(EC.invisibility_of_element((By.XPATH, "//*[text() = 'Aguarde...']")))
        
def pesquisar_processo(nav: webdriver.Firefox, processo_sei: str) -> None:
    """
    Pesquisa um processo na barra de pesquisa do SEI-RJ e abre.
    
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        processo_sei (str): Número do processo a ser pesquisado.
    """
    barra_pesquisa = nav.find_element(By.ID, "txtPesquisaRapida")
    barra_pesquisa.send_keys(processo_sei)
    barra_pesquisa.send_keys(Keys.ENTER)
    
    WebDriverWait(nav,10).until(EC.presence_of_element_located((By.ID, "ifrArvore")))    

def procurar_documentos(nav: webdriver.Firefox, lista_documentos : list[str] | str, coordenacao: str = "") -> list[WebElement]:
    """
    Procura na árvore de documentos do processo no SEI-RJ todos os documentos que contenham em seu nome uma das strings da lista e retorna.
    Caso coordenacao seja diferente de "", procura por documentos apenas gerados pela coordenação solicitada.
    \nJanela: PROCESSO

    Args:
        nav (webdriver.Firefox): Navegador aberto.
        lista_documentos (list[str] | str): Documento ou lista de documentos que deseja procurar.
        coordenacao (str): Coordenação de onde vem os documentos.
    Returns:
        documentos (list[WebElement]): Uma lista de WebElements derivadas do XPATH "//div[@id = 'divArvore']//div//a[@class = 'infraArvoreNo']", que representam um documento na árvore do processo.
    """
    lista = []
    nav.switch_to.default_content()

    arvore = WebDriverWait(nav,10).until(EC.presence_of_element_located((By.ID, "ifrArvore")))    
    nav.switch_to.frame(arvore)
    abrir_pastas(nav)

    docs = nav.find_elements(By.XPATH, "//div[@id = 'divArvore']//div//a[@class = 'infraArvoreNo']")

    quant_docs = len(docs)
    
    if isinstance(lista_documentos,str):
        lista_documentos = [lista_documentos]
        
    for doc in (range(quant_docs)):
        doc_texto = docs[doc].text
        if any(arquivo.upper() in doc_texto.upper() for arquivo in lista_documentos):   
            
            id_doc = re.search(r"anchor(.*)", docs[doc].get_attribute('id')).group(1)
            coordenacao_doc = nav.find_element(By.XPATH,"//div[@id = 'divArvore']//div//a[@id = 'anchorUG"+ id_doc+"']")
            if coordenacao in coordenacao_doc.text:
                lista.append(docs[doc])
    
    nav.switch_to.default_content()
                
    return lista      
    
def baixar_documentos(nav: webdriver.Firefox, lista_arquivos: list[str] | str) -> None:
    """
    Procura na árvore de documentos do processo no SEI-RJ todos os documentos que contenham em seu nome uma das strings da lista e baixa eles.
    \nJanela: PROCESSO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        lista_documentos (list[str] | str): Documento ou lista de documentos que deseja baixar.
    """
    if isinstance(lista_arquivos,str):
        lista_arquivos = [lista_arquivos]
    
    alterar_config_pdf_firefox(nav,"Salvar Arquivo")
    
    nav.switch_to.default_content()
    
    arvore = WebDriverWait(nav,10).until(EC.presence_of_element_located((By.ID, "ifrArvore")))    
    nav.switch_to.frame(arvore)
    
    abrir_pastas(nav)

    lista_docs =  WebDriverWait(nav,10).until(EC.presence_of_element_located((By.ID, "divArvore")))  
    docs = lista_docs.find_elements(By.TAG_NAME, "a")
    
    for doc in docs:
        if any(arquivo.upper() in doc.text.upper() for arquivo in lista_arquivos):
            doc.click()
            
    alterar_config_pdf_firefox(nav,"Abrir no Firefox")
                
def acessar_bloco_interno(nav: webdriver.Firefox, bloco_solicitado : str) -> None:
    """
    Acessa um bloco interno no SEI-RJ.
    
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        bloco_solicitado (str): O bloco que deseja acessar.
    Raises:
        BlocoNaoEncontradoException: Quando o bloco não é encontrado.
    """
    nav.find_element(By.XPATH, "//span[text() = 'Blocos']").click()
    WebDriverWait(nav,10).until(EC.element_to_be_clickable((By.XPATH, "//span[text() = 'Internos']"))).click()
    blocos = nav.find_elements(By.XPATH, LINHA_SEI)[1:-1]

    for bloco in blocos:    
        numero_bloco = bloco.find_elements(By.XPATH,".//td")[1]
        if numero_bloco.text == bloco_solicitado:
            numero_bloco.find_element(By.XPATH, './/a').click()
            break     
    else:
        raise BlocoNaoEncontradoException("Bloco não encontrado")
        
def entrar_e_obter_processos_bloco(nav: webdriver.Firefox, bloco_solicitado: str) -> list[WebElement]:
    """
    Acessa um bloco interno no SEI-RJ e retorna os processos encontrados.
    
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        bloco_solicitado (str): O bloco que deseja acessar.
    Returns:
        processos (list[WebElement]): Lista de WebElements encontrados no bloco, derivados do XPATH "//tbody//tr[@id='trPos0']".
    Raises:
        BlocoNaoEncontradoException: Quando o bloco não é encontrado.
    """
    
    nav.find_element(By.XPATH, "//span[text() = 'Blocos']").click()
    WebDriverWait(nav,10).until(EC.element_to_be_clickable((By.XPATH, "//span[text() = 'Internos']"))).click()
    
    WebDriverWait(nav,8).until(EC.presence_of_element_located, (By.XPATH, "//div[text() = 'Blocos Internos']"))

    
    blocos = nav.find_elements(By.XPATH, LINHA_SEI)[1:-1]

    for bloco in blocos:    
        numero_bloco = bloco.find_elements(By.XPATH,".//td")[1]
        if numero_bloco.text == bloco_solicitado:
            numero_bloco.find_element(By.XPATH, './/a').click()
            break
    else:
        raise BlocoNaoEncontradoException("Bloco não encontrado")
  
    processos = nav.find_elements(By.XPATH, "//tbody//tr[@id='trPos0']")
    return processos

def obter_processos_bloco(nav: webdriver.Firefox) -> list[WebElement]:
    """
    Retorna os processos do bloco atual.
    \nJanela: BLOCO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
    Returns:
        processos (list[WebElement]): Lista de WebElements encontrados no bloco, derivados do XPATH "//tbody//tr[@id='trPos0']".
    """
    time.sleep(2)
    processos = nav.find_elements(By.XPATH, LINHA_SEI)
    return processos
  
def escrever_anotacao(nav: webdriver.Firefox,texto : str| list[str],numero_processo: str) -> None:
    """
    Escreve uma anotação no bloco interno, no processo desejado.
    \nJanela: BLOCO
    Args:
        nav (webdriver.Firefox): Navegador aberto
        texto (list[str] | str): Texto para ser escrito na anotação, se for lista, são separados por ENTER.
        numero_processo (str): Número do processo da anotação.
    """
    processos = nav.find_elements(By.XPATH, LINHA_SEI)
    for processo in processos:
        if numero_processo in processo.text:
            processo.find_element(By.XPATH,".//td//a//img[@title='Anotações']").click()
            break                       
    try:
        WebDriverWait(nav,5).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'iframe')))

        txtarea = WebDriverWait(nav,10).until(EC.element_to_be_clickable((By.XPATH, '//textarea[@id = "txtAnotacao"]')))

        txtarea.send_keys(Keys.PAGE_DOWN)
        txtarea.send_keys(Keys.END)
        if isinstance(texto,list):
            for paragrafo in texto:
                txtarea.send_keys(Keys.ENTER)
                txtarea.send_keys(paragrafo)
        if isinstance(texto,str):
            txtarea.send_keys(Keys.ENTER)
            txtarea.send_keys(texto)
        salvar = nav.find_element(By.XPATH, '//button[@value = "Salvar"]')
        salvar.click()
        
    except TimeoutException:
       traceback.print_exc()
       nav.find_element(By.XPATH, FECHAR_ABA_SEI).click()
    finally:
        nav.switch_to.default_content()
        WebDriverWait(nav,3).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class = 'sparkling-modal-overlay']")))

def buscar_informacao_em_documento(nav: webdriver.Firefox,documento: WebElement, regex: str, verificador:str = None,show:bool = False) -> Match[str] | None:
    """
    Busca no corpo de um documento no processo SEI, qualquer informação via regex.
    \nJanela: PROCESSO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        documento (WebElement): Elemento que representa um link pro documento na árvore, "//div[@id = 'divArvore']//div//a[@class = 'infraArvoreNo']".
        regex (str): Regex pra buscar as informações.
        verificador (str): String pra buscar no corpo do documento antes do regex, pra verificar se o documento foi aberto corretamente. Caso nulo, o sistema aguarda 1s.
        show (bool): Marcar como True caso deseje printar o corpo do documento.
    Returns:
        resultado (Match[str]): Um Match do regex. Para acessar o valor dele usar a função group.
    Raises:
        CondicaoNaoEncontradaException: Quando o verificador não é encontrado no corpo do documento.
    """
    
    nav.switch_to.default_content()
    WebDriverWait(nav,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
    
    documento.click()
    nav.switch_to.default_content()            
    WebDriverWait(nav,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
    WebDriverWait(nav,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvoreHtml")))


    if not verificador:
        time.sleep(1)  
    elif isinstance(verificador,str):
        condicao = "//*[contains(text(), '" + verificador + "')]"
    else:
        condicao = "//*["
        
        for item in verificador:
            condicao += "contains(text(), '" + item + "') or "
        
        condicao = condicao[:-4]
        condicao += "]"    
        
        try:
            WebDriverWait(nav,3).until(EC.presence_of_element_located((By.XPATH, condicao)))
        except TimeoutException:
            raise CondicaoNaoEncontradaException(condicao + "não encontrado no corpo")
    
    body = nav.find_element(By.XPATH, '//body').text    
    
    if show:
        print(body)
    
    if isinstance(regex,list):
        resultado = []
        for item in regex:
            resultado.append(re.search(item,body))
        if all(elem is None for elem in resultado):
            return None
    if isinstance(regex,str):
        resultado = re.search(regex,body)
    
    
    nav.switch_to.default_content()

    return resultado

def incluir_processo_bloco(nav: webdriver.Firefox,bloco : str) -> None:
    """
    Inclui um processo em um bloco interno.
    \nJanela: PROCESSO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        bloco(str): O bloco que o processo vai ser enviado.
    Raises:
        ProcessoJaIncluidoException: Quando o processo já existe no bloco interno selecionado.
    """
    nav.switch_to.default_content()
    WebDriverWait(nav,5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
    nav.switch_to.default_content()
    WebDriverWait(nav,5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
    WebDriverWait(nav,5).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Incluir em Bloco']"))).click()
    try:
        WebDriverWait(nav,2).until(EC.alert_is_present())
        nav.switch_to.alert.accept()
    except NoSuchElementException:
       pass

    nav.switch_to.default_content()
    WebDriverWait(nav,5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@name = 'modal-frame']")))
    WebDriverWait(nav,5).until(EC.element_to_be_clickable((By.XPATH, "//a[text() = '"+bloco+"']"))).send_keys(Keys.ENTER)
    nav.switch_to.default_content()  
    try:
        WebDriverWait(nav,2).until(EC.alert_is_present())
        time.sleep(4)
        nav.switch_to.alert.accept()
        raise ProcessoJaIncluidoException("Processo já incluso no bloco")
    except TimeoutException:
        print("Processo adicionado no bloco " + bloco)
           
def remover_processo_bloco(nav: webdriver.Firefox,numero_processo: str)-> None:
    """
    Remover processo de um bloco interno.
    \nJanela: BLOCO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        numero_processo (str): Numero do Processo pra ser removido.

    """
    processos = nav.find_elements(By.XPATH, LINHA_SEI)
    for processo in processos:
        if numero_processo in processo.text:
            processo.find_element(By.XPATH,".//td//a//img[@title='Retirar Processo/Documento do Bloco']").click()
            break 
        
    WebDriverWait(nav,5).until(EC.alert_is_present())
    nav.switch_to.alert.accept()
    nav.switch_to.default_content()
    print("Processo removido do bloco")

def gerar_despacho(nav: webdriver.Firefox,tipo_documento: str,texto_inicial: str| None = None,modelo:str | None = None,acesso: str = "Restrito", hipotese: str = "Controle Interno (Art. 26, § 3º, da Lei nº 10.180/2001)", nome: str = "") -> None:
    """
    Gera um novo despacho.
    Não preenche o modelo de despacho.
    \nJanela: PROCESSO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        tipo_documento(str): Qual o tipo de despacho, exemplos: Despacho de Autorização, Despacho de Encaminhamento...
        texto_inicial(str):  "Documento Padrão", "Texto Padrão" ou None. Define qual o texto inicial.
        modelo(str): Nome ou número do modelo do despacho.
        acesso(str): "Restrito", "Público" ou "Sigiloso". O nível de acesso do despacho.
        hipotese(str): Qual a hipótese legal para o acesso. Se o acesso for "Público" é desconsiderado.
        nome(str): Nome na árvore do despacho.
    Raises:
        CondicaoNaoEncontradaException: Quando o verificador não é encontrado no corpo do documento.
    """
    
    nav.switch_to.default_content()
    WebDriverWait(nav,5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
    WebDriverWait(nav,10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Incluir Documento']"))).click()
    WebDriverWait(nav,5).until(EC.presence_of_element_located((By.XPATH,"//label[text() = 'Escolha o Tipo do Documento: ']")))
    nav.find_element(By.XPATH,'//a[text() = "' + tipo_documento +'"]').click()
    
    inicial = {"Documento Modelo": "ProtocoloDocumentoTextoBase", "Texto Padrão": "TextoPadrao", "Nenhum" : None, None : None}
    texto_inicial = inicial.get(texto_inicial,texto_inicial)
    
    
    WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.ID, "divOptProtocoloDocumentoTextoBase")))

    nav.find_element(By.ID, "txtNomeArvore").send_keys(nome)


    
    if texto_inicial:
        nav.find_element(By.XPATH, "//label[@for = 'opt" + texto_inicial + "']").click()
        input_modelo = WebDriverWait(nav,5).until(EC.presence_of_element_located((By.XPATH,"//input[@id= 'txt" + texto_inicial + "']")))
        input_modelo.send_keys(modelo)
        time.sleep(1)
        input_modelo.send_keys(Keys.ENTER)
    
    
    controle_acesso = {"Sigiloso" : "optSigiloso", "Restrito" : "optRestrito", "Público": "optPublico"}
    
    acesso = controle_acesso.get(acesso,acesso)
    
    nav.find_element(By.XPATH,'//label[@for ="' + acesso + '"]').click()
    if acesso != "optPublico":
        hipoteses = Select(nav.find_element(By.ID, 'selHipoteseLegal'))
        opcoes = hipoteses.options
        for opcao in opcoes:
            if hipotese in opcao:
                hipoteses.select_by_visible_text(opcao)
    
    
    nav.find_element(By.XPATH, "//button[@name = 'btnSalvar']").click()
       
def inserir_hyperlink_sei(nav:  webdriver.Firefox,numero_documento: str) -> None:
    """
    Insere um hyperlink SEI na janela de modificação de despacho.
    \nJanela: EDITOR DE DESPACHO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        numero_documento (str): Numero do documento na árvore do processo.
    """

    nav.switch_to.default_content()
    WebDriverWait(nav,5).until(EC.element_to_be_clickable((By.XPATH, "//a[@id = 'cke_178']"))).click()
    nav.find_element(By.XPATH, "//input[@class = 'cke_dialog_ui_input_text']").send_keys(numero_documento)
    nav.find_element(By.XPATH, "//a[@class = 'cke_dialog_ui_button cke_dialog_ui_button_ok']").click()
    #FAZER TRATAMENTO DE ERROS
    
def limpar_anotacao(nav:  webdriver.Firefox,numero_processo: str) -> None:
    """
    Limpa todo o texto de uma anotação de um processo em um bloco interno.
    \nJanela: BLOCO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        numero_processo(str): Numero do processo para ter as anotações apagadas.
    """
    
    processos = nav.find_elements(By.XPATH, LINHA_SEI)
    for processo in processos:
        if numero_processo in processo.text:
            processo.find_element(By.XPATH,".//td//a//img[@title='Anotações']").click()
            break                       
    try:
        WebDriverWait(nav,5).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'iframe')))

        txtarea = nav.find_element(By.XPATH, '//textarea[@id = "txtAnotacao"]')
        txtarea.send_keys(Keys.CONTROL + "a")
        txtarea.send_keys(Keys.BACKSPACE)

        salvar = nav.find_element(By.XPATH, '//button[@value = "Salvar"]')
        salvar.click()
        
    except ElementNotInteractableException:
       traceback.print_exc()
       nav.find_element(By.XPATH, FECHAR_ABA_SEI).click()
    finally:
        nav.switch_to.default_content()
        WebDriverWait(nav,3).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class = 'sparkling-modal-overlay']")))
        
def escrever_acompanhamento_especial(nav: webdriver.Firefox, texto:list[str],grupo_acompanhamento:str) -> None:
    """
    Escreve no acompanhamento especial do processo.
    \nJanela: PROCESSO
    
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        texto (list[str]): Texto com as informções para adicionar no acompanhamento especial, cada item na lista é separado com um ENTER e /.
        grupo_acompanhamento (str): O grupo de acompanhamento especial dessas informações.
        
    Raises:
        ElementoNaoEncontradoException: Quando o grupo do acompanhamento especial não é encontrado.
        CaixaDeTextoCheiaException: Quando a caixa de texto do acompanhamento especial está cheia.
    """

    nav.switch_to.default_content()
    WebDriverWait(nav,5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
    nav.switch_to.default_content()
    WebDriverWait(nav,5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
    
    WebDriverWait(nav,5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Processo aberto')]")))
    nav.find_element(By.XPATH, "//img[@title = 'Acompanhamento Especial']").click()

    try:
        WebDriverWait(nav,2).until(EC.presence_of_element_located((By.XPATH, '//img[@alt ="Alterar Acompanhamento"]'))).click()
    except TimeoutException:
        try:
            WebDriverWait(nav,2).until(EC.presence_of_element_located((By.XPATH, '//img[@alt ="Novo Grupo de Acompanhamento"]')))
        except TimeoutException:
            raise ElementoNaoEncontradoException ("Acompanhamento não encontrado")             
    
    WebDriverWait(nav,10).until(EC.presence_of_element_located((By.ID, "selGrupoAcompanhamento")))
    sel_grupo_acompanhamento = Select(nav.find_element(By.ID, "selGrupoAcompanhamento"))
    sel_grupo_acompanhamento.select_by_visible_text(grupo_acompanhamento)
    
    caixa_texto = nav.find_element(By.ID, "txaObservacao")
    caixa_texto.send_keys(Keys.PAGE_DOWN)
    caixa_texto.send_keys(Keys.END)

    texto_original = nav.find_element(By.XPATH, "//textarea").text

    for info in texto:
        if info.upper() not in texto_original.upper():  
            info = "\n" + info + " /"    
            if len(texto_original) + len(info) > 500:
                raise CaixaDeTextoCheiaException("Texto cheio!")
            
            caixa_texto.send_keys(info)
            print('"'+info + '" adicionada!')
            texto_original += info
    nav.find_element(By.XPATH, "//button[@value = 'Salvar']").click()
    nav.switch_to.default_content()

def buscar_numero_documento(nav: webdriver.Firefox,documento: str,lista: bool=False)  -> str | list[str]:
    """
    Busca o número dos documentos no SEI.
    \nJanela: PROCESSO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        documento (str): O nome do documento pra encontrar o número.
        lista(boolean): Se True, retorna a lista dos documentos. Se False retorna o último da árvore.
    Returns:
        numero_documento(str | list[str]): Retorna o número do documento ou a lista de números.

    """
    
    nav.switch_to.default_content()

    WebDriverWait(nav,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
    abrir_pastas(nav)

    docs = nav.find_elements(By.XPATH, "//div[@id = 'divArvore']//div//a[@class = 'infraArvoreNo']")
    
    
    if lista:
        lista = []
        for doc in reversed(docs):
            texto = doc.text
            if re.search(documento,texto):
                lista.append(re.search(r"(\d+)\)?$", texto).group(1)  )  
        
        nav.switch_to.default_content()
        return lista
      
    for doc in reversed(docs):
        texto = doc.text
        if re.search(documento,texto):
            nav.switch_to.default_content()
            return  re.search(r"(\d+)\)?$", texto).group(1)

def incluir_bloco_assinatura(nav:webdriver.Firefox,bloco_assinatura:str) -> None:
    """
    Inclui um processo no bloco de assinatura desejado.
    \nJanela: PROCESSO
    
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        bloco_assinatura (str): Número ou nome completo do bloco de assinatura.
    """
    
    print("Incluindo no novo bloco de assinatura...")
    nav.switch_to.default_content()

    iframe_botoes = nav.find_element(By.ID, "ifrVisualizacao")
    nav.switch_to.frame(iframe_botoes)


    arvore_botoes =  WebDriverWait(nav,5).until(EC.element_to_be_clickable((By.ID, "divInfraAreaTela")))
    botoes_sei = arvore_botoes.find_element(By.CLASS_NAME, "barraBotoesSEI")
    opcoes_botoes_sei = botoes_sei.find_elements(By.TAG_NAME, "a")
    for opcao_botao_sei in opcoes_botoes_sei:
        info_botao = opcao_botao_sei.find_element(By.TAG_NAME, "img")
        attr_title = info_botao.get_attribute("title")
        if attr_title == "Incluir em Bloco de Assinatura":
            opcao_botao_sei.click()
            break

    WebDriverWait(nav, 20).until(EC.element_to_be_clickable((By.ID, "selBloco")))
    # Clicar para abrir a aba de blocos
    nav.find_element(By.ID, "selBloco").click()
    selecao_bloco = nav.find_element(By.ID, "selBloco")
    options_bloco = selecao_bloco.find_elements(By.TAG_NAME, "option")
   

    for option_bloco in options_bloco:
        if  bloco_assinatura in option_bloco.text:
            option_bloco.click()
            break
            
    
    # Incluir no bloco de assinatura
    nav.find_element(By.ID, "sbmIncluir").click()

    nav.switch_to.default_content()

    print("Incluido com sucesso.")

def gerar_documento_externo(nav: webdriver.Firefox,tipo_documento: str,arquivo: str,nome:str = "",formato:str = "Nato-digital",acesso:str ="Restrito",hipotese:str ='Controle Interno (Art. 26, § 3º, da Lei nº 10.180/2001)'):
    """
    Busca no corpo de um documento no processo SEI qualquer informação via regex.
    \nJanela: PROCESSO
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        tipo_documento (str): Tipo do Documento, exemplos: Comprovante, Alvará.
        arquivo (str): Caminho do Arquivo no computador.
        nome (str): Nome na árvore. 
        formato(str): "Nato-digital" ou "Digitalizado nessa unidade". Formato do documento.
        acesso(str): "Restrito", "Público" ou "Sigiloso". O nível de acesso do despacho.
        hipotese(str): Qual a hipótese legal para o acesso. Se o acesso for "Público" é desconsiderado. (default = "Controle Interno").
    """
    
    data_hoje = date.today()
    data_formatada = "{:02d}/{:02d}/{:04d}".format(data_hoje.day, data_hoje.month, data_hoje.year)
    
    
    nav.switch_to.default_content()
    WebDriverWait(nav,5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
    WebDriverWait(nav,5).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt = 'Incluir Documento']"))).click()
    WebDriverWait(nav,5).until(EC.presence_of_element_located((By.XPATH,"//label[text() = 'Escolha o Tipo do Documento: ']")))
    WebDriverWait(nav,5).until(EC.presence_of_element_located((By.XPATH,'//a[text() = " Externo"]'))).click()

       
    WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.ID, "divSerieDataElaboracao")))

   
    nav.find_element(By.ID, "txtDataElaboracao").send_keys(data_formatada)

    nav.find_element(By.ID, "txtNomeArvore").send_keys(nome)
    
    select = Select(nav.find_element(By.XPATH, "//select[@id = 'selSerie']"))
    select.select_by_visible_text(tipo_documento)
    
    nav.find_element(By.XPATH, "//label[text() = '"+formato+"']").click()
    nav.find_element(By.XPATH, "//label[text() = '"+acesso+"']").click()

    if acesso != "Público":
        hipoteses = Select(nav.find_element(By.ID, 'selHipoteseLegal'))
        opcoes = hipoteses.options
        for opcao in opcoes:
            if hipotese in opcao:
                hipoteses.select_by_visible_text(opcao)
    
    nav.find_element(By.XPATH, "//input[@id = 'filArquivo']").send_keys(arquivo)
    time.sleep(1)
    
    nav.find_element(By.XPATH, "//button[@name = 'btnSalvar']").click()
    nav.switch_to.default_content()
    
def alterar_config_pdf_firefox(nav:webdriver.Firefox,config:str) -> None:
    """
    Altera as configurações do Firefox para baixar automaticamente um PDF ao clicar nele ou salvar no Firefox.
    
    Args:
        nav (webdriver.Firefox): Navegador aberto.
        config (str): "Salvar arquivo" ou "Abrir no Firefox", para decidir a configuração.
    
    """
    
    if config == "Salvar arquivo":
        config2 = "Save File"
    if config == "Abrir no Firefox":
        config2 = "Open in Firefox"
    nav.switch_to.new_window("tab")
    nav.get("about:preferences#general")

    pdf = WebDriverWait(nav,5).until(EC.presence_of_element_located((By.XPATH,"//*[@type = 'application/pdf']" )))
    pdf.find_element(By.XPATH, ".//*[@class = 'actionsMenu']").click()
    try:
        pdf.find_element(By.XPATH,".//*[@label = '"+ config +"']").click()
    except NoSuchElementException:
        pdf.find_element(By.XPATH,".//*[@label = '"+ config2 +"']").click()

    nav.close()
    nav.switch_to.window(nav.window_handles[1])