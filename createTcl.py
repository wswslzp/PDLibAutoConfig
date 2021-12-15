from functools import reduce

from jsonConfig import PdConfig
from libManager import *

class TclFactory(object):
    def __init__(self, config: PdConfig) -> None:
        super().__init__()
        self.config = config
    
    @property
    def getJsonConfig(self):
        return self.config.config

    def printRC(self):
        ret = ""
        for rc in self.getJsonConfig['rcCorner']:
            ret += "create_rc_corner"
            ret += "-name " + rc 
            ret += "-T" + str(self.getJsonConfig['rcCorner'][rc]['temperature'])
            ret += "-preRoute_res " + str(self.getJsonConfig['rcCorner'][rc]['preRoute']['resistance'])
            ret += "-preRoute_cap "+ str(self.getJsonConfig['rcCorner'][rc]['preRoute']['capacitance'])
            ret += "-preRoute_clkres "+ str(self.getJsonConfig['rcCorner'][rc]['preRoute']['clockResistance'])
            ret += "-preRoute_clkcap "+ str(self.getJsonConfig['rcCorner'][rc]['preRoute']['clockCapacitance'])
            ret += "-postRoute_res "+ str(self.getJsonConfig['rcCorner'][rc]['postRoute']['resistance'])
            ret += "-postRoute_cap "+ str(self.getJsonConfig['rcCorner'][rc]['postRoute']['capacitance'])
            ret += "-postRoute_clkres "+ str(self.getJsonConfig['rcCorner'][rc]['postRoute']['clockResistance'])
            ret += "-postRoute_clkcap "+ str(self.getJsonConfig['rcCorner'][rc]['postRoute']['clockCapacitance'])
            ret += "-postRoute_xcap "+ str(self.getJsonConfig['rcCorner'][rc]['postRoute']['resistance'])
            ret += "-postRoute_clkxcap "+ str(self.getJsonConfig['rcCorner'][rc]['postRoute']['resistance'])
            ret += "\n"
        return ret

    def printLibSet(self):
        ret = ""
        for libSet in self.getJsonConfig['library']:
            ret += "create_library_set"
            ret += "-name " + libSet
            ret += "-timing " + '{'
            if len(self.getJsonConfig['library'][libSet]) > 1:
                ret += reduce(lambda a,b: a + " " + b, self.getJsonConfig['library'][libSet])
            else:
                ret += self.getJsonConfig['library'][libSet][0]
            ret += "}\n"
        return ret

    def printCons(self):
        ret = ""
        for cons in self.getJsonConfig['constraint']:
            ret += "create_constraint_mode -name " + cons 
            ret += "-sdc_files {" + self.getJsonConfig['constraint'][cons]['sdcFile']['preCTS'] + "}\n"
        return ret

    def printDelayCorner(self):
        ret = ""
        for corner in self.getJsonConfig['delayCorner']:
            ret += "create_delay_corner -name " + corner
            ret += "-rc_corner" + self.getJsonConfig['delayCorner'][corner]['rcCorner']
            # TODO: early lib set and late lib set
            ...
        return ret

    def printView(self):
        ret = ""
        for view in self.getJsonConfig['mmmcView']:
            ret += "create_analysis_view -name " + view 
            ret += "-constraint_mode {" + self.getJsonConfig['mmmcView'][view]['constraint'] + "}"
            ret += "-delay_corner {" + self.getJsonConfig['mmmcView'][view]['delayCorner'] + "}\n"
        return ret

    def printMMMCFile(self, viewPath: str):
        with open(viewPath, "w") as f:
            content = self.printRC()
            content += self.printLibSet()
            content += self.printCons()
            content += self.printDelayCorner()
            content += self.printView()
            f.write(content)
