import msvcrt
import os
import re
import subprocess
import time

from colorama import Fore, init
from terminaltables import DoubleTable

from scripts.back import back
from scripts.nagios import hosts

def input_timeout(prompt, timeout=120):
    finishat = time.time() + timeout
    tecla = []
    print(prompt)
    while True:
        if msvcrt.kbhit():
            tecla.append(msvcrt.getche())
            if tecla[-1] == b'\r':  # or \n, whatever Win returns;-)
                return None
            time.sleep(0.1)  # just to yield to other processes/threads
        else:
            if time.time() > finishat:
                return None


def pingna():
    try:
        init()
        os.system("title PingNa")
        os.system('mode con: cols=110 lines=30')
        par = {'hostgroup': 'all', 'style': 'hostdetail', 'hoststatustypes': '12', 'limit': '0'}
        while True:
            data = hosts(par)
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            info.wShowWindow = subprocess.SW_HIDE
            tableData = [['Nº', 'Host', 'IP', "Tempo", 'Status', 'Resposta']]  # create header of table
            for key, value in data['hosts'].items():  # loop of items get on Nagios
                output = subprocess.Popen(['ping', '-n', '1', '-w', '500', value['ip']], stdout=subprocess.PIPE,
                                          startupinfo=info).communicate()[0]  # ping host
                if b"destino inacess" in output:
                    tableData.append([key, str(value['host']), str(value['ip']), str(value['time']),
                                      Fore.YELLOW + "Inacessível" + Fore.WHITE, '--'])
                elif b"Esgotado o tempo limite do pedido" in output:
                    tableData.append([key, str(value['host']), str(value['ip']), str(value['time']),
                                      Fore.RED + "Offline" + Fore.WHITE, '--'])  # get real state of host
                else:
                    result = re.search(re.compile(b'(\d*ms)'), output)
                    tableData.append([key, str(value['host']), str(value['ip']), str(value['time']),
                                      Fore.GREEN + "Online" + Fore.WHITE,
                                      result.group(0).decode("utf-8")])
                os.system('cls || clear')  # clear the prompt for print table
                os.system("title PingNa - Problemas: " + str(data['problems']))  # print in the title number of issues
                if int(key) > 24:
                    os.system('mode con: cols=110 lines=' + str((int(key) + 9)))
                print(DoubleTable(tableData, "Pings").table)  # print the table
            input_timeout("\n\nPressione Enter para atualizar...")  # input with timer for refresh anytime
    except KeyboardInterrupt:
        back()  # on press Ctrl + C user back to menu
