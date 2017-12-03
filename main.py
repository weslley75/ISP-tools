import os

from colorama import Fore, init

from frames.pingNa import pingna


def menu():
    init()
    os.system("cls || clear")
    os.system("title Heyapple's ISP Tools")
    print(Fore.GREEN + "-=-=-=-=-=-=" + Fore.YELLOW + "Heyapple's ISP Tools" +
          Fore.GREEN + "-=-=-=-=-=-=\n" + Fore.WHITE)
    print("\t1. Ping Nagios")
    print("\t2. Buscar Canais")
    print("\t3. Consulta IPs")
    print(Fore.GREEN + "\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" + Fore.WHITE)
    result = int(input("Selecione uma opção: "))
    actions = {1: pingna, 0: exit, }
    actions.get(result)()


menu()
