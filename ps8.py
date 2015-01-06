# 6.00 Problem Set 8
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

import time


SUBJECT_FILENAME = "subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    inputFile = open(filename)
    subjects = {}
    for line in inputFile:
        linel = line.split(",")
        linel[2] = linel[2].strip()
        
        subjects[linel[0]] = [int(linel[1]), int(linel[2])]
    return subjects

    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = list(subjects.keys())
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print(res)

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    return  val1 > val2

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return  work1 < work2

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return float(val1) / work1 > float(val2) / work2

#
# Problem 2: Subject Selection By Greedy Optimization
#
def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    sortedList = mergeSort(subjects, comparator)
    totwork = 0
    classes = {}
    for i in sortedList:
        if totwork + subjects[i][WORK] < maxWork:
            totwork += subjects[i][WORK]
            classes[i] = subjects[i]
    return classes

    
def mergeSort(subjects, comparator):
    unsortedList = list(subjects.keys())
    sortedl = breakUp(unsortedList, comparator, subjects)
    return sortedl

def breakUp(unsortedList, comparator, subjects):
    if len(unsortedList) == 1:
        return unsortedList
    else:
        middle = len(unsortedList)//2
        left = breakUp(unsortedList[:middle], comparator, subjects)
        right = breakUp(unsortedList[middle:], comparator, subjects)
        sortedl = merge(left, right, comparator, subjects)
    return sortedl
    
    
    
def merge(l, r, comparator, subjects):
    i = 0
    j = 0
    merged = []
    while i < len(l) and j < len(r):
        if comparator(subjects[l[i]], subjects[r[j]]):
            merged.append(l[i])
            i += 1
        else:
            merged.append(r[j])
            j += 1
    if i < len(l):
        for k in range(i, len(l)):
            merged.append(l[k])
    else:
        for k in range(j, len(r)):
            merged.append(r[k])
    return merged
        
    
    
        

def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    nameList = list(subjects.keys())
    tupleList = list(subjects.values())
    bestSubset, bestSubsetValue = \
            bruteForceAdvisorHelper(tupleList, maxWork, 0, None, None, [], 0, 0)
    outputSubjects = {}
    for i in bestSubset:
        outputSubjects[nameList[i]] = tupleList[i]
    return outputSubjects

def bruteForceAdvisorHelper(subjects, maxWork, i, bestSubset, bestSubsetValue,
                            subset, subsetValue, subsetWork):
    # Hit the end of the list.
    if i >= len(subjects):
        if bestSubset == None or subsetValue > bestSubsetValue:
            # Found a new best.
            return subset[:], subsetValue
        else:
            # Keep the current best.
            return bestSubset, bestSubsetValue
    else:
        s = subjects[i]
        # Try including subjects[i] in the current working subset.
        if subsetWork + s[WORK] <= maxWork:
            subset.append(i)
            bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                    maxWork, i+1, bestSubset, bestSubsetValue, subset,
                    subsetValue + s[VALUE], subsetWork + s[WORK])
            subset.pop()
        bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                maxWork, i+1, bestSubset, bestSubsetValue, subset,
                subsetValue, subsetWork)
        return bestSubset, bestSubsetValue

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceTime(subjects):
    """
    Runs tests on bruteForceAdvisor and measures the time required to compute
    an answer.
    """
    maxWork = [2, 4, 6, 7, 8, 9, 10]
    times = {}
    for work in maxWork:
        startTime = time.time()
        bruteForceAdvisor(subjects, work)
        endTime = time.time()
        times[work] = round(endTime - startTime, 3)
        print(times)
    return times

# Problem 3 Observations
# ======================
#
# TODO: write here your observations regarding bruteForceTime's performance

#
# Problem 4: Subject Selection By Dynamic Programming
#
def dpAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work) that contains a
    set of subjects that provides the maximum value without exceeding maxWork.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    m = {}
    answer = {}
    
    w = []
    v = []
    keys = []
    for classes in subjects:
        w.append(subjects[classes][WORK])
        v.append(subjects[classes][VALUE])
        keys.append(classes)
    
    value, courses = decisionTree(w, v, len(w)-1, maxWork, m)
    
    for classes in courses:
        answer[keys[classes]] = [v[classes], w[classes]]
    return answer
    
def decisionTree(w, v, i, aW, m):
    try: 
        return m[(i, aW)]
    except KeyError:
        if i == 0:
            if w[i] <= aW:
                m[(i, aW)] = v[i], [i]
                return v[i], [i]
            else:
                m[(i, aW)] = 0, []
                return 0, []
        without_i, courseList = decisionTree(w, v, i-1, aW, m)
        if w[i] > aW:
            m[(i, aW)] = without_i, courseList
            return without_i, courseList
        else: 
            with_i, courseListL = decisionTree(w, v, i-1, aW-w[i], m)
            with_i += v[i]
        if with_i > without_i:
            ival = with_i
            courseList = [i] + courseListL
        else: 
            ival = without_i
        m[(i, aW)] = ival, courseList
        return ival, courseList
        
        

#
# Problem 5: Performance Comparison
#
def dpTime():
    """
    Runs tests on dpAdvisor and measures the time required to compute an
    answer.
    """
    maxWork = [2, 4, 6, 7, 8, 9, 10, 30, 500]
    times = {}
    for work in maxWork:
        startTime = time.time()
        dpAdvisor(subjects, work)
        endTime = time.time()
        times[work] = round(endTime - startTime, 3)
    return times

# Problem 5 Observations
# ======================
#
# TODO: write here your observations regarding dpAdvisor's performance and
# how its performance compares to that of bruteForceAdvisor.