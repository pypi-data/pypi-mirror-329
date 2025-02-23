#coding:utf8
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    配置文件(yaml)处理
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys
from ruamel.yaml import YAML

# 初始化ruamel.yaml的RoundTripLoader和RoundTripDumper
yaml = YAML(typ='rt')

basePath = os.path.dirname(os.path.realpath(sys.argv[0]))

class Config:
    def __init__(self, configFile):
        self.configpath = basePath + configFile

        self.ymDict = None
        with open(self.configpath, 'r',encoding='utf-8') as f:
            self.ymDict = yaml.load(f)

    def getValue(self, section, option):
        try:
            value = None
            if option != None:
                value = self.ymDict[section][option]
            else:
                value = self.ymDict[section]
            return value
        except Exception as e:
            return None

    def setValue(self, section, option, val):
        try:
            with open(self.configpath,'r',encoding='utf-8') as f:
                result = f.read()
                FileConf = yaml.load(result)

                FileConf[section][option] = val

                with open(self.configpath,'w',encoding='utf-8') as w_f:
                    yaml.dump(FileConf, w_f)

        except Exception as e:
            print(str(e))
            return None

# if __name__ == '__main__':
#     ConfigYaml = Config(configFile="config.yaml")
#     print(ConfigYaml.getValue('detectorCon','color'))