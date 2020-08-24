# pyinstaller -F TestPathMLServer.py

import os, sys
from pathlib import Path

def test_environment_windows():
    print("- ClexportXX.test_environment_windows() \n -- чтение где лежит MLserver ")
    _mlserver = str(os.environ.get("MLSERVER1", ""))
    print(" ********************   ", _mlserver)
    if len(_mlserver) <= 0:
            print("Не прописана системная переменная MLSERVER -> путь к каталогу \n "
                  " к примеру C:\Program Files (x86)\GIN\MLserver")
            print("Не прописана системная переменная MLSERVER -> путь к каталогу")
            sys.exit(-2)
    else:
        print(" Системная переменная MLSERVER -> путь к каталогу - прописана ")
    return _mlserver

if __name__=="__main__":
    _path_MLServer = test_environment_windows()
    _drive = Path(_path_MLServer).drive
    os.chdir(_drive)
    os.chdir(_path_MLServer)
    ls= list(Path(_path_MLServer).glob("siglog.dll"))
    if ls:
        print("Нужный каталог !!!!")
        print(*ls)
    else:
        print(":(((  ~~~~")

    k=1
