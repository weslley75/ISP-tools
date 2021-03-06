from configparser import ConfigParser
from lxml import html
import urllib.request


def logar(par=None):
    if par is None:
        par = {'hostgroup': 'all', 'style': 'hostdetail', 'hoststatustypes': '2', 'limit': '0'}
    config = ConfigParser()  # open config file
    config.read('config/hosts.cfg')
    host = (config.get('nagios', 'host'))
    login = (config.get('nagios', 'login'))  # get configs
    psw = (config.get('nagios', 'psw'))
    site = "http://" + host + "/nagios/cgi-bin/status.cgi?" # todo if nagios or interface
    for key, value in par.items():
        site += key + "=" + value + "&"
    # get site by host in config file
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, site, login, psw)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)  # add password to manager
    opener = urllib.request.build_opener(handler)
    opener.open(site)  # create opener to site
    urllib.request.install_opener(opener)
    return urllib.request.urlopen(site).read().decode("utf-8")  # get nagios webpage content


def hosts(par=None):
    pag = logar(par)
    receive = {'hosts': {}}  # create dict
    tree = html.fromstring(pag)
    receive['problems'] = int(tree.xpath('//td[@class="hostTotalsPROBLEMS"]/text()')[0])  # get number of issues
    host = tree.xpath('//td[@class="statusHOSTUNREACHABLE" or '
                      '@class="statusHOSTDOWN" or @class="statusHOSTUP"]/a/text()')
    ip = tree.xpath('//td[@class="statusHOSTUNREACHABLE" or @class="statusHOSTDOWN" or '
                    '@class="statusHOSTUP"]/a/@title')  # (name, ip and time)
    time = tree.xpath('//td[(@class="statusBGUNREACHABLE" or @class="statusBGDOWN" or '
                      '@class="statusEven" or @class="statusOdd") and not(@valign="center") and '
                      'contains(text(), "d")]/text()')
    for x in range(0, len(time)):
        receive['hosts'][str(x)] = {}
        receive['hosts'][str(x)]['host'] = host[x]
        receive['hosts'][str(x)]['ip'] = ip[x]
        receive['hosts'][str(x)]['time'] = time[x]
    return receive
