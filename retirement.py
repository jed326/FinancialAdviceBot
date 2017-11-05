import math

#inputs are:
#current age
#age that you'd like to retire at
#current annual income
#what percent of your annual income you will invest
#current savings
def calculate(age, retireAge, income, percentPerYear, currentSavings):
    years = retireAge - age

    #interest + contributions formula adapted from a tab that's not open anymore
    #assumes 6.6% return adjusted for inflation
    inflation = 0.066
    moneyAtRetirement = int(currentSavings * math.pow(1 + inflation, years) + \
        ((percentPerYear / 100) * income * (math.pow(1 + inflation, years) - 1)) / inflation)

    #while loop because I'm too lazy to figure out another formula
    tempMoney = moneyAtRetirement
    
    countYears = 0
    while tempMoney > 0 and countYears < 100:
        tempMoney = tempMoney - (0.9 * income)
        tempMoney = tempMoney * (1.066)
        countYears += 1

    #returns how much money the person will have at their chosen retirement age
    #also returns how long that money will last them (assumes living on 80% of their current income during retirement)
    return(moneyAtRetirement, retireAge + countYears)
