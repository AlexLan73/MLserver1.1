import re
from datetime import datetime
import pprint
ls_trigger = [
                "Tue, 21.07.2020 13:34:18.00: Logger Firmware: 4.23",
                "Tue, 21.07.2020 13:34:18.00: Free Memory: 00476 GB, 65535 MB",
                "Tue, 21.07.2020 13:34:33.22: VIN number:",
                "Tue, 21.07.2020 13:35:12.02: Trigger 2 activated",
                "Tue, 21.07.2020 13:35:12.02: Trigger 4 activated",
                "Tue, 21.07.2020 13:35:12.32: Trigger 7 activated",
                "Tue, 21.07.2020 14:51:01.00: Trigger 2 activated",
                "Tue, 21.07.2020 14:51:01.00: Trigger 4 activated",
                "Tue, 21.07.2020 15:00:40.00: Shutdown reason:  0",
                "Tue, 21.07.2020 15:00:40.00: Free Memory: 00475 GB, 65535 MB",
                "Tue, 21.07.2020 15:00:57.00: Vehicle ID: PS33SED ",
                "Tue, 21.07.2020 15:00:57.00: Logger Configuratoin ID: UMPv0100",
                "Tue, 21.07.2020 15:00:57.00: Logger Firmware: 4.23",
                "Tue, 21.07.2020 15:00:57.00: Free Memory: 00475 GB, 65535 MB",
                "Tue, 21.07.2020 15:01:12.21: VIN number:",
                "Tue, 21.07.2020 15:01:47.58: Trigger 2 activated",
                "Tue, 21.07.2020 15:01:47.58: Trigger 4 activated",
                "Tue, 21.07.2020 15:01:47.88: Trigger 7 activated",
                "Tue, 21.07.2020 15:02:49.57: Trigger 3 activated",
                "Tue, 21.07.2020 15:34:04.72: Shutdown reason:  0",
                "Tue, 21.07.2020 15:34:04.72: Free Memory: 00474 GB, 65535 MB",
                ]
if __name__ == "__main__":
    _clf_data_trigger = dict()
    _clf_trigger_data = dict()
    for it in ls_trigger:

        if "trigger" in it.lower():
            print(it)
            __datatime = datetime.strptime(re.findall(r"\d+.\d+.\d+ \d+:\d+:\d+.\d+", it)[0], '%d.%m.%Y %H:%M:%S.%f')
            __trigger0 = it[it.lower().index("trigger"):]
            __trigger = __trigger0.split(" ")
            print("время1 {} \n триггер {}".format(__datatime, __trigger))
            _clf_data_trigger[__datatime]=__trigger[1:]
            _z = _clf_trigger_data.get(__trigger[1],dict())
            _z[__datatime]=__trigger[2]
            _clf_trigger_data[__trigger[1]]=_z
            k=1

    clf = dict()
    clf['data_trigger'] = _clf_data_trigger
    clf['trigger_data'] = _clf_trigger_data
    pprint.pprint(clf, width=1)
    pprint.pprint(clf, width=1)
