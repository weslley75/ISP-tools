import re
import telnetlib
import time
import os

from terminaltables import DoubleTable

from scripts.nagios import hosts
from scripts.back import back


def cid():
    try:
        torre = input("Digite o número da torre: ")
        timeout = 1
        result = None
        datatable = [['Interface', 'IP', 'Canal']]
        for key, value in hosts(None)['hosts'].items():
            canal = False
            if re.match(r'InterfaceAPT' + re.escape(torre) + r'[A-Z_-]', value['host']):
                host = value['ip']
                try:
                    session = telnetlib.Telnet(host, 23, timeout)
                except IOError:
                    canal = "Timeout"
                else:
                    time.sleep(0.2)
                    tipo = session.read_until(b"hardware", 1)
                    if re.search(r'MikroTik.*', tipo.decode("UTF-8")) is not None:
                        canal = "MikroTik"
                    else:
                        session.write("ubnt".encode('ascii') + b"\r")
                        time.sleep(0.2)
                        session.write("unimanu".encode('ascii') + b"\r")
                        time.sleep(0.2)
                        session.write("head -10000 /tmp/system.cfg | grep radio.1.freq".encode('ascii') + b"\r")
                        output = session.expect([re.compile(b"hardware", 1)])
                        result = re.search(r'radio.1.freq=(\d*)', output.decode("UTF-8"))
                        if not result:
                            time.sleep(0.2)
                            session.write("more /tmp/system.cfg | grep radio.1.channel".encode('ascii') + b"\r")
                            output = session.read_until(b"hardware", 1)
                            result = re.search(r'radio.1.channel=(\d*)', output.decode("UTF-8"))
                            if result:
                                canal = ((int(result.group(1)) * 5) + 5000)
                        else:
                            canal = result.group(1)
                    session.close()
                if canal:
                    datatable.append([value['host'], value['ip'], canal])
                    os.system("cls || clear")
                    print(DoubleTable(datatable).table)
        input("Pressione enter para sair...")
        back()
    except KeyboardInterrupt:
        back()
