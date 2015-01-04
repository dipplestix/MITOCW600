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