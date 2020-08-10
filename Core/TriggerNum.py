from pathlib import Path
from datetime import datetime
import re

from .ReadWrite import *


def TriggerNum(work_dir):
    rw = ReadWrite(work_dir)
    fname = Path(work_dir + "\\TextLog.txt")

    if not (fname.exists()):
        return dict(), dict()

    ls_file = rw.ReadText(work_dir + "\\TextLog.txt")

    _clf_data_trigger = dict()
    _clf_trigger_data = dict()

    for it in ls_file:
        if "trigger" in it.lower():
            print(it)
            __datatime = datetime.strptime(re.findall(r"\d+.\d+.\d+ \d+:\d+:\d+.\d+", it)[0],
                                           '%d.%m.%Y %H:%M:%S.%f')
            __trigger0 = it[it.lower().index("trigger"):]
            __trigger = __trigger0.split(" ")
            _clf_data_trigger[str(__datatime)] = __trigger[1:]
            _z = _clf_trigger_data.get(__trigger[1], dict())
            _z[str(__datatime)] = __trigger[2]
            _clf_trigger_data[__trigger[1]] = _z
    return _clf_data_trigger, _clf_trigger_data
