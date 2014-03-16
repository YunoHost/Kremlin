import requests
from time import sleep


def check_container_is_ready_to_be_installed(ip):
    for i in range(10):
        try:
            print "try to get the api for the %s time" % i
            response = requests.get("https://%s/ynhapi/installed" % ip, verify=False)
            installed = response.json()["installed"]
        except requests.ConnectionError as e:
            print "ConnectionError", e
            sleep(10)
            continue
        except ValueError as e:
            print "ValueError (probably json stuff)", e, [response.content]
            sleep(10)
            continue

        print "Return not installed where installed =", installed
        return not installed

    print "Fail to get api, return"
    return False
