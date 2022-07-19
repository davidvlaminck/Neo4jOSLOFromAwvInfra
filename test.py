if __name__ == '__main__':
    import os
    import requests
    print("Hello, World!")
    page_num = 10000
    page_size = 100
    crt="C:\\resources\\datamanager_eminfra_prd.awv.vlaanderen.be.crt"
    key = "C:\\resources\\datamanager_eminfra_prd.awv.vlaanderen.be.key"
    if not os.path.isfile(crt):
        raise FileNotFoundError(crt + " is not a valid path. Cert file does not exist.")
    if not os.path.isfile(key):
        raise FileNotFoundError(key + " is not a valid path. Key file does not exist.")
    url = f'https://services.apps.mow.vlaanderen.be/eminfra/feedproxy/feed/assets/{page_num}/{page_size}'
    response = requests.get(url=url, cert=(crt, key))
    decoded_string = response.content.decode("utf-8")
    print(decoded_string)