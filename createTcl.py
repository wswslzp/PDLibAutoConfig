from functools import reduce
import time
from jsonConfig import PdConfig
from libManager import *

class TclFactory(object):
    def __init__(self, config: PdConfig) -> None:
        super().__init__()
        self.config = config
        self.mmmcPath = ""
    
    @property
    def getJsonConfig(self):
        return self.config.config

    def printRC(self):
        ret = ""
        for rc in self.getJsonConfig['rcCorner']:
            ret += "create_rc_corner"
            ret += " -name " + rc 
            ret += " -T " + str(self.getJsonConfig['rcCorner'][rc]['temperature'])
            ret += " -preRoute_res " + str(self.getJsonConfig['rcCorner'][rc]['factor']['preRoute']['resistance']).replace('[','{').replace(']', '}')
            ret += " -preRoute_cap "+ str(self.getJsonConfig['rcCorner'][rc]['factor']['preRoute']['capacitance']).replace('[','{').replace(']', '}')
            ret += " -preRoute_clkres "+ str(self.getJsonConfig['rcCorner'][rc]['factor']['preRoute']['clockResistance']).replace('[','{').replace(']', '}')
            ret += " -preRoute_clkcap "+ str(self.getJsonConfig['rcCorner'][rc]['factor']['preRoute']['clockCapacitance']).replace('[','{').replace(']', '}')
            ret += " -postRoute_res "+ str(self.getJsonConfig['rcCorner'][rc]['factor']['postRoute']['resistance']).replace('[','{').replace(']', '}')
            ret += " -postRoute_cap "+ str(self.getJsonConfig['rcCorner'][rc]['factor']['postRoute']['capacitance']).replace('[','{').replace(']', '}')
            ret += " -postRoute_clkres "+ str(self.getJsonConfig['rcCorner'][rc]['factor']['postRoute']['clockResistance']).replace('[','{').replace(']', '}')
            ret += " -postRoute_clkcap "+ str(self.getJsonConfig['rcCorner'][rc]['factor']['postRoute']['clockCapacitance']).replace('[','{').replace(']', '}')
            ret += " -postRoute_xcap "+ str(self.getJsonConfig['rcCorner'][rc]['factor']['postRoute']['resistance']).replace('[','{').replace(']', '}')
            # ret += " -postRoute_clkxcap "+ str(self.getJsonConfig['rcCorner'][rc]['factor']['postRoute']['resistance']).replace('[','{').replace(']', '}')
            ret += " -qx_tech_file " + str(self.getJsonConfig['rcCorner'][rc]['qrcTechFile'])
            ret += "\n"
        return ret

    def printLibSet(self):
        ret = ""
        for libSet in self.getJsonConfig['library']:
            ret += "create_library_set"
            ret += " -name " + libSet
            ret += " -timing " + '{'
            if len(self.getJsonConfig['library'][libSet]) > 1:
                ret += reduce(lambda a,b: a + " " + b, self.getJsonConfig['library'][libSet])
            else:
                ret += self.getJsonConfig['library'][libSet][0]
            ret += "}\n"
        return ret

    def printCons(self):
        ret = ""
        for cons in self.getJsonConfig['constraint']:
            if self.getJsonConfig['constraint'][cons]['sdcFile']['preCTS'] != "":
                ret += "create_constraint_mode -name " + cons 
                ret += " -sdc_files {" + self.getJsonConfig['constraint'][cons]['sdcFile']['preCTS'] + "}\n"
            else:
                self.getJsonConfig['constraint'].pop(cons)
        return ret

    def printDelayCorner(self, isOCV: bool = False):
        ret = ""
        for corner in self.getJsonConfig['delayCorner']:
            ret += "create_delay_corner -name " + corner
            ret += " -rc_corner " + self.getJsonConfig['delayCorner'][corner]['rcCorner']
            # TODO: early lib set and late lib set
            # if not isOCV:
            ret += " -library_set " + "{" + self.getJsonConfig['delayCorner'][corner]['library'] + "}\n"
        return ret

    def printView(self):
        ret = ""
        for view in self.getJsonConfig['mmmcView']:
            ret += "create_analysis_view -name " + view 
            ret += " -constraint_mode {" + self.getJsonConfig['mmmcView'][view]['constraint'] + "}"
            ret += " -delay_corner {" + self.getJsonConfig['mmmcView'][view]['delayCorner'] + "}\n"
        return ret

    def printMMMCFile(self, viewPath: str):
        self.mmmcPath = viewPath
        with open(viewPath, "w") as f:
            content = ""
            content += "# Version:1.0 MMMC View Definition File\n"
            content += "# Do Not Remove Above Line\n"
            content += self.printRC() + "\n"
            content += self.printLibSet() + "\n"
            content += self.printCons() + "\n"
            content += self.printDelayCorner() + "\n"
            content += self.printView() + "\n"
            f.write(content)

    def printGlobals(self, globalPath: str):
        from functools import reduce
        def mkString(contextList, sep=" "):
            return reduce(lambda a,b: a + sep + b, contextList)
        with open(globalPath, 'w') as f:
            content = f"""
###############################################################
#  Generated by:      PD Flow Gen Tool
#  Generated on:      {time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())}
#  Design:            {self.config.config['designData']['design']}
###############################################################
#
# Version 1.1
#\n
"""
            content += "set init_lef_file {" + mkString(self.config.config['physicalData']['lef']) + "}\n"
            content += "set init_mmmc_file {" + self.mmmcPath + "}\n"
            content += "set init_pwr_net {" + mkString(self.config.config['designData']['powerGround']['power']) + "}\n"
            content += "set init_gnd_net {" + mkString(self.config.config['designData']['powerGround']['ground']) + "}\n"
            content += "set init_io_file {" + self.config.config['designData']['ioFile'] +" }\n"
            content += "set init_top_cell {" + self.config.config['designData']['design'] + "}\n"
            content += "set init_verilog {" + self.config.config['designData']['netlist'] + "}\n"
            f.write(content)

if __name__ == "__main__":
    config = PdConfig().readJson("test.json")
    factory = TclFactory(config)
    factory.printMMMCFile("test.view")