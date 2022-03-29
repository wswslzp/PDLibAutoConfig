import os
import gzip
import re

def toStr(line):
    if type(line) is bytes:
        return line.decode()
    else:
        return str(line)

class PhysicLib(object):
    def __init__(self) -> None:
        super().__init__()
        self.libPath = ""
        self.libName = ""

    def isTechLef(self):
        ret = True
        with open(self.libPath, "r") as lef:
            for line in lef:
                if "MACRO" in line:
                    ret = False 
                    break
        return ret

    def getAllLayers(self):
        layer_p = re.compile(r"LAYER (\w+)\s*TYPE\sROUTING ;")
        with open(self.libPath, "r") as lef:
            content = lef.read()
            layers = layer_p.findall(content)
            return layers

class TimingLib(object):
    def __init__(self) -> None:
        super().__init__()
        self.libPath = ""
        self.libName = ""
        self.cornerName = ""
        self.corner = {
            "process": "",
            "voltage": 0,
            "temperature": 9999
        }

    def getProcessFromName(self, name: str):
        name = name.lower()
        if "ff" in name:
            self.corner["process"] = "ff"
        elif "tt" in name:
            self.corner["process"] = "tt"
        elif "ss" in name:
            self.corner["process"] = "ss"

    def scanForName(self, content):
        ret = False
        for line in content:
            line = toStr(line)
            pat = re.compile(r"\s*library\s*\(\s*(\w+)\s*\)\s*\{")
            if pat.match(line):
                self.libName = pat.findall(line)[0]
                self.getProcessFromName(self.libName)
                ret = True
                break
        return ret
    
    def scanForPVT(self, content):
        p_pat = re.compile(r"\s*operating_conditions\s*\(\s*(\w+)\s*\)")
        nt_pat = re.compile(r"\s*nom_temperature\s*:\s*(-?[1-9]\d*|0)\s*;")
        nv_pat = re.compile(r"\s*nom_voltage\s*:\s*([1-9]\d*\.\d*|0\.\d*[1-9]\d*)\s*;")
        matched = 0
        for line in content:
            line = toStr(line)
            if p_pat.match(line):
                self.cornerName = p_pat.findall(line)[0]
                if self.corner["process"] == "":
                    self.getProcessFromName(self.cornerName)
                matched += 1
            if nt_pat.match(line):
                self.corner["temperature"] = nt_pat.findall(line)[0]
                matched += 1
            if nv_pat.match(line):
                self.corner["voltage"] = nv_pat.findall(line)[0]
                matched += 1
            if matched == 3:
                break

    def check(self):
        if self.corner["process"] == "":
            assert False, "Process isn't catched. "
        elif self.corner["voltage"] == 0:
            assert False, "Voltage isn't catched."
        elif self.corner["temperature"] == 9999:
            assert False, "temperature isn't catched."

    def scanContent(self, content):
        if self.scanForName(content):
            self.scanForPVT(content)
            self.check()
        return self

def scanPhysicLib(libPath: str):
    ret = PhysicLib()
    if libPath.endswith(".lef") or libPath.endswith(".plef"):
        ret.libPath = libPath
        ret.libName = os.path.basename(libPath).split(".")[0]
    return ret

def scanTimingLib(libPath: str):
    ret = TimingLib()
    ret.libPath = libPath
    if libPath.endswith(".lib"):
        with open(libPath, "r") as libf:
            ret = ret.scanContent(libf)
    elif libPath.endswith(".lib.gz"):
        with gzip.open(libPath, "r") as libf:
            ret = ret.scanContent(libf)
    else :
        return None
    return ret

def searchForPhysicLib(path: str):
    ret = []
    for p, d, f in os.walk(path):
        for lib in f:
            if lib.endswith(".lef") or lib.endswith(".plef"):
                physicLib = scanPhysicLib(os.path.join(p, lib))
                ret.append(physicLib)
    return ret

def searchForTimingLib(path: str):
    ret = []
    for p, d, f in os.walk(path):
        for lib in f:
            if lib.endswith(".lib") or lib.endswith(".lib.gz"):
                print("scanning {path}".format(path=os.path.join(p,lib)))
                timingLib = scanTimingLib(os.path.join(p, lib))
                if timingLib.libName != "":
                    ret.append(timingLib)
    return ret

if __name__ == "__main__":
    # libs = searchForTimingLib("testLib/lib")
    # lefs = searchForPhysicLib("/mnt/d/lzp/tmp/umc/55ulpuhvt/fsf0u_juu/2017Q3v1.0")
    lefs = searchForPhysicLib("D:/lzp/tmp/umc/55ulpuhvt/fsf0u_juu/2017Q3v1.0")
    techlefs = list(filter(lambda lef: lef.isTechLef(), lefs))
    print(techlefs[0].getAllLayers())
    print("")