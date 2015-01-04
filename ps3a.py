def countSubStringMatch(string, target):
    index = string.find(target)
    result = 0
    while index >= 0:
        result += 1
        index = string.find(target, index+1)
    return result

def countSubStringMatchRecursive(string, target, i=0):
    index = string.find(target, i)
    if index >= 0:
        return 1 + countSubStringMatchRecursive(string[index+1:], target)
    else:
        return 0