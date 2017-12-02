import os
from colorama import Fore, init

def menu():
    init()
    os.system("cls || clear")
    print(Fore.GREEN + "-=-=-=-=-=-="+ Fore.YELLOW + "Heyapple's ISP Tools" +
          Fore.GREEN + "-=-=-=-=-=-=\n" + Fore.WHITE)
    print("\t1. Ping Nagios")
    print("\t2. Buscar Canais")
    print("\t3. Consulta IPs")
    print(Fore.GREEN + "\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" + Fore.WHITE)
    return(input("Selecione uma opção: "))

menu()
