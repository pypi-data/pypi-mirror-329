from typing import Optional
import requests
import time

def invoke_api_list(link: str, token: str, method: Optional[str] = "GET", print_response: Optional[bool] = False) -> dict:
    """
    Exemplo de uso abaixo:

        import BCFOX as bc

        def invoke_api_list(self):
            link = 'https://linK_api.com.br/apis/{parametros}'
            token = 12345ABCDE12345ABCDE12345ABCDE12345ABCDE12345

            bc.invoke_api_list(link, token, print_response=True)

        OBS: o print_response vem por padrão desligado, caso você queira ativa o print da view coloque 'ON'

        """
    http_methods = {
        "POST": requests.post,
        "GET": requests.get,
        "PUT": requests.put,
        "DELETE": requests.delete,
        "PATCH": requests.patch
    }

    # Verifica se o método fornecido é válido
    method = method.upper()
    if method not in http_methods:
        raise ValueError(f"Método HTTP inválido. Use um dos seguintes: {', '.join(http_methods.keys())}.")

    payload = {}
    headers = {"x-access-token": token}

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        from .get_driver import RD, RESET
        try:

            # Realiza a requisição com o método correto
            if method == "GET" or method == "DELETE": response_insert = http_methods[method](link, params=payload, headers=headers)
            else: response_insert = http_methods[method](link, json=payload, headers=headers)
            if "Sequelize" in response_insert.json(): raise SystemError(f" {RD}>>> {response_insert.json()}{RESET}")

            if print_response == True:
                print(f"\n{response_insert.json()}")

            return response_insert.json()

        except Exception as e:
            print(f"Tentativa {attempt} falhou: {e}")

            if attempt < max_attempts:
                print("Tentando novamente em 5 segundos...")
                time.sleep(5)
                continue

            else: raise ValueError("Api list falhou")

    return response_api_list

def invoke_api_proc(link: str, payload_vars: dict, token: str, method: str, print_response: Optional[bool] = False) -> str:
    """
    Exemplo de uso abaixo:

    import BCFOX as bc

    def invoke_api_proc_final(self):
        link = https://linK_api.com.br/apis/{parametros}
        token = 12345ABCDE12345ABCDE12345ABCDE12345ABCDE12345

        payload = [
        {"ID":self.id},
        {"STATUS":self.status},
        {"PAGAMENTO":self.pagamento}
        ...
        ]

        bc.invoke_api_proc_final(link, payload, token, print_response=True)

    OBS: o print_response vem por padrão desligado, caso você queria ver o returno do response coloque 'ON'

    """

    http_methods = {
        "POST": requests.post,
        "GET": requests.get,
        "PUT": requests.put,
        "DELETE": requests.delete,
        "PATCH": requests.patch,
    }

    # Verifica se o método fornecido é válido
    method = method.upper()
    if method not in http_methods:
        raise ValueError(f"Método HTTP inválido. Use um dos seguintes: {', '.join(http_methods.keys())}.")

    # PROC PARA FINALIZAR PROCESSO
    url = link

    payload = payload_vars

    if print_response == True:
        print(f'payload: {payload}')

    headers = {"x-access-token": token}

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            # Realiza a requisição com o método correto
            if method == "GET" or method == "DELETE": response_insert = http_methods[method](url, params=payload, headers=headers)
            else: response_insert = http_methods[method](url, json=payload, headers=headers)

            response_insert.raise_for_status()

            if print_response == True:
                print(response_insert.json())

            status = response_insert.json()[0]['STATUS']
            print(status)

            if status != 200:
                print('Erro ao atualizar caso!')
                invoke_api_proc()

            return status

        except Exception as e:
            print(f"Tentativa {attempt} falhou: {e}")

            if attempt < max_attempts:
                print("Tentando novamente em 5 segundos...")
                time.sleep(5)
                continue

            else: raise ValueError("Api proc final falhou")

def invoke_api_proc_log(link, id_robo, token):
    """Só colocar o ID do robo e o Token direto """

    payload = {
        "id": id_robo
    }

    print(payload)

    headers = {
        "x-access-token": token}

    responseinsert = requests.request(
        "POST", link, json=payload, headers=headers)
    print(f"\n{responseinsert.json()}")

# FIX: Não funcional ainda, está aqui como base para o futuro
def captcha_solver():

    # Configurações
    API_KEY = "40efad0ffa6a4398bb7829185b1729e9"
    SITE_KEY = "6LeARtIZAAAAAEyCjkSFdYCBZG6JahcIveDriif3"  # A "sitekey" do reCAPTCHA
    PAGE_URL = "https://consorcio.cnpseguradora.com.br/"  # URL onde o CAPTCHA aparece

    def enviar_captcha():
        url = "https://2captcha.com/in.php"
        payload = {
            "key": API_KEY,
            "method": "userrecaptcha",
            "googlekey": SITE_KEY,
            "pageurl": PAGE_URL,
            "json": 1,
        }
        response = requests.post(url, data=payload)
        result = response.json()

        if result.get("status") == 1:
            return result.get("request")  # ID da tarefa
        else:
            raise Exception(f"Erro ao enviar CAPTCHA: {result.get('request')}")

    def verificar_captcha(task_id):
        url = "https://2captcha.com/res.php"
        payload = {
            "key": API_KEY,
            "action": "get",
            "id": task_id,
            "json": 1,
        }

        while True:
            response = requests.get(url, params=payload)
            result = response.json()

            if result.get("status") == 1:  # Solução disponível
                return result.get("request")  # TOKEN do CAPTCHA
            elif result.get("request") == "CAPCHA_NOT_READY":  # Ainda processando
                time.sleep(5)  # Aguardar antes de tentar novamente
            else:
                raise Exception(f"Erro ao verificar CAPTCHA: {result.get('request')}")

    def resolver_recaptcha():
        try:
            print("Enviando CAPTCHA para o TwoCaptcha...")
            task_id = enviar_captcha()
            print(f"Tarefa enviada! ID: {task_id}")

            print("Aguardando solução...")
            token = verificar_captcha(task_id)
            print(f"CAPTCHA resolvido! Token: {token}")

            return token
        except Exception as e:
            print(f"Erro: {e}")

    id = enviar_captcha()
    verificar_captcha(id)
    token_resolution = resolver_recaptcha()

    self.driver.execute_script("""
        var element = document.querySelector('input[id="g-recaptcha-response]"');
        if (element) {
            element.setAttribute('type', 'text');
        }
    """)

    self.driver.execute_script(f"""
    const element = document.querySelector('textarea[id="g-recaptcha-response"]');
    if (element) {{
        element.value = "{token_resolution}";
    }}
    """)


# ToDo: Continuar dps q validar as outras
# def invoke_depara_cliente():
#     """
#     Formato:
#         invoke_depara_cliente(parametros, )
#         - Parametros: https://linK_api.com.br/apis/views/depara/ { PARAMETROS/VAI/AQUI }
#     """

#     url = f"https://linK_api.com.br/apis/views/depara/{parametros}"

#     payload = {}
#     headers = {"x-access-token": token}
#     max_attempts = 5
#     for attempt in range(1, max_attempts + 1):
#         try:
#             response = requests.request("GET", url, json=payload, headers=headers)
#             print(response.json())

#             try:
#                 print(response.json()[0])
#                 gi.cliente = response.json()[0]['CLIENTE_BB']
#                 break
#             except BaseException:
#                 gi.obs = "Cliente Invalido ou não configurado"
#                 self.exibir_messagebox("Atenção", f'Atenção! Cliente Invalido ou não configurado para gerar as custas \n cliente:{gi.cliente} idcliente: {gi.id_cliente} \n cnpj: {gi.cnpj_autor}')
#                 break
#         except Exception as e:
#             print(f"Tentativa {attempt} falhou: {e}")
#             if attempt < max_attempts:
#                 print("Tentando novamente em 5 segundos...")
#                 time.sleep(5)
#                 continue
#             else:
#                 raise ValueError("Error no depara cliente")

# def invoke_delete_guias():
#     if gi.status != 3:

#         url = f'https://linK_api.com.br/apis/{self.url}'

#         payload = {"idguia": gi.id_tabela}

#         headers = {"x-access-token": token}

#         max_attempts = 5
#         for attempt in range(1, max_attempts + 1):
#             try:
#                 response = requests.delete(url, json=payload, headers=headers)
#                 # Lança uma exceção se a resposta não for bem-sucedida
#                 response.raise_for_status()
#                 print(response.json())
#                 print(f'{payload}, JSON: {response.json()}')
#                 status = response.json()[0]['STATUS']

#                 if status != 200:
#                     print('Erro ao deletar guias!')
#                     self.invoke_delete_guias()

#                 break

#             except Exception as e:
#                 print(f"Tentativa {attempt} falhou: {e}")

#                 if attempt < max_attempts:
#                     print("Tentando novamente em 5 segundos...")
#                     time.sleep(5)
#                     continue

#                 else:
#                     raise ValueError("Erro no delete guias")

# def invoke_insere_guias():

#     url = f'https://linK_api.com.br/apis/{self.url}'
#     # gi.link_servidor = 'https://bcfiles.bcfox.com.br/docs/arquivos/'

#     # ToDo: Ajustar variáveis quando tiver todas
#     payload = {
#         "idguia": gi.id_tabela,
#         "numseq": 1,
#         "status": gi.status,
#         "nomearquivo": gi.nome_arquivo,
#         "linkarquivo": f'{gi.link_servidor}{gi.nome_arquivo}',
#         "linhadigitavel": gi.linha_digitavel
#     }

#     headers = {"x-access-token": token}

#     max_attempts = 5
#     for attempt in range(1, max_attempts + 1):
#         try:
#             response_insert = requests.post(url, json=payload, headers=headers)
#             # Lança uma exceção se a resposta não for bem-sucedida
#             response_insert.raise_for_status()
#             print(f'Response.json: {response_insert.json()}')
#             print(f'Payload: {payload}')
#             status = response_insert.json()[0]['STATUS']

#             if status != 200:
#                 print('Erro ao inserir guias!')
#                 self.invoke_insere_guias()

#             gi.id_guia = response_insert.json()
#             break

#         except Exception as e:
#             print(f"Tentativa {attempt} falhou: {e}")

#             if attempt < max_attempts:
#                 print("Tentando novamente em 5 segundos...")
#                 time.sleep(5)
#                 continue

#             else:
#                 raise ValueError("Erro no insere guias")

# def valida_qtd_itens():
#     base_api_url = "https://linK_api.com.br/apis"
#     url = f"{base_api_url}/views/guias/iniciais/valida/itens"
#     self.tipo_guia = 'POS'

#     payload = {
#         "id": gi.id_tabela,
#         "uf": self.uf,
#         "tipo": self.tipo_guia,
#         "tipoguia": 0
#     }

#     headers = {
#         "x-access-token": token
#     }

#     max_attempts = 5

#     for attempt in range(1, max_attempts + 1):
#         try:
#             response = requests.request("PATCH", url, headers=headers, data=payload)
#             response_data = response.json()

#             # Exibe o retorno da API
#             print(response_data)

#             # Trata o retorno da API
#             status = response_data[0].get("STATUS")
#             if status == 200:
#                 print("Validação OK!")
#                 print(f"Quantidade Real: {response_data[0].get('QUANTIDADE_REAL')}")
#                 print(f"Quantidade Atual: {response_data[0].get('QUANTIDADE_ATUAL')}")
#                 return status
#             elif status == 400:
#                 print("Quantidade de arquivos no banco incorreta!")
#                 print("")
#                 self.exibir_messagebox(
#                     None, f"Quantidade que deveria ter: {
#                         response_data[0].get('QUANTIDADE_REAL')}\nQuantidade que possui: {
#                         response_data[0].get('QUANTIDADE_ATUAL')}\n")
#             else:
#                 print("Resposta inesperada da API.")
#                 self.exibir_messagebox(None, "Resposta inesperada da API.")

#             return response_data[0]

#         except Exception as e:
#             print(f"Tentativa {attempt} falhou: {e}")

#             if attempt < max_attempts:
#                 print("Tentando novamente em 5 segundos...")
#                 time.sleep(5)
#             else:
#                 print("Máximo de tentativas atingido. Falha ao validar quantidade de itens.")
#                 # Aqui pode ser adicionada uma ação caso o erro persista
#                 break