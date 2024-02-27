import requests

class Offsets:

    def __init__(self) -> None:
        try:
            print('[sigma-kit] Fetching offsets...')
            self._ = requests.get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/generated/offsets.json').json()
            self.CLIENT_DLL = requests.get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/generated/client.dll.json').json()
            print('[sigma-kit] Fetched offsets.')
        except:
            print('[sigma-kit] Unable to get offsets. Check your internet connection and try again.')
            exit()

    def getOffset(self, a: str) -> int:
        try:
            return self._['client_dll']['data'][a]['value']
        except:
            print(f'[sigma-kit] [getOffset] couldnt get {a} (?invalid name?)')
            exit()

    def getClientOffset(self, __f: str, __s: str) -> int:
        try:
            return self.CLIENT_DLL[__f]['data'][__s]['value']
        except:
            print(f'[sigma-kit] [getClientOffset] couldnt get {__f} ~> {__s}')
            exit()
