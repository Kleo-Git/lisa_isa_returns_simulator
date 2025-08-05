import numpy as np
import matplotlib.pyplot as plt


def LISA(num_years, interest_rate, yearly_investment, gov_return = 1.25):
    total_money = 0
    total_money_per_year = []
    for i in range(num_years):
        total_invested_year = yearly_investment * gov_return
        total_money = (total_money + total_invested_year) * interest_rate
        total_money_per_year.append(total_money)
    return total_money_per_year

def ISA(num_years, interest_rate, yearly_investment):
    total_money = 0
    total_money_per_year = []
    for i in range(num_years):
        total_money = (total_money + yearly_investment) * interest_rate
        total_money_per_year.append(total_money)
    return total_money_per_year

def ratio_split(ratio, total_money_to_invest, lisa_cap):
    lisa_money = ratio*total_money_to_invest
    isa_money = (1-ratio) * total_money_to_invest
    if lisa_money > lisa_cap:
        print(f"Money in LISA too high, moved excess {lisa_money - lisa_cap} into ISA")
        isa_money += lisa_money - lisa_cap
        lisa_money = lisa_cap
    return lisa_money, isa_money

def results_over_years(num_years, interest_rate, total_money_to_invest, ratio_lisa_isa, lisa_cap = 4000, emigration_prob = 0.5):
    results = []
    corrected_results = []
    for i in range(len(ratio_lisa_isa)):
        money_split = ratio_split(ratio_lisa_isa[i], total_money_to_invest, lisa_cap)
        
        lisa_money = money_split[0]
        isa_money = money_split[1]
        
        money_lisa = LISA(num_years, interest_rate, lisa_money)
        money_isa = ISA(num_years, interest_rate, isa_money)
        
        corrected_money_lisa = []
        for i in range(len(money_lisa)):
            penalty = penalty_function(money_lisa[i])
            corrected_value = money_lisa[i] * (1 - emigration_prob * penalty)
            corrected_money_lisa.append(corrected_value)
        
        total_per_year = [l + i for l, i in zip(money_lisa, money_isa)]
        corrected_total_per_year = [l + i for l, i in zip(corrected_money_lisa, money_isa)]
        results.append(total_per_year)
        corrected_results.append(corrected_total_per_year)
    return(results, corrected_results)

def plot_total_money_vs_ratio(results, ratio_lisa_isa, num_years, corrected_results=0):
    x=[];y=[]
    results = results[corrected_results]
    for i in range(len(results)):
        x.append(ratio_lisa_isa[i])
        y.append(results[i][-1])
    plt.plot(x,y)
    plt.title(f"Total money after {num_years} years based on ratio split")
    plt.xlabel("Ratio of money split")
    plt.ylabel("Total Amount of Money (£)")
    plt.savefig("images/total_money_vs_ratio_split.png")
    plt.show()

def find_best_ratio(results, ratio_lisa_isa, corrected_results=0, print_reuslt=0):
    x=[];y=[]
    results = results[corrected_results]
    for i in range(len(results)):
        x.append(ratio_lisa_isa[i])
        y.append(results[i][-1])
    best_value_index = np.argmax(y)
    best_value = y[best_value_index]
    best_ratio = x[best_value_index]
    if print_reuslt:
        print("Best Ratio = ", best_ratio)
        print("Highest corrected money = ", best_value)
    return(best_ratio)
    
def plot_money_over_years(results, ratio_lisa_isa, num_years, corrected_results=0):
    results = results[corrected_results]
    for i in range(len(ratio_lisa_isa)):
        x=[];y=[]
        for t in range(num_years):
            x.append(t+1)
            y.append(results[i][t])
        plt.plot(x,y, label = f"Ratio LISA to ISA: {ratio_lisa_isa[i]:.2f}")
    plt.legend()
    plt.xlabel("Number years")
    plt.ylabel("Total Amount of Money (£)")
    plt.title("Money per year")
    plt.savefig("images/money_over_years.png")
    plt.show()

def penalty_function(x, central_point=20000, max_value=0.5, scale=2000):
    shifted_x = (-x+central_point)/scale
    sigmoid = 1 / (1 + np.e**(shifted_x))
    output = max_value * sigmoid
    return (output)
    
#Assume total of 10k a year
#Start with a 5 year period

num_years = 5
interest_rate = 1.1
total_money_to_invest = 10000
lisa_cap = 4000
ratio_lisa_isa = np.arange(0,0.41,0.1)

results = results_over_years(num_years, interest_rate, total_money_to_invest, ratio_lisa_isa, lisa_cap)
plot_money_over_years(results, ratio_lisa_isa, num_years)
plot_total_money_vs_ratio(results, ratio_lisa_isa, num_years)

ratio_lisa_isa = np.arange(0,0.4001,0.001)
emigration_probs = np.arange(0,1.01,0.01)
best_ratios = []
for i in range(len(emigration_probs)):
    results = results_over_years(num_years, interest_rate, total_money_to_invest, ratio_lisa_isa, lisa_cap, emigration_probs[i])
    best_ratios.append(find_best_ratio(results, ratio_lisa_isa, 1, 0))


plt.title("Best ratio vs emigration chance")
plt.xlabel("Emigration Chance")
plt.ylabel("Best ratio")
plt.plot(emigration_probs, best_ratios)
plt.savefig("images/ideal_ratio_vs_emigration_chance.png")
plt.show()


