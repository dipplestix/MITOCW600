def subStringMatchExact(target, key):
    results = ()
    index = target.find(key)
    while index > -1:
        results += (index,)
        index = target.find(key, index+1)
    return results