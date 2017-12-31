import re
import telnetlib
import os

from terminaltables import DoubleTable
from colorama import init, Fore
from collections import Counter

from scripts.nagios import hosts
from scripts.back import back


def diferente(canal, lst):
    if Counter(lst)[str(canal)] > 1:
        return Fore.RED + str(canal) + Fore.WHITE
    else:
        return str(canal)


def cid():
    try:
        init()
        torre = input("Digite o número da torre: ")
        timeout = 1
        tableData = [['Interface', 'IP', 'Canal']]
        lista = []
        for key, value in hosts()['hosts'].items():
            result = False
            canal = False
            if re.match(r'InterfaceAPT' + re.escape(torre) + r'[A-Z_-]?', value['host']):
                host = value['ip']
                try:
                    session = telnetlib.Telnet(host, 23, timeout)
                except IOError:
                    canal = "Timeout"
                else:
                    tipo = session.expect([re.compile(b".*[Ll]ogin:")], timeout)
                    if re.search(r'MikroTik.*', tipo[2].decode("UTF-8")) is not None:
                        canal = "MikroTik"
                    else:
                        session.write("ubnt".encode('ascii') + b"\r")
                        session.expect([re.compile(b"[Pp]assword:")], timeout)
                        session.write("unimanu".encode('ascii') + b"\r")
                        session.expect([re.compile(b".*#")], timeout)
                        session.write("head -10000 /tmp/system.cfg | grep radio.1.freq".encode('ascii') + b"\r")
                        output = session.expect([re.compile(b".*#")], timeout)
                        result = re.search(r'radio.1.freq=(\d*)', output[2].decode("UTF-8"))
                        if not result:
                            session.write("more /tmp/system.cfg | grep radio.1.channel".encode('ascii') + b"\r")
                            output = session.expect([re.compile(b".*#")], timeout)
                            result = re.search(r'radio.1.channel=(\d*)', output[2].decode("UTF-8"))
                            if result:
                                canal = ((int(result.group(1)) * 5) + 5000)
                        else:
                            canal = int(result.group(1))
                    session.close()
                if canal == 0:
                    canal = "Automático"
                elif canal and not canal == "Timeout":
                    lista.append(str(canal))
                else:
                    canal = "ERROR"
                tableData.append([value['host'], value['ip'], diferente(canal, lista)])
                os.system("cls")
                print(DoubleTable(tableData).table)
        input("Pressione enter para sair...")
        back()
    except KeyboardInterrupt:
        back()
