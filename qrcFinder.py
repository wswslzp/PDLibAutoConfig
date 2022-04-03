import os 

def findQrcTechFile(path: str):
    ret = {
        'typical': '',
        'cbest': '',
        'cworst': '',
        'rcbest': '',
        'rcworst': ''
    }
    for p,_,fs in os.walk(path):
        for f in fs:
            f_abspath = os.path.join(p, f)
            for rc in ret:
                if rc in f_abspath:
                    ret[rc] = f_abspath
    return ret
