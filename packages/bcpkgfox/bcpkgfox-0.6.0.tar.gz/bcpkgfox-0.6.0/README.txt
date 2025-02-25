#nota Token único api: pypi-AgEIcHlwaS5vcmcCJDNiOTVjMjFlLTdiNWEtNGY1OC1hYmUxLTBiODQ0ZjM5MGJjYQACKlszLCI2MjE4YTk4OC1hOTg3LTQ4ODAtOGQ4MC0wZDZlNzZiZDE3NTMiXQAABiCpcLmagfgWs5kIeHr_0k3jDMXjsyRD51lu3Cs2X_3LIQ


Para lançar uma versão nova da bibliotca:

    - 1° Verifique se você tem o arquivo de autenticação .pypirc:
        Na pasta de do seu usuário (C:\Users\eliezer.gimenes), deve conter o arquivo com o nome ".pypirc"
        E dentro dele tem que ter o seguinte conteúdo:

            """
            [distutils]
            index-servers =
                pypi

            [pypi]
            repository: https://upload.pypi.org/legacy/
            username = bcfoxtecnologia
            password = pypi-AgEIcHlwaS5vcmcCJDNiOTVjMjFlLTdiNWEtNGY1OC1hYmUxLTBiODQ0ZjM5MGJjYQACKlszLCI2MjE4YTk4OC1hOTg3LTQ4ODAtOGQ4MC0wZDZlNzZiZDE3NTMiXQAABiCpcLmagfgWs5kIeHr_0k3jDMXjsyRD51lu3Cs2X_3LIQ
            """

    - 2° Instale essas bibliotecas:
        pip install setuptools twine

    - 3° Depois de ter altualizado o código da biblioteca, mude a versão no arquivo chamado "Setup.py"
        Exemplo:
            Na linha 'version="0.1.5"' mude para a versão seguinte, 'version="0.1.6"'

    - 4° Salve o setup.py e gere o novo executável:
        Abra um terminal no diretório do arquivo e cole o seguinte comando:
            'python setup.py sdist bdist_wheel'

    - 5° Remova a versão antiga:
        Depois de ter gerado o comando de exec, terá a versão nova e a antiga dentro da pasta dist
        Apague o .whl e o .tar.gz da versão antiga

        Exemplo:
            BCFOX/
            │
            ├── bcpkgfox/
            │
            ├── bcpkgfox.egg-info/
            │
            ├── build/
            │
            ├── dist/
            │   ├── BCFOX-0.1.5-py3-none-any.whl  (apagar)
            │   ├── BCFOX-0.1.6-py3-none-any.whl  (versão nova)
            │   │
            │   ├── bcfox-0.1.5.tar.gz            (apagar)
            │   └── bcfox-0.1.6.tar.gz            (versão nova)
            │
            ├── README.md
            └── setup.py

    - 6° Push:
        Em um terminal dentro de repositório:
            twine upload dist/*