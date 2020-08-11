from datetime import datetime
from pprint import pprint
from pathlib import Path
import re

if __name__ == "__main__":

    _all_files = [
        "10F0", "22F1", "0_F2"
    ]

    _files = len([x for x in _all_files if len(re.findall(r'\dF', str(x))) > 0])

    k = 1
    _x = r"E:\MLserver\data\PS33SED\log\2020-06-30_15-21-49"
    _root = Path(_x).root
    _drive = Path(_x).drive
    _z = r"C:\Program Files (x86)\GIN\MLserver"
    _ls = list(Path(_z).glob("*.ini"))
    k = 1

    xx = dict(short='dict', long='dictionary')

    _triggerName = {1: "RemKey1",
                    2: "ABS_Lamp_1",
                    3: "CCU_Failure_gt_0",
                    4: "EBD_Lamp_1",
                    5: "BLS_Fault_1",
                    6: "EPB_FailureSts_1",
                    7: "HvSystemFailure_gt_1",
                    8: "MIL_OnRq_1",
                    9: "stGbxMILReq_1",
                    10: "TM_WarningInd_1"
                    }

    __maska0_datatime = r'%d.%m.%Y %H:%M:%S.%f'
    _clf_data_trigger = dict()
    _clf_data_trigger[datetime.strptime("21.06.2020 13:32:57.763873", __maska0_datatime)] = 2
    _clf_data_trigger[datetime.strptime("21.06.2020 14:32:57.763873", __maska0_datatime)] = 1
    _clf_data_trigger[datetime.strptime("21.06.2020 15:32:57.763873", __maska0_datatime)] = 3
    _clf_data_trigger[datetime.strptime("21.06.2020 13:32:55.763873", __maska0_datatime)] = 4

    __start = datetime.strptime("21.06.2020 13:31:57.000000", __maska0_datatime)
    __end = datetime.strptime("21.06.2020 13:34:02.769873", __maska0_datatime)

    pprint(_clf_data_trigger, width=1)
    __d = dict()
    __file_num_trig = ""
    for key, val in _clf_data_trigger.items():
        print(key)
        if (key >= __start) and (key <= __end):
            print("!!!")
            __d[key] = [val, _triggerName[val]]
            __file_num_trig += "_({})".format(val)

    print(" ===>  ", __file_num_trig)
    pprint(__d, width=1)
    __d_key = list(__d.keys())
    print("**" * 45)
    for it in __d_key: del _clf_data_trigger[it]
    pprint(_clf_data_trigger, width=1)

    k = 1

#         self.self._all_file.dclf.get("TriggerName", dict())
#
#             "Start": "21.06.2020 13:32:57.000000",
#         "Trigger": "21.06.2020 13:32:57.763873",
#         "TriggerX":{
#                     2:["21.06.2020 13:32:57.763873", "Stop",
#                     3:"21.06.2020 13:32:57.763873",
#                   }
#         "End": "21.06.2020 13:33:02.769873"
