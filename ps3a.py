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
    
assert countSubStringMatch('aaa', 'b') == 0
assert countSubStringMatch('aaa', 'aa') == 2
assert countSubStringMatch('abba', 'ba') == 1
assert countSubStringMatch('abbaabba', 'ba') == 2
assert countSubStringMatch('abababab', 'aba') == 3

assert countSubStringMatchRecursive('aaa', 'b') == 0
assert countSubStringMatchRecursive('aaa', 'aa') == 2
assert countSubStringMatchRecursive('abba', 'ba') == 1
assert countSubStringMatchRecursive('abbaabba', 'ba') == 2
assert countSubStringMatchRecursive('abababab', 'aba') == 3