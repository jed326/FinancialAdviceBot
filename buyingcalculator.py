def prompting():
    print("Are you buying a house, a car, or a different product?")
    typ = input()
    if typ == 'house':
        house()
    elif typ == 'car':
        car()
    else:
        simple()
    
def simple():
    print("What is the total cost of your purchase?")
    totalcost = input()
    totalcost.replace(',','')
    if totalcost.isdigit() == True:
        print("The purchase will cost: " + totalcost)
        totalcost = int(totalcost)
    else:
        print("Please input a valid price")
        prompting()
    print("How much do you have saved so far for the purchase?")
    saved = input()
    saved.replace(',','')
    if saved.isdigit() == True:
        print("Remaining cost of your purchase = ", totalcost - int(saved))
        left = totalcost - int(saved)
    else:
        print("Please input a valid savings")
        prompting()
    print("Would you like to know how much you need to save up every week or how long it will take you up?\n\nType 1 for the first and 2 for the second")
    option = input()
    if option == '1':
        print("In how many weeks would you like to make the purchase?")
        weeks = int(input())
        print("Save $", left//weeks, "every week to buy in time!")
    elif option == '2':
        print("How much are you willing to save for the purchase each week?")
        money = int(input())
        print("At this rate, it will take", left//money + 1, "weeks to make your purchase!")
    else:
        print("Please enter choose a valid option")
        prompting()

        
def car():
    print ("What is the total price of the car?")
    total = int(input())
    print ("What is the down payment on the car?")
    down = int(input())
    print ("What is the APR on the car in percent?")
    APR = (input())
    APR.replace('%','')
    APR = int(APR)
    print ("Over how many months will you pay for the car?")
    months = int(input())
    print("What is the MPG on the car?")
    MPG = int(input())
    print("What is the insurance premium on the car per year?")
    insur = int(input())
    print("What is your annual income?")
    income = int(input())

    monthlygasinsur = (12000//MPG*2.3 + insur)/12
    print(monthlygasinsur)
    monthlyfinancing = (APR/1200*(total-down))/(1-(1+APR/1200)**(months*-1))
    print(monthlyfinancing)
    totalmonthly = monthlygasinsur + monthlyfinancing
    print(totalmonthly*12)
    print("Assuming that you can make the down payment, the cost of the car per year will be $", totalmonthly*12)
    percent = (totalmonthly*12)/income*100
    print("\nThis car will take up",percent,"% of your yearly income")
    if(percent < 10):
        return("This car seems to be in your price range! With some careful planning you should be all set to purchase it.")
    elif(10 <= percent <= 15):
        return("This car could be in your price range, but some more consideration should be given towards other costs that could prevent you from financing your car.")
    else:
        return("You are probably not ready to purchase this car. Please consider other financial options or other vehicles that will fall into your price range")
    

    
           
def house():
    
    
print(prompting())
