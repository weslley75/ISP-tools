import msvcrt
import os
import re
import subprocess
import time
import urllib.request
from configparser import ConfigParser

from colorama import Fore, init
from lxml import html
from terminaltables import DoubleTable

from scripts.back import back


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


def logar():
    config = ConfigParser()  # open config file
    config.read('config/hosts.cfg')
    host = (config.get('nagios', 'host'))
    login = (config.get('nagios', 'login'))  # get configs
    psw = (config.get('nagios', 'psw'))
    site = "http://" + host + "/nagios/cgi-bin/status.cgi?hostgroup=all&style=hostdetail&hoststatustypes=12"
    # get site by host in config file
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, site, login, psw)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)  # add password to manager
    opener = urllib.request.build_opener(handler)
    opener.open(site)  # create opener to site
    urllib.request.install_opener(opener)
    return urllib.request.urlopen(site).read().decode("utf-8")  # get nagios webpage content


def hosts():
    pag = logar()
    receive = {'hosts': {}}  # create dict
    tree = html.fromstring(pag)
    receive['problems'] = int(tree.xpath('//td[@class="hostTotalsPROBLEMS"]/text()')[0])  # get number of issues
    # noinspection PyTypeChecker
    for x in range(0, receive['problems']):
        receive['hosts'][str(x)] = {}
        receive['hosts'][str(x)]['host'] = tree.xpath('//td[@class="statusHOSTUNREACHABLE" or '
                                                      '@class="statusHOSTDOWN"]/a/text()')[x]
        receive['hosts'][str(x)]['ip'] = tree.xpath('//td[@class="statusHOSTUNREACHABLE" or '  # get hosts data
                                                    '@class="statusHOSTDOWN"]/a/@title')[x]  # (name, ip and time)
        receive['hosts'][str(x)]['time'] = tree.xpath('//td[(@class="statusBGUNREACHABLE" or @class="statusBGDOWN") '
                                                      'and not(@valign="center") and contains(text(), "d")]/text()')[x]
    return receive


def pingna():
    try:
        init()
        os.system("title PingNa")
        os.system('mode con: cols=110 lines=30')
        while True:
            data = hosts()
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
