
from Core.RenameMDF import *
from Core.StatDan import *
from Core.CLFJson import *

import time

if __name__ == "__main__":
    StatDan.__setItem__("path_work", r"E:\MLserver\data\PS33SED\log\2020-06-30_15-21-49")

    _clf_json = CLFJson(StatDan.__getItem__("path_work") + "\\clf.json")
    StatDan.__setItem__("iclf_json", _clf_json)

    ext: str = '*.mdf'

    is_work = True
    _renamemdf = RenameMDF(StatDan.__getItem__("path_work"),  _clf_json, ext, is_work)
    _renamemdf.run1()
    while True:
        time.sleep(1.5)
