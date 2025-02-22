from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

from typing import Optional

import pyautogui
import time

class Elements:
    def __init__(self, driver):
        self.driver = driver

    def find_element_with_wait(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = 10,
        parent: Optional[WebElement] = None
    ) -> WebElement:

        if "css" in by:
            by = By.CSS_SELECTOR

        if parent is None: parent = self.driver
        return WebDriverWait(parent, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def find_elements_with_wait(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = 10,
        parent: Optional[WebElement] = None
    ) -> WebElement:

        if "css" in by:
            by = By.CSS_SELECTOR

        if parent is None: parent = self.driver
        return WebDriverWait(parent, timeout).until(
            EC.presence_of_all_elements_located((by, value))
        )

    def wait_for_element_be_clickable(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = 10,
        parent: Optional[WebElement] = None
    ) -> WebElement:

        if "css" in by:
            by = By.CSS_SELECTOR

        if parent is None: parent = self.driver
        return WebDriverWait(parent, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def move_to_image(
        self,
        imagens: [str | list],
        click_on_final: Optional[bool] = False,
        tolerancia: Optional[float] = 0.8,
        timeout: Optional[int] = 10,
        repeat: Optional[bool] = False
    ) -> str:
        """
        Move o mouse até o centro de uma imagem na tela e clica, se necessário.

        Args:
            imagens (list) : Caminho da imagem a ser localizada.
            click_on_final (bool): Se True, realiza um clique ao final.
            tolerancia (float): Tolerância para a comparação da imagem (opcional, valor padrão: 1).
            timeout (int): Tempo máximo (em segundos) para procurar a imagem antes de desistir (opcional, valor padrão: 10).
            repeat (bool): Se for True ele ignora o timeout, e fica tentando encontrar a imagem até conseguir, sem gerar erro

        Exemplo:
            caminho_imagem = 'C:\\User\\Caminho\\exemplo.png'
            move_to_image(caminho_imagem, click_on_final=True, tolerancia=0.9, timeout=30)

        Nota:
            Recomenda-se colocar a imagem na mesma pasta do arquivo MAIN para evitar problemas ao gerar o executável com pyinstaller e rodar em outras máquinas.
        """

        if isinstance(imagens, str):
            imagens = [imagens]

        attempts = 0
        ultima_excecao = None

        def funcao():
            nonlocal attempts, ultima_excecao
            try:
                # Os for's abaixo servem para caso seja mais de uma imagem
                for imagem in imagens:
                    try:
                        localizacao = pyautogui.locateOnScreen(imagem, confidence=tolerancia)
                        break
                    except:
                        localizacao = None
                        continue

                if localizacao is not None:
                    x = localizacao.left + round(localizacao.width / 2)
                    y = localizacao.top + round(localizacao.height / 2)
                    pyautogui.moveTo(x, y)

                    if click_on_final:
                        pyautogui.click()
                    return localizacao

                else: raise FileNotFoundError()

            except Exception as e:
                attempts += 1
                ultima_excecao = e
                time.sleep(1)

        if repeat == True:
            while True:
                result = funcao()
                if result is not None:
                    return result
        else:
            while attempts < timeout:
                result = funcao()
                if result is not None:
                    return result

        # Se todas as tentativas falharem, levanta erro
        raise ValueError(f"Erro ao procurar a imagem '{imagens}' após 10 tentativas.") from ultima_excecao

    def wait_for_appear(
        self,
        object: [str|list],
        type: str,
        timeout: Optional[int] = 10
    ) -> str | WebElement:
        """
        Aguarda até que um objeto (texto, elemento, imagem ou janela) seja encontrado na tela.

        Args:
            object (str|list): O objeto a ser procurado. Pode ser um caminho de imagem, texto, elemento XPATH ou janela.
            type (str): O tipo de objeto a ser procurado. Pode ser 'imagem', 'texto', 'elemento' ou 'janela'.
            timeout (int): limite de tempo que vai procurar o objeto, coloque 0 para não ter limite

        Exemplo:
            wait_for('C:\\Caminho\\da\\imagem.png', 'imagem')
            wait_for('Texto a ser encontrado', 'texto')
            wait_for('XPATH_AQUI', 'elemento')
            wait_for('titulo_janela', 'janela')
        """
        text_type = ['text', 'texto', 'string', 'palavra', 'mensagem', 'frase', 'conteúdo', 'texto_visível', 'texto_encontrado', 'texto_display', 'label']
        element_type = ["elemento", "botao", 'element', 'web_element', 'html_element', 'ui_element', 'interface_element', 'objeto', 'widget', 'campo', 'componente']
        imagem_type = [ 'imagem', 'img', 'imagem_png', 'imagem_jpeg', 'image', 'imagem_exata', 'padrão_imagem', 'foto', 'captura_tela', 'screenshot', 'imagem_visual']
        window_type = ["window", "windows", "wd", "jn", "janela", "janelas", "janel", "windosw", "ui", "interface", "interface", "graphic", "display", "salvar como"]

        for escrita in text_type:
            if escrita in type.lower():
                type = "text"
                break

        for escrita in element_type:
            if escrita in type.lower():
                type = "element"
                break

        for escrita in imagem_type:
            if escrita in type.lower():
                type = "image"
                break

        for escrita in window_type:
            if escrita in type.lower():
                type = "window"
                break

        attempt = 0
        timeout = float(inf) if timeout == 0 else timeout

        if type == "text":
            while attempt < timeout:
                if object in self.driver.page_source:
                    return f"{object} encontrado"
                else:
                    attempt += 1

        if type == "element":
            while attempt < timeout:
                try:
                    element = WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.XPATH, object)))
                    if element:
                        return element
                except:
                    attempt += 1

        if type == "image":
            while attempt < timeout:
                try:
                    num_tolerancia = 1
                    for _ in range(3):
                        try:
                            self.move_to_image(object, tolerancia=num_tolerancia, timeout=1)
                            return f"{object} encontrado"
                        except:
                            num_tolerancia -= 0.1
                except:
                    attempt += 1

        if type == "window":
            from .get_driver import RD, RESET
            import pygetwindow as gw

            if isinstance(object, str) == True: object = [object]
            while attempt < timeout:
                for title_ in object: window_to_search = gw.getWindowsWithTitle(str(title_))
                if len(window_to_search) >= 1: return window_to_search
                else:
                    time.sleep(1)
                    attempt += 1

        raise ValueError(f" {RD}>>> {object} não encontrado {RESET}")

    def wait_for_disappear(
        self,
        object: [str | list],
        type: str,
        timeout: str,
    ) -> str | WebElement:

        """
        Aguarda até que um objeto desapareça.(texto, elemento ou imagem)

        Args:
            object (str|list): O objeto a ser procurado. Pode ser um caminho de imagem, texto ou elemento XPATH.
            type (str): O tipo de objeto a ser procurado. Pode ser 'imagem', 'texto' ou 'elemento'.
            timeout (int): limite de tempo que vai procurar o objeto, coloque 0 para não ter limite

        Exemplo:
            wait_for('C:\\Caminho\\da\\imagem.png', 'imagem')
            wait_for('Texto a ser encontrado', 'texto')
            wait_for( XPATH_AQUI, 'elemento')
        """
        global driver
        tempo = timeout

        text_type = ['texto', 'string', 'palavra', 'mensagem', 'frase', 'conteúdo', 'texto_visível', 'texto_encontrado', 'texto_display', 'label']
        element_type = [ "element", "elemento", "botao", 'element', 'web_element', 'html_element', 'ui_element', 'interface_element', 'objeto', 'widget', 'campo', 'componente']
        imagem_type = [ 'imagem', 'img', 'imagem_png', 'imagem_jpeg', 'image', 'imagem_exata', 'padrão_imagem', 'foto', 'captura_tela', 'screenshot', 'imagem_visual']

        for escrita in text_type:
            if escrita in type.lower():
                type = "text"

        for escrita in element_type:
            if escrita in type.lower():
                type = "element"

        for escrita in imagem_type:
            if escrita in type.lower():
                type = "image"

        # Encontra o objeto
        attempt = 0
        if timeout == 0:
            attempt = float('inf')

        if type == "text":
            while attempt != timeout:
                if object in driver.page_source:

                    # Depois de encontrar o elemento pela primeira vez espera ele sumir
                    while object in driver.page_source \
                        and attempt != timeout:
                        time.sleep(1)
                        attempt += 1

                    return f"{object} desapareceu"
                else:
                    time.sleep(1)
                    attempt += 1

        if type == "element":
            while attempt != timeout:
                try:
                    element = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, object)))

                    # Após encontrar umas primeira vez espera ele sumir
                    WebDriverWait(driver, abs(timeout-attempt)).until(EC.invisibility_of_element_located((By.XPATH, object)))
                    return f"{object} desapareceu"
                except:
                    attempt += 1

        if type == "image":
            while attempt != timeout:
                try:

                    # Vai abaixando a tolerancia até 0.8 para ver se encontra
                    num_tolerancia = 1
                    for _ in range(3):
                        try:
                            move_to_image(object, tolerancia=num_tolerancia, timeout=1)

                            # Após encontrar umas primeira vez espera ele sumir
                            while attempt != timeout:
                                try:
                                    move_to_image(object, tolerancia=num_tolerancia, timeout=1)
                                    time.sleep(0.9)
                                except:
                                    return f"{object} desapareceu"

                        except:
                            num_tolerancia -= 0.1
                except:
                    attempt += 1

        raise ValueError(f"{object} desapareceu")

def backcode__dont_use__wait_for_element_be_clickable(driver, by, value, timeout: Optional[int] = 10, parent: Optional[WebElement] = None) -> WebElement:
    if "css" in by:
        by = By.CSS_SELECTOR

    if parent is None:
        parent = driver  # Usa o driver principal se nenhum elemento pai for passado
    return WebDriverWait(parent, timeout).until(
        EC.element_to_be_clickable((by, value))
    )

def backcode__dont_use__find_element_with_wait_backcode(driver, by, value, timeout: Optional[int] = 10, parent: Optional[WebElement] = None) -> WebElement:
    if "css" in by:
        by = By.CSS_SELECTOR

    if parent is None:
        parent = driver  # Usa o driver principal se nenhum elemento pai for passado
    return WebDriverWait(parent, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def backcode__dont_use__find_elements_with_wait_backcode(driver, by, value, timeout, parent):
    if "css" in by:
        by = By.CSS_SELECTOR

    if parent is None:
        parent = driver  # Usa o driver principal se nenhum elemento pai for passado
    return WebDriverWait(parent, timeout).until(
        EC.presence_of_all_elements_located((by, value))
    )

def move_to_image(imagens, click_on_final=False, tolerancia=1, timeout=10, repeat=False):
    """
    Move o mouse até o centro de uma imagem na tela e clica, se necessário.

    Args:
        imagens (list) : Caminho da imagem a ser localizada.
        click_on_final (bool): Se True, realiza um clique ao final.
        tolerancia (float): Tolerância para a comparação da imagem (opcional, valor padrão: 1).
        timeout (int): Tempo máximo (em segundos) para procurar a imagem antes de desistir (opcional, valor padrão: 10).
        repeat (bool): Se for True ele ignora o timeout, e fica tentando encontrar a imagem até conseguir, sem gerar erro

    Exemplo:
        caminho_imagem = 'C:\\User\\Caminho\\exemplo.png'
        move_to_image(caminho_imagem, click_on_final=True, tolerancia=0.9, timeout=30)

    Nota:
        Recomenda-se colocar a imagem na mesma pasta do arquivo MAIN para evitar problemas ao gerar o executável com pyinstaller e rodar em outras máquinas.
    """

    if isinstance(imagens, str):
        imagens = [imagens]

    attempts = 0
    ultima_excecao = None

    def funcao():
        nonlocal attempts, ultima_excecao
        try:
            # Os for's abaixo servem para caso seja mais de uma imagem
            for imagem in imagens:
                try:
                    localizacao = pyautogui.locateOnScreen(imagem, confidence=tolerancia)
                    break
                except:
                    localizacao = None
                    continue

            if localizacao is not None:
                x = localizacao.left + round(localizacao.width / 2)
                y = localizacao.top + round(localizacao.height / 2)
                pyautogui.moveTo(x, y)

                if click_on_final:
                    pyautogui.click()
                return localizacao

            else: raise FileNotFoundError()

        except Exception as e:
            attempts += 1
            ultima_excecao = e
            time.sleep(1)

    if repeat == True:
        while True:
            result = funcao()
            if result is not None:
                return result
    else:
        while attempts < timeout:
            result = funcao()
            if result is not None:
                return result

    # Se todas as tentativas falharem, levanta erro
    raise ValueError(f"Erro ao procurar a imagem '{imagens}' após 10 tentativas.") from ultima_excecao

def backcode__dont_use__wait_for(driver, object, type, timeout):
    # Encontra o objeto
    attempt = 0
    if timeout == 0:
        attempt = 2

    if type == "text":
        while attempt != timeout:
            if object in driver.page_source:
                return f"{object} encontrado"
            else:
                attempt += 1

    if type == "element":
        while attempt != timeout:
            try:
                element = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, object)))
                if element:
                    return element
            except:
                attempt += 1

    if type == "image":
        while attempt != timeout:
            try:
                num_tolerancia = 1
                for _ in range(3):
                    try:
                        move_to_image(object, tolerancia=num_tolerancia, timeout=1)
                        return f"{object} encontrado"
                    except:
                        num_tolerancia -= 0.1
            except:
                attempt += 1

    raise ValueError(f"{object} não encontrado")

def backcode__dont_use__wait_for_d(driver, object, type, timeout):
    # Encontra o objeto
    attempt = 0
    if timeout == 0:
        attempt = float('inf')

    if type == "text":
        while attempt != timeout:
            if object in driver.page_source:

                # Depois de encontrar o elemento pela primeira vez espera ele sumir
                while object in driver.page_source \
                    and attempt != timeout:
                    time.sleep(1)
                    attempt += 1

                return f"{object} desapareceu"
            else:
                time.sleep(1)
                attempt += 1

    if type == "element":
        while attempt != timeout:
            try:
                element = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, object)))

                # Após encontrar umas primeira vez espera ele sumir
                WebDriverWait(driver, abs(timeout-attempt)).until(EC.invisibility_of_element_located((By.XPATH, object)))
                return f"{object} desapareceu"
            except:
                attempt += 1

    if type == "image":
        while attempt != timeout:
            try:

                # Vai abaixando a tolerancia até 0.8 para ver se encontra
                num_tolerancia = 1
                for _ in range(3):
                    try:
                        move_to_image(object, tolerancia=num_tolerancia, timeout=1)

                        # Após encontrar umas primeira vez espera ele sumir
                        while attempt != timeout:
                            try:
                                move_to_image(object, tolerancia=num_tolerancia, timeout=1)
                                time.sleep(0.9)
                            except:
                                return f"{object} desapareceu"

                    except:
                        num_tolerancia -= 0.1
            except:
                attempt += 1

    raise ValueError(f"{object} desapareceu")
