#!/usr/bin/python3
import prettytable as ppt
from functools import reduce

import libScanner

class PhysicLibManager(object):
    def __init__(self) -> None:
        super().__init__()
        self.techLef: libScanner.PhysicLib = None
        self.macroLef: list[libScanner.PhysicLib] = []

    def searchForLibs(self, libPath):
        # def getLayerNum(techlef: libScanner.PhysicLib):
        #     return len(techlef.getAllLayers())
        lefs = libScanner.searchForPhysicLib(libPath)
        techlefs = list(filter(lambda lef: lef.isTechLef(), lefs))
        if len(techlefs) != 0:
            self.techLef = techlefs[0] ## TODO: randomly choose
        self.macroLef += list(filter(lambda lef: not lef.isTechLef(), lefs))
        # layers = map(getLayerNum, techlefs)
        

class TimingLibManager(object):
    def __init__(self, IPName) -> None:
        super().__init__()
        self.IPName = IPName
        self.timingLibs: list[libScanner.TimingLib] = []
        
    def searchForLibs(self, libPath):
        self.timingLibs = libScanner.searchForTimingLib(libPath)

    def getPVT(self, pvt: str):
        return [lib.corner[pvt] for lib in self.timingLibs]

    def getSubManager(self, pvt: str, pvt_v): 
        ret = TimingLibManager(self.IPName)
        for lib in self.timingLibs:
            if lib.corner[pvt] == pvt_v:
                ret.timingLibs.append(lib)
        return ret

    def indexByPVT(self, p, v, t):
        ret = []
        for lib in self.timingLibs:
            if p == lib.corner["process"] and v == lib.corner["voltage"] and t == lib.corner["temperature"]:
                ret.append(lib)
        return ret

    def getFastest(self):
        maxVoltage = max(map(lambda x: int(x), self.getPVT("voltage")))
        for lib in self.timingLibs:
            if lib.corner["process"] == "ff":
                ...

    def printCornerTable(self):
        def getLibName(lib: libScanner.TimingLib):
            if lib != None:
                return lib.cornerName
            else:
                return "None"
        ps = list(set(self.getPVT("process")))
        for p in ps:
            p_libsManager = self.getSubManager("process", p)
            vs = list(set(p_libsManager.getPVT("voltage")))
            ts = list(set(p_libsManager.getPVT("temperature")))
            tsWithUnit = list(map(lambda s: s+" C", ts))
            table = ppt.PrettyTable([p] + tsWithUnit)
            for v in vs:
                pv_libsManager = p_libsManager.getSubManager("voltage", v)
                row = [v+" V"]
                for t in ts:
                    libs = pv_libsManager.indexByPVT(p, v, t)
                    libs = map(getLibName, libs)
                    libs = list(libs)
                    if len(libs) > 1:
                        libsContent = reduce(lambda a,b: a+"/"+b, list(libs))
                    elif len(libs) == 1:
                        libsContent = libs[0]
                    else:
                        libsContent = "None"
                    row.append(libsContent)
                table.add_row(row)
            print(table)


class MultipleTimingLibManager(object):
    def __init__(self) -> None:
        super().__init__()
        self.subLibsManager: list[TimingLibManager] = []

    def addSearchPath(self, ip: str, ipLibPath: str):
        manager = TimingLibManager(ip)
        manager.searchForLibs(ipLibPath)
        self.subLibsManager.append(manager)
        

if __name__ == "__main__":
    # libm = TimingLibManager("eco")
    libm = PhysicLibManager()
    # libm.searchForLibs("D:\\lzp\\tmp\\umc\\55ulpuhvt\\fsf0u_juu\\2017Q3v1.0\\ECO_M1_CORE\\FrontEnd\\synopsys\\synthesis")
    # libm.searchForLibs("D:\\lzp\\tmp\\umc\\55ulpuhvt\\fsf0u_juu\\2017Q3v1.0\\GENERIC_CORE")
    libm.searchForLibs("D:\\lzp\\tmp\\umc\\55ulpuhvt\\fsf0u_juu\\2017Q3v1.0")
    # libm.searchForLibs("/mnt/d/lzp/tmp/umc/55ulpuhvt/fsf0u_juu/2017Q3v1.0")
    # libm.printCornerTable()
    print("")
