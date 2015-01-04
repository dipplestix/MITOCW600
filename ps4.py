def nestEggFixed(salary, save, growthRate, years):
    amount = [salary*save/100]
    year = 1
    while year < years:
        loopAmount = amount[year - 1]*(1+growthRate/100) + salary*save/100
        amount.append(loopAmount)
        year += 1
    return amount
    
def nestEggVariable(salary, save, growthRates):
    amount = []
    year = 1
    for rate in growthRates:
        if len(amount) == 0:
            amount.append(salary*save/100)
        else:
            loopAmount = amount[-1]*(1+rate/100) + salary*save/100
            amount.append(loopAmount)
    return amount
    
def postRetirement(savings, growthRates, expenses):
    balance = []
    for rate in growthRates:
        if len(balance) == 0:
            balance.append(savings*(1+rate/100) - expenses)
        else:
            newbalance = balance[-1]*(1+rate/100) - expenses
            balance.append(newbalance)
    return balance
    
def findMaxExpenses(salary, save, preRetireGrowthRates, postRetireGrowthRates,
                    epsilon):
    savings = nestEggVariable(salary, save, preRetireGrowthRates)[-1]
    low = 0
    high = savings
    guess = (low + high)/2
    balance = postRetirement(savings, postRetireGrowthRates, guess)
    while abs(balance[-1]) > epsilon:
            if balance[-1] > 0:
                low = guess
            else:
                high = guess
            guess = (low + high)/2
            balance = postRetirement(savings, postRetireGrowthRates, guess)
    return guess

def testFindMaxExpenses():
    salary                = 10000
    save                  = 10
    preRetireGrowthRates  = [3, 4, 5, 0, 3]
    postRetireGrowthRates = [10, 5, 0, 5, 1]
    epsilon               = .01
    expenses = findMaxExpenses(salary, save, preRetireGrowthRates,
                               postRetireGrowthRates, epsilon)
    print(expenses)
    # Output should have a value close to:
    # 1229.95548986
