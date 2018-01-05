import requests

from scripts.back import back

def mac():
    try:
        mac = input("Digite o mac: ")
        url = "http://macvendors.co/api/{}/json".format(mac)
        r = requests.get(url=url).json()
        if 'error' in r['result']:
            print("MAC Inválido ou sem cadastro")
        else:
            print(r['result']['company'])
        input("Pressione Enter para voltar...")
        back()
    except KeyboardInterrupt:
        back()  # on press Ctrl + C user back to menu