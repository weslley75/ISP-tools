import os

from colorama import Fore, init
from sys import exit

from frames.pingNa import pingna
from frames.cid import cid
from frames.search import search
from frames.mac import mac


def menu():
    try:
        init()
        os.system("cls || clear")
        os.system("title Heyapple's ISP Tools")
        print(Fore.GREEN + "-=-=-=-=-=-=" + Fore.YELLOW + "Heyapple's ISP Tools" +
              Fore.GREEN + "-=-=-=-=-=-=\n" + Fore.WHITE)
        print("\t1. Ping Nagios")
        print("\t2. Buscar Canais")
        print("\t3. Consulta IPs")
        print("\t4. Consulta MACs")
        print(Fore.GREEN + "\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" + Fore.WHITE)
        result = int(input("Selecione uma opção: "))
        actions = {1: pingna, 2: cid, 3: search, 4: mac, 0: exit, }
        actions.get(result)()
    except KeyboardInterrupt:
        exit()


menu()
