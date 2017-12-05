from terminaltables import DoubleTable

from scripts.nagios import hosts
from scripts.back import back


def search():
    try:
        var = input("Pesquisar: ")
        data = hosts()
        datatable = [["Host", "IP"]]
        for key, host in data['hosts'].items():
            if var.lower() in host['host'].lower():
                datatable.append([host['host'], host['ip']])
        print("\n" + DoubleTable(datatable, "Resultado").table)
        input("Pressione Enter para voltar...")
        back()
    except KeyboardInterrupt:
        back()
