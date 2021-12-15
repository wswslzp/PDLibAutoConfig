from libManager import *
import json
import os

template = {
    "globalData": {
        "version": 20.2
    },
    "physicalData": {
        "process": 55,
        "lef": []
    },
    "designData": {
        "netlist": "",
        "design": "",
        "floorPlan": "",
        "powerGround": {
            "power": "VDD_CORE",
            "ground": "VSS_CORE"
        },
        "ctsCell": [],
        "flow": "mmmc",
        "enableOCV": "pre_postcts"
    },
    "library": {
        "*": []
    },
    "rcCorner": {
        "typical": {
            "qrcTechFile": "",
            "capTable": "",
            "temperature": 25, 
            "factor": {
                "preRoute": {
                    "resistance": 1,
                    "capacitance": 1, 
                    "clockResistance": 0,
                    "clockCapacitance": 0
                },
                "postRoute": {
                    "resistance": [1, 1, 1],
                    "capacitance": [1, 1, 1], 
                    "clockResistance": [0, 0, 0],
                    "clockCapacitance": [0, 0, 0]
                }
            }
        }
    },
    "enableCPPR": True,
    "delayCorner": {
        "typical": {
            "rcCorner": "typical",
            "library": "*",
            "derateFactor": {
                "clock": {
                    "cell": {
                        "early": 1, 
                        "late": 1
                    },
                    "net": {
                        "early": 1,
                        "late": 1
                    }
                },
                "data": {
                    "cell": {
                        "early": 1, 
                        "late": 1
                    },
                    "net": {
                        "early": 1,
                        "late": 1
                    }
                }
            }
        }
    },
    "constraint": {
        "func": {
            "sdcFile": {
                "preCTS": "",
                "incrCTS": "",
                "postCTS": ""
            }
        }
    },
    "mmmcView": {
        "typical": {
            "delayCorner": "typical",
            "constraint": "func"
        }
    }
}

def getOpcond(p: str, v: str, t: str):
    pstr = p
    vstr = 'v' + v.replace('.', 'p')
    tstr = 't' + t.replace('-', 'n')+'c'
    return pstr + vstr + tstr

class PdConfig(object):
    def __init__(self) -> None:
        super().__init__()
        self.config = template
        self.timingManager = MultipleTimingLibManager()
        # complete all five rc corners
        for corner in ["cbest", "rcbest", "cworst", "rcworst"]:
            self.config["rcCorner"][corner] = template["rcCorner"]["typical"].copy()

    def addIp(self, *ips: tuple[str, str]):
        for ip in ips:
            self.timingManager.addSearchPath(ip[0], ip[1])

    def addConsMode(self, *sdcs: tuple[str, str]):
        if len(sdcs) != 0:
            template = self.config['constraint'].pop('func')
        for sdc in sdcs:
            mode = sdc[0]
            sdcPath = sdc[1]
            self.config['constraint'][mode] = template.copy()
            self.config['constraint'][mode]['sdcFile']['preCTS'] = sdcPath

    def buildLibarySets(self):
        """
        The first step of build delay corners. This function is to group the 
        timing libraries by pvt corners. 
        """
        # ps = self.timingManager
        self.config['library'].pop("*")
        for manager in self.timingManager.subLibsManager:
            ps = list(set((manager.getPVT("process"))))
            vs = list(set(manager.getPVT("voltage")))
            ts = list(set(manager.getPVT("temperature")))
            for p in ps:
                for v in vs:
                    for t in ts:
                        opcond = getOpcond(p, v, t)
                        libs = manager.indexByPVT(p, v, t)
                        libPaths = list(
                            map(lambda lib: lib.libPath, libs)
                        )
                        if len(libs) != 0:
                            if opcond in self.config['library']:
                                self.config['library'][opcond] += libPaths
                            else:
                                self.config['library'][opcond] = libPaths
        return self

    def buildDelayCorner(self):
        """
        This function aims to build all the possible delay corners, 
        respective to the various library sets and the rc corners.
        Thus, firstly, the function list all the pvt corner, in which 
        resides all the ip's libraries belong to the corner. 
        Secondly, the function iterate all the corner with each rc corner, 
        to build delay corners. 
        """
        template = self.config['delayCorner'].pop('typical')
        self.buildLibarySets()
        for rc in self.config["rcCorner"]:
            for opc in self.config['library']:
                cornerName = opc + '_' + rc
                self.config['delayCorner'][cornerName] = template.copy()
                self.config['delayCorner'][cornerName]['rcCorner'] = rc
                self.config['delayCorner'][cornerName]['library'] = opc
        return self

    def buildMmmcView(self):
        """
        This function is to build the mmmc analysis view for mmmc timing analysis.
        An view consists of a constraint mode and a delay corner. 
        You need to provide your own sdc file path. 
        """
        template = self.config['mmmcView'].pop('typical')
        self.buildDelayCorner()
        for cons in self.config['constraint']:
            for corner in self.config['delayCorner']:
                view = cons + "_" + corner
                self.config['mmmcView'][view] = template
                self.config['mmmcView'][view]['constraint'] = cons
                self.config['mmmcView'][view]['delayCorner'] = corner
        return self

    def writeJson(self, jsonPath: str):
        content = json.dumps(self.config, indent=4, separators=(',', ':'))
        with open(jsonPath, 'w') as jsonf:
            jsonf.write(content)


if __name__ == "__main__":
    config = PdConfig()
    config.addIp(
        ("stdcell", "D:\\lzp\\tmp\\umc\\55ulpuhvt\\fsf0u_juu\\2017Q3v1.0")
    )
    config.buildMmmcView()
    config.writeJson("test.json")
