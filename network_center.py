import os

def get_networks():
    os.system("/System/Library/PrivateFrameworks/Apple80211.framework/"
              "Versions/Current/Resources/airport -s >> ssid_scan.txt")


if __name__ == '__main__':
    get_networks()