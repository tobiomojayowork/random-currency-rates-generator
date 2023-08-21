
import datetime, random, os

# FILE AND DIRECTORY PATHS
#----------------------------------------------------------------
DATAFOLDER = "DATA"
OUTPUTFOLDER = os.path.join(DATAFOLDER, "OUTPUT")

RATEGROUPFILE = "rate_groups.txt"
CURRENCYFILE = "my_currencies.txt"

#RATETYPEFILEPATH = "rate_types.txt"
RATEGROUPFILEPATH = os.path.join(DATAFOLDER, RATEGROUPFILE)
CURRENCYFILEPATH = os.path.join(DATAFOLDER, CURRENCYFILE)

OUTPUTCLIENRATESTFILEPATH = os.path.join(OUTPUTFOLDER, "random_client_rates.csv")
OUTPUTCONSTANTRATESFILEPATH = os.path.join(OUTPUTFOLDER, "random_const_rates.csv")


# [USER INSTRUCTIONS #1]
def PrintInstructions():
    print(
            f" * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
            f" \n\n\tWELCOME TO THE RANDOM CURRENCY RATE GENERATOR"
            f"\n\n * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
            f"\n\nThis app is used to generate random exchange rates for unit and load testing purposes in a target KIP Currency Application"
            f"\n\n * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
            f"\nBefore you run the app, you would need to: "
            f"\n\t1. Review the file containing a list of the rate groups, called {RATEGROUPFILE}. Add and update entries as required."
            f"\n\n\t2. Review the file containing a list of 3-letter ISO currency codes (e.g. GBP, USD, etc), called {CURRENCYFILE}. Add and update entries as required."
            f"\n\n\n Entries in each of the files must i) be on a separate line, ii) have no trailing or leading spaces or spaces (the rate group entries can have spaces within them but not at the beginning or end)"
            f"\n\n * * The data generated is purely mock random data and has no bearing on any existing entity, engagement or the company. * * "
            f"\n\n The entries in each file must be valid for use in the target Currency App, in that they must exist in that Application's database. " 
            f"\n\nFor the rate groups, the first entry must be the (default) group for the KPMG constant rates as configured in the target Currency App"
            f"\n\nThe created files will be saved to the {OUTPUTFOLDER} directory."
            f"\n\n\n\t3. Indicate how many exchange rates you wish to generate. This can be any figure. "
            f"Bear in mind larger numbers may impact performance, which is not guaranteed."
            f"\n\n\nCreate the files as instructed and then answer the next question."
            f"\n\n\n * * * * * * * * * * * * * * * * * * * * * * * * * * * *"
        )
    if input(f"\n\tHave you created a rate group and currency file as instructed?"
             f"\n\tEnter Y to continue: ").upper() == "Y":
        return True
    else:
        print("\n\nThe program will exit now. When you're ready you can run the generator again.\n\n")
        return False 
    

def PrintEndText():
    print(
        f"Your rates have been generated. you can find them in the {OUTPUTFOLDER} directory.\n\n"
        f"Import the generated rates from the csv files into the import rates template in the Currency App."
        f"\n\n\nThe program has ended.\n\n"
        )

# Rate groups [USER CHECK/PROMPT #1]
#----------------------------------------------------------------
def LoadRateGroups():
    global rate_groups
    
    rate_groups = []

    if os.path.exists(RATEGROUPFILEPATH):

        f = open(RATEGROUPFILEPATH)

        for group in f:
            rate_groups.append(group.rstrip("\n"))

        f.close()

        rate_groups = tuple(rate_groups)

        #print(rate_groups)
    if len(rate_groups) == 0:
        print(f"The {RATEGROUPFILE} file was not created OR the file had no groups in it. Aborting random rates generation.")
        return False

    return True

# CURRENCIES  [USER CHECK/PROMPT #2]
#----------------------------------------------------------------

def LoadCurrencies():
    global currencies

    currencies = []

    if os.path.exists(CURRENCYFILEPATH):
        f = open(CURRENCYFILEPATH)

        for curr in f:
            currencies.append(curr.rstrip("\n"))

        f.close()

        #print(currencies)
    if len(currencies) == 0 :
        print(f"The {CURRENCYFILE} file was not created OR the file had no currency codes in it. Aborting random rates generation.")
        return False

    return True

# NUMBER OF CURRENCIES TO GENERATE [USER CHECK/PROMPT #3]
# how many exchange rates do you want to create? enter a number
#----------------------------------------------------------------
def GetTotalCountToCreate():
    _rate_count = -1

    try: 
        _rate_count = int(input("\n\nEnter the number of rates to generate (this MUST be > 5): "))
    except:
        print(f"Incorrect entry specified! Aborting random rates generation.\n\n")
        return _rate_count

    if(_rate_count > 5):
        return _rate_count 
    else:
        print(f"No number was specified. Aborting random rates generation.\n\n")
        return _rate_count
    


# Random Date generation
#Set Year Month Date parameters for random dates generation
#----------------------------------------------------------------
def SetRandomDateConfig():
    global cfg   

    year = datetime.datetime.now().year
    startMonth = datetime.datetime.now().month
    startDay = datetime.datetime.now().day    

    randomOption = random.randint(0, 400)

    if randomOption > 300: year = random.randint(2017, datetime.datetime.now().year)
    if randomOption > 200: startMonth = random.randint(1, 12)
    if randomOption > 100: startDay = GetRandomDay(startMonth, year)
    maxDayInterval = randomOption

    cfg = { 
        "globalStartDate" : datetime.date(year, startMonth, startDay), 
        "globalMaxDayInterval": maxDayInterval
    }

def GetRandomDay(month, year):
    if month in [9, 4, 6, 11]:
        return random.randint(1, 30)
    elif month == 2 and year % 4 == 0:
        return random.randint(1, 29)
    elif month == 2:
        return random.randint(1, 28)
    else:
        return random.randint(1, 31)
    

def CreateStartDate():
    #random date
    randomDayInterval = random.randint(0, cfg["globalMaxDayInterval"])
    return cfg["globalStartDate"] + datetime.timedelta(days=randomDayInterval)

def CreateDateRange():
    #random date range
    date_start = CreateStartDate()
    return [ 
        date_start,
        date_start + datetime.timedelta(days=random.randint(0, cfg["globalMaxDayInterval"]))
    ]


# Output List 
#----------------------------------------------------------------
outputRates = {
    "constant": [],
    "client": []
}


# Rate types list (fixed)
#----------------------------------------------------------------
rate_types = ("Constant", "Day", "BalanceSheet", "ProfitAndLoss")


def GetRateGroup(avoidDefault=None):
    # ensure all rates data and settings specified here matches what is in the database
    rate_group = random.choice(rate_groups)

    # the KPMG Default rate group is restricted to the Constant rate
    # for simplicity and ease of exclusion, ensure this group is the first element
    if avoidDefault:
        while rate_group == rate_groups[0]:
            rate_group = random.choice(rate_groups) 

    return rate_group


# RANDOM Currency Rate creators
#----------------------------------------------------------------
def GetCurrencyPair():
    currFrom = random.choice(currencies)
    currTo = random.choice(currencies) 
    # could make the rates plausible based on the currency pair
    # for now, make it completely random rates
    rate = float("{:.4f}".format(random.random() * random.randint(1, 100)))

    while currFrom == currTo:
        currTo = random.choice(currencies) 
    
    return [currFrom, currTo, rate]



def CreateRate(rateFields):
    currFrom, currTo, dateStart, dateEnd, rateType, rate, rateGroup = rateFields

    return {
        "CurrFrom": currFrom,
        "CurrTo": currTo,
        "StartDate": dateStart,
        "EndDate": dateEnd,
        "RateType": rateType,
        "Rate": rate,
        "RateGroup": rateGroup
    }    

def CreateDayRate(currFrom, currTo, rate):
    # MUST have the same start and end date
    date_start = CreateStartDate()

    return CreateRate([
        currFrom,
        currTo,
        date_start,
        date_start,
        random.choice([rate_types[1], rate_types[2]]),
        rate,
        GetRateGroup(True)
    ])
    


def CreateProfitAndLossRate(currFrom, currTo, rate):
    date_start, date_end = CreateDateRange()

    # only add rate pair if it does not already exist - at least in our output
    # because of contiguous date error

    return CreateRate([
        currFrom,
        currTo,
        date_start,
        date_end,
        rate_types[3],
        rate,
        GetRateGroup(True)
    ])

def CreateConstantRate(currFrom, currTo, rate):
    # date NOT REQUIRED for constant rates
    # must output on separate sheet

    # only add rate pair if it does not already exist - at least in our output

    return CreateRate([
        currFrom,
        currTo,
        None,
        None,
        rate_types[0],
        rate,
        GetRateGroup()
    ])

# Validators
#----------------------------------------------------------------
def RatePairExists(sourceKey, rateToFind):
    # sure there is a more efficient way to do this but it'll have to do for now....
    for rate in outputRates[sourceKey]:
        if rateToFind["CurrFrom"]==rate["CurrFrom"] and rateToFind["CurrTo"]==rate["CurrTo"] and rateToFind["RateType"]==rate["RateType"]:
            return True
    
    return False

# MAIN PROGRAM BODY: 
# 1 GENERATE Random Currency Rates 
#----------------------------------------------------------------
def GenerateRandomRates(_rate_count):
    while _rate_count != 0:
        currFrom, currTo, rate = GetCurrencyPair()

        actionIndex = random.randint(1,4)

        newrate = None

        if actionIndex == 2: 
            newrate = CreateProfitAndLossRate(currFrom, currTo, rate)

            if not RatePairExists("client", newrate):
                outputRates["client"].append(newrate)
            else: 
                print(f'rate {newrate["CurrFrom"]} - {newrate["CurrTo"]} ({newrate["RateType"]}) already exists, will not be added')
                actionIndex = 3

        if actionIndex == 3: 
            newrate = CreateConstantRate(currFrom, currTo, rate)

            if not RatePairExists("constant", newrate):
                outputRates["constant"].append(newrate)
            else: 
                print(f'rate {newrate["CurrFrom"]} - {newrate["CurrTo"]} ({newrate["RateType"]}) already exists, will not be added')
                actionIndex = 1

        if actionIndex == 1: 
            newrate = CreateDayRate(currFrom, currTo, rate)
            outputRates["client"].append(newrate)

        if actionIndex == 4: SetRandomDateConfig()

        if actionIndex != 4: _rate_count-=1






# 2 OUTPUT FILES:
#----------------------------------------------------------------
def OutputRatesFiles():
    fclient = open(OUTPUTCLIENRATESTFILEPATH, "w" )

    fclient.write("CurrFrom,CurrTo,StartDate,EndDate,RateType,Rate,RateGroup")
    for rate in outputRates["client"]:
        fclient.write(f'\n{rate["CurrFrom"]},{rate["CurrTo"]},{rate["StartDate"]},{rate["EndDate"]},{rate["RateType"]},{float(rate["Rate"])},{rate["RateGroup"]}')

    fclient.close()

    fconst = open(OUTPUTCONSTANTRATESFILEPATH, "w")
    fconst.write("CurrFrom,CurrTo,RateType,Rate,RateGroup")
    for rate in outputRates["constant"]:
        fconst.write(f'\n{rate["CurrFrom"]},{rate["CurrTo"]},{rate["RateType"]},{float(rate["Rate"])},{rate["RateGroup"]}')

    fconst.close()


# PROGRAM START 
#----------------------------------------------------------------
#----------------------------------------------------------------

if PrintInstructions() and LoadCurrencies() and LoadRateGroups():
    rateCount = GetTotalCountToCreate()

    if(rateCount>0):
        SetRandomDateConfig()

        GenerateRandomRates(rateCount) 

        OutputRatesFiles()

        PrintEndText()

# PROGRAM END  
#----------------------------------------------------------------
#----------------------------------------------------------------