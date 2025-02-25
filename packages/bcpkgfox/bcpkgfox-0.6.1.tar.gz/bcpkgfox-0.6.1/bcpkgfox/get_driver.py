RESET, GR, ORANGE, DK_ORANGE, RD = "\033[0m", "\033[38;5;34m", "\033[38;5;214m", "\033[38;5;130m", "\033[38;5;196m"
from .find_elements import Elements, backcode__dont_use__find_element_with_wait_backcode, By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium_stealth import stealth
from selenium import webdriver
from typing import Optional

from .find_elements import Elements

import undetected_chromedriver as uc
import subprocess
import requests
import logging
import random
import time
import sys
import os
class Instancedriver:
    def __init__(self,
        Version: Optional[str | int] = "latest",
        Subprocess: Optional[bool] = False,
        Selenoid: Optional[str] = None,
        Navegador: Optional[str] = "chrome",
        Driver_path: Optional[str] = None
        ):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(), logging.FileHandler(f'{self.__class__.__name__}.log')]
        )
        self.version_main = None
        self.options = None
        self.version = Version
        self.subprocess = Subprocess
        self.selenoid = Selenoid
        self.nav = Navegador
        self.driver_path = Driver_path

        self.captcha_api_key = None
        self.extension_path = None
        self.captcha_name = None
        self.driver = None

        self.arguments = self.Arguments(self)
        self.elements = None #FIX: Instance of .get_driver

    def initialize_driver(self,
        maximize: Optional[bool] = True,
        Active_logs: Optional[bool] = True
        ):
        self.version_main = self._get_chrome_version() if self.version == "latest" else self.version

        if self.selenoid:
            if self.nav.lower() == "firefox":
                self.options = webdriver.FirefoxOptions()
            elif self.nav.lower() == "opera":
                self.options = webdriver.OperaOptions()
            else:
                self.options = webdriver.ChromeOptions()

            self.options.set_capability("browserVersion", "128.0")
            self.options.set_capability("selenoid:options", {"enableVNC": True})

            self.driver = webdriver.Remote(
                command_executor='http://host.docker.internal:4444/wd/hub',
                options=self.options,
            )

        else:

            # Internet explorer
            if self.nav.lower() in ["ie", "internet_explorer", "internet explorer", "explorer"]:
                self.nav = "Internet explorer"
                self.iniciate_internet_explorer(Active_logs)

            # Edge
            elif self.nav.lower() == "edge":
                self.driver = webdriver.Edge()

            # Firefox
            elif self.nav.lower() in ["firefox", "fox", "fire", "mozila", "mozila firefox"]:
                self.options = webdriver.FirefoxOptions()
                self.driver = webdriver.Firefox(options=self.options)

            # Opera
            elif self.nav.lower() == "opera":
                self.options = webdriver.OperaOptions()

            # Chrome
            else:
                self.options = webdriver.ChromeOptions()
                chrome_options = self.options
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")

                # Automatically download and use the correct ChromeDriver
                service = Service(ChromeDriverManager().install())

                # Initialize Chrome
                self.driver = Chrome(service=service, options=chrome_options)

                # Apply stealth (optional)
                # stealth(
                #     self.driver,
                #     languages=["en-US", "en"],
                #     vendor="Google Inc.",
                #     platform="Win32",
                #     webgl_vendor="Intel Inc.",
                #     renderer="Intel Iris OpenGL Engine",
                #     fix_hairline=True,
                # )
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print(f" {DK_ORANGE}> {ORANGE}{self.nav[0].upper()}{self.nav[1:].lower()}{RESET} instânciado com sucesso.") if Active_logs else None
        if maximize: self.driver.maximize_window()
        self.elements = Elements(self.driver)
        return self.driver

    def iniciate_internet_explorer(self, Active_logs):
        powershell_script = """
            $zones = @("1", "2", "3", "4")
            $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\"

            foreach ($zone in $zones) {
                Set-ItemProperty -Path ($path + $zone) -Name 2500 -Value 0 -Type DWord
            }

            Write-Output "Modo Protegido ativado para todas as zonas de segurança do Internet Explorer."
        """

        process = subprocess.run(
            ["powershell", "-Command", powershell_script],
            capture_output=True,
            text=True
        ) # ; print(process.stdout, process.stderr)
        print(f" {DK_ORANGE}>{RESET} Modo Protegido ativado para todas as zonas de segurança do Internet Explorer.") if Active_logs else None

        options = webdriver.IeOptions()
        options.ignore_protected_mode_settings = True
        options.require_window_focus = True
        service = IEService(executable_path=self.driver_path)
        self.driver = webdriver.Ie(service=service, options=options)

    def add_extension(self, extension_folder: str,
        config: Optional[bool] = False,
        key: Optional[str|int] = None
        ):
        """ Inicia o navegador com uma extensão, o 'config' ele identifica o nome da pasta e se for uma conhecida (capmonster, twocaptcha) configura automaticamente

        - OBS: Caso a extensão precise de alguma KEY, declare ela também na variavel "key"

        - Exemplo: add_extension("capmonster", config=True)"""
        try:
            extensao_caminho = self.__resource_path(extension_folder)
            if not os.path.exists(extensao_caminho): extensao_caminho = os.path.abspath(extension_folder)
            self.arguments.add_new_argument(f'--load-extension={extensao_caminho}')
        except Exception as e:
            logging.error("Erro ao verificar pasta da extensão", exc_info=True)
            raise SystemError("Verificar pasta da extensão") from e

        if key:
            key = str(key) ; cap_monster_names = ["capmonster", "captchamonster", "monster", "cap-monster", "captcha monster", "captcha-monster", "cmonster", "cap monster"]
            for name in cap_monster_names:
                if name in extension_folder.lower(): self._config_capmonster(key)

    def _get_chrome_version(self) -> int:
        """Get major Chrome version"""
        try:
            if os.name == 'nt':
                return self._get_windows_chrome_version()
            return self._get_linux_chrome_version()
        except Exception as e:
            logging.error("Chrome version detection failed", exc_info=True)
            raise SystemError("Chrome version detection failed") from e

    @staticmethod
    def _get_windows_chrome_version() -> int:
        registry_paths = [
            r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome',
            r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome'
        ]
        for path in registry_paths:
            try:
                result = subprocess.check_output(
                    ['reg', 'query', path, '/v', 'DisplayVersion'],
                    stderr=subprocess.DEVNULL,
                    universal_newlines=True
                )
                version = result.split()[-1].split('.')[0]
                return int(version)
            except subprocess.CalledProcessError:
                continue
        raise SystemError("Chrome registry entry not found")

    @staticmethod
    def _get_linux_chrome_version() -> int:
        try:
            output = subprocess.check_output(
                ['google-chrome', '--version'],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            return int(output.strip().split()[-1].split('.')[0])
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise SystemError("Chrome not found in PATH")

    def _config_capmonster(self, api_key: str) -> None:
        self.driver.get("chrome://extensions/") ; time.sleep(5)

        # Shadow-doom
        id_extension = self.driver.execute_script("""
            return document.querySelector('extensions-manager')
            .shadowRoot.querySelector('extensions-item-list')
            .shadowRoot.querySelector('extensions-item').id;
        """) ; print(f" {DK_ORANGE}>{RESET} ID extensão extraido: ", id_extension)

        self.driver.get(f"chrome-extension://{id_extension.lower()}/popup.html")

        backcode__dont_use__find_element_with_wait_backcode(self.driver, By.ID, "client-key-input").send_keys(api_key) ; time.sleep(2.5)
        backcode__dont_use__find_element_with_wait_backcode(self.driver, By.XPATH, '//label[span[input[@id="captcha-radio-token-ReCaptcha2"]]]').click()
        backcode__dont_use__find_element_with_wait_backcode(self.driver, By.ID, "client-key-save-btn").click()
        print(" {DK_ORANGE}>{RESET} Capmonter configurado.")

    @staticmethod
    def __resource_path(relative_path):
        """Get the absolute path to a resource, works for dev and for PyInstaller."""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    @staticmethod
    def __check_selenoid_connection(selenoid_url: str):
        try:
            response = requests.get(selenoid_url)
            if response.status_code != 200:
                raise ConnectionError(f"Falha na conexão com o Selenoid. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise SystemError(f"Erro ao conectar ao servidor do Selenoid: {e}")

    @staticmethod
    def create_temp(folder_dir, txt_file: Optional[str] = None):
        """ folder_dir: coloque a pasta e subpastas que você quer criar.
            text_file: Coloque o que você quer que esteja escrito se tiver um .txt dentro (opcional).
        """
        import tempfile

        # Define a persistent temporary folder in the system temp directory.
        persistent_temp_folder = os.path.join(tempfile.gettempdir(), folder_dir)
        if not os.path.exists(persistent_temp_folder):
            os.makedirs(persistent_temp_folder)
            print(f" {ORANGE}>{RESET} Diretório temp criado:", file_path)
        else:
            print(f" {ORANGE}>{RESET} Diretório temp identificado:", file_path)

        # Define the path for the text file.
        file_path = os.path.join(persistent_temp_folder, folder_dir)

        # Write some content to the text file.
        with open(file_path, "w") as file:
            file.write(txt_file)

    @staticmethod
    def read_temp_file(temp_path, file_path):
        # Define the persistent temporary folder and file path (same as in Script 1).
        persistent_temp_folder = os.path.join(tempfile.gettempdir(), temp_path)
        file_path = os.path.join(persistent_temp_folder, file_path)

        # Read the content from the file.
        with open(file_path, "r") as file:
            content = file.read()

        return content

    class Arguments:
        def __init__(self, self_bot):
            self.web = self_bot
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler(), logging.FileHandler(f'{self.__class__.__name__}.log')]
            )

        def add_new_argument(self, Args: str | list):
            """ Coloque apenas o argumento que você quer adicionar a inicialização do driver.

            - Exemplo único: add_new_argument("--headless")

            - Exemplo composto: add_new_argument(["--headless", "--disable-gpu", ... ])"""

            if isinstance(Args,list) == True:
                for arg in Args: self.web.options.add_argument(arg)
            else: self.web.options.add_argument(Args)

        def add_experimental_new_option(self, Args: str | list):
            """ Coloque apenas o argumento que você quer adicionar a inicialização do driver.

            - Exemplo: add_experimental_new_option("prefs", profile)"""

            if isinstance(Args, list) == True:
                for arg in Args: self.web.options.add_experimental_option [arg]
            else: self.web.options.add_experimental_option[Args]

    class Selenoid:
        def __init__(self, self_bot):
            self.web = self_bot
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler(), logging.FileHandler(f'{self.__class__.__name__}.log')]
            )
            self.capabilities = DesiredCapabilities.CHROME.copy()

        def add_capabilities(self, capabilities: str | list):

            if isinstance(capabilities, list) == True:
                for cap in capabilities: self.web.options.add_experimental_option [arg]
            else: self.web.options.add_experimental_option[Args]

            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities["browserName"] = "chrome"
            capabilities["version"] = "122.0"
            capabilities["enableVNC"] = True

            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                desired_capabilities=capabilities
            )

            driver.get("https://www.google.com")

            import time
            time.sleep(10)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def backcode__dont_use__set_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    ]
    return random.choice(user_agents)

def backcode__dont_use__launch_browser(download_dir: str, extension_path, captcha_name, captcha_api_key) -> WebElement:
    global driver

    # Configurações para o Chrome
    options = uc.ChromeOptions()

    # Alterar o User-Agent
    options.add_argument(f"user-agent={backcode__dont_use__set_user_agent()}")

    # Default's
    profile = {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'download.default_directory': download_dir,
    }
    options.add_experimental_option('prefs', profile)

    # Configurações para reduzir detecção
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')

    if extension_path:
        extensao_caminho = resource_path(extension_path)
        if not os.path.exists(extensao_caminho):
            extensao_caminho = os.path.abspath(extension_path)

        options.add_argument(f'--load-extension={extensao_caminho}')

    # options.add_argument('--disable-extensions') # Fix: Possibilita ter extensões ou não, nunca influenciou na detecção

    # Inicializar o navegador com undetected_chromedriver
    driver = uc.Chrome(options=options, use_subprocess=True)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    if captcha_name:
        cap_monster_names = ["capmonster", "captchamonster", "monster", "cap-monster", "captcha monster", "captcha-monster", "cmonster", "cap monster"]

        for name in cap_monster_names:
            if captcha_name.lower() == name:
                backcode__dont_use__capmonster(captcha_api_key)

    driver.maximize_window()
    return driver

def backcode__dont_use__get(driver, link) -> WebElement:
    driver.get(link)

def backcode__dont_use__capmonster(api_key) -> None:
    global driver

    driver.get("chrome://extensions/")
    time.sleep(5)

    # Pega por JS pois está dentro da shadow
    id_extension = driver.execute_script("""
        return document.querySelector('extensions-manager')
        .shadowRoot.querySelector('extensions-item-list')
        .shadowRoot.querySelector('extensions-item').id;
    """)

    print("ID extensão extraido:", id_extension)
    driver.get(f"chrome-extension://{id_extension.lower()}/popup.html")

    backcode__dont_use__find_element_with_wait_backcode(driver, By.ID, "client-key-input").send_keys(api_key)
    time.sleep(2.5)
    backcode__dont_use__find_element_with_wait_backcode(driver, By.XPATH, '//label[span[input[@id="captcha-radio-token-ReCaptcha2"]]]').click() # icone salvar
    backcode__dont_use__find_element_with_wait_backcode(driver, By.ID, "client-key-save-btn").click() # icone salvar
    print(" - Capmonter configurado.")