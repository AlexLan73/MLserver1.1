
from ConfigDan import *
import unittest
import pprint

class unit_test_configdan(unittest.TestCase):
    import os

    def test_path_config_default(self):
            config = ConfigDan()
            test0 = config.path_file_name_config
            print(test0)
            self.assertEqual(test0, self.os.getcwd()+"\\mlserver.json", 'incorrect path config default')
    #
    def test_path_config_test(self):
        path = r"E:\MLserver\MLServer1.0\Config\mlserver_test"
        config1 = ConfigDan(PathConfig = path)
        test0 = config1.path_file_name_config
        print(test0)
        self.assertEqual(test0, self.os.getcwd()+"\\mlserver_test.json", 'incorrect path config mlserver_test.json')

    def test_path_config_test_car(self):
        path = r"E:\MLserver\MLServer1.0\Config\mlserver_test"
        config = ConfigDan(PathConfig = path)
        dcar =  config.config_car
        pprint.pprint(dcar, width=1)
        _is = dcar !={}
        self.assertTrue(_is )

    def test_path_config_test_clexport(self):
        path = r"E:\MLserver\MLServer1.0\Config\mlserver_test"
        config = ConfigDan(PathConfig = path)
        config.set("PS0001")
        print(" config.clexport - ", config.clexport)
        _mdf = config.clexport["MDF"]
        print(" config.clexport -  MDF -  ", _mdf)
        print(" config.lrf_dec - ", config.lrf_dec)
        self.assertEqual(_mdf, "003", 'incorrect config.clexport MDF 003')
        self.assertEqual(config.lrf_dec, "004", 'incorrect config.lrf_dec CLF 004')



if __name__ == "__main__":
    print("   Unit test")
    _ut =  unit_test_configdan()

#     _config.set("PS0001")
