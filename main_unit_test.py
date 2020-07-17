#
# import unittest
#
# class TestStringMethods(unittest.TestCase):
#
#   def test_upper(self):
#       self.assertEqual('foo'.upper(), 'FOO')
#
#   def test_isupper(self):
#       self.assertTrue('FOO'.isupper())
#       self.assertFalse('Foo'.isupper())
#
#   def test_split(self):
#       s = 'hello world'
#       self.assertEqual(s.split(), ['hello', 'world'])
#       # Проверим, что s.split не работает, если разделитель - не строка
#       with self.assertRaises(TypeError):
#           s.split(2)
#
# if __name__ == '__main__':
#     unittest.main()


from Core.ConfigDan import *
import unittest
import pprint

class unit_test_configdan(unittest.TestCase):
    import os
    #
    #
    # def test_upper(self):
    #   self.assertEqual('foo'.upper(), 'FOO')
    #
    # def test_isupper(self):
    #   self.assertTrue('FOO'.isupper())
    #   self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #   s = 'hello world'
    #   self.assertEqual(s.split(), ['hello', 'world'])
    #   # Проверим, что s.split не работает, если разделитель - не строка
    #   with self.assertRaises(TypeError):
    #       s.split(2)


    def test_path_config_default(self):
            config = ConfigDan()
            test0 = config.path_file_name_config
            print(test0)
            self.assertEqual(test0, self.os.getcwd()+"\\mlserver.json", 'incorrect path config default')

    def test_path_config_test(self):
        path = r"D:\MLServer\MLserver1.1\mlserver_test"
        config1 = ConfigDan(PathConfig = path)
        test0 = config1.path_file_name_config
        print(test0)
        self.assertEqual(test0, self.os.getcwd()+"\\mlserver_test.json", 'incorrect path config mlserver_test.json')

    def test_path_config_test_car(self):
        path = r"D:\MLServer\MLserver1.1\mlserver_test"
        config = ConfigDan(PathConfig = path)
        dcar =  config.config_car
        pprint.pprint(dcar, width=1)
        _is = dcar !={}
        self.assertTrue(_is )

    def test_path_config_test_clexport(self):
        path = r"D:\MLServer\MLserver1.1\mlserver_test"
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
    unittest.main()
    k=1

