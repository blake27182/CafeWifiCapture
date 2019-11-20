import os


def get_ssid_list():
    if os.path.exists("ssid_scan.txt"):
        os.remove('ssid_scan.txt')
    os.system("/System/Library/PrivateFrameworks/Apple80211.framework/"
              "Versions/Current/Resources/airport -s >> ssid_scan.txt")

    with open('ssid_scan.txt', 'r') as f:
        ssids = []
        first = True
        for line in f:
            if first:
                first = False
                continue
            ssids.append(line[:line.find(':')-3].strip())

    return sorted(ssids)


def sign_in(ssid, password):
    # try to sign in
    # if it works, return a True
    # if not, return a False
    pass


if __name__ == '__main__':
    network_names = get_ssid_list()
    for name in network_names:
        print(name)

