

def deepCopyList(inp):
    for vl in inp:
        if isinstance(vl, list):
            yield list(deepCopyList(vl))
        elif isinstance(vl, dict):
            yield deepCopyDict(vl)

def deepCopyDict(inp):
    outp = inp.copy()
    for ky, vl in outp.iteritems():
        if isinstance(vl, dict):
            outp[ky] = deepCopyDict(vl)
        elif isinstance(vl, list):
            outp[ky] = list(deepCopyList(vl))
    return outp

def simpleDeepCopy(inp):
    if isinstance(inp, dict):
        return deepCopyDict(inp)
    elif isinstance(inp, list):
        return deepCopyList(inp)
    else:
        return inp

if __name__ == '__main__':
    import time
    from copy import deepcopy
    start = time.time()
    sample = [2,3,4]
    for _ in range(1000000):
        tmp = simpleDeepCopy(sample)
    end = time.time()
    print('simpleDeepCopy: ' + str(end - start))
    start = time.time()
    for _ in range(1000000):
        tmp = deepcopy(sample)
    end = time.time()
    print ('copy.deepcopy: ' + str(end - start))