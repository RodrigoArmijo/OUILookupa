import sys
import getopt
import http.client
import json
import time
import subprocess

API_HOST = "api.maclookup.app"
API_PATH = "/v2/macs/"

def get_mac_vendor(mac):
    start_time = time.time()
    conn = http.client.HTTPSConnection(API_HOST)
    conn.request("GET", API_PATH + mac)
    response = conn.getresponse()
    response_time = round((time.time() - start_time) * 1000)

    if response.status == 200:
        data = response.read()
        result = json.loads(data)
        vendor = result.get('company', 'Not found')
        print(f"MAC address : {mac}\nFabricante : {vendor}\nTiempo de respuesta: {response_time}ms")
    else:
        print(f"MAC address : {mac}\nFabricante : Not found\nTiempo de respuesta: {response_time}ms")
    conn.close()

def get_arp_table():
    arp_output = subprocess.check_output(['arp', '-a']).decode()
    print("IP/MAC/Vendor:")
    for line in arp_output.split('\n'):
        if line:
            parts = line.split()
            ip, mac = parts[0], parts[1]
            get_mac_vendor(mac)

def print_help():
    print("Use: OUILookup.py --mac <mac> | --arp | [--help]")
    print("--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.")
    print("--arp: muestra los fabricantes de los hosts disponibles en la tabla arp.")
    print("--help: muestra este mensaje y termina.")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:a", ["mac=", "arp", "help"])
        if not opts:
            print_help()
            sys.exit()
        for opt, arg in opts:
            if opt in ("--mac", "-m"):
                get_mac_vendor(arg)
            elif opt in ("--arp", "-a"):
                get_arp_table()
            elif opt == "--help":
                print_help()
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

if __name__ == "__main__":
    main()
