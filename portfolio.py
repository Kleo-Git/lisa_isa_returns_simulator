import numpy as np
import matplotlib.pyplot as plt
from accounts import LISA, ISA

class Portfolio:
    """
    Represents an investment portfolio split between a LISA and an ISA account.
    
    Attributes:
        yearly_investment (float): Total annual investment.
        interest_rate (float): Annual interest rate multiplier.
        lisa_ratio (float): Proportion of investment allocated to LISA.
        lisa_cap (float): Maximum yearly contribution allowed to LISA (default: 4000).
    """
    
    def __init__(self, yearly_investment, interest_rate, lisa_ratio, lisa_cap = 4000):
        """
        Initialize the portfolio with investment details and allocation ratio.

        Parameters:
            yearly_investment(float): Total amount invested annually.
            interest_rate(float): Annual interest rate multiplier.
            lisa_ratio(float): Proportion (0 to 1) of investement directed into LISA.
            lisa_cap(float, optional): Annual LISA contribution cap. Default is 4000.

        """
        
        self.yearly_investment = yearly_investment
        self.interest_rate = interest_rate
        self.lisa_ratio = lisa_ratio
        self.lisa_cap = lisa_cap
        self.accounts = []
        
    def allocate_funds(self, show_warning_message = False):
        """
        Allocate yearly investment between LISA and ISA, bounded by LISA cap.

        Parameters:
            show_warning_message(bool): Whether to print a warning if LISA cap is exceeded.
            
        Returns:
            tuple: (lisa_allocation, isa_allocation) after applying cap adjustments.

        """
        lisa_cap = self.lisa_cap
        lisa_allocation = self.yearly_investment * self.lisa_ratio
        isa_allocation = self.yearly_investment * (1 - self.lisa_ratio)
        
        #Enforce LISA cap and transfer excess to ISA
        if lisa_allocation > lisa_cap:
            excess_lisa_allocation = lisa_allocation - lisa_cap
            lisa_allocation = lisa_cap
            isa_allocation += excess_lisa_allocation
            
            if (show_warning_message == True):
                print(f"LISA contribution in excess of £{lisa_cap} limit by £{excess_lisa_allocation}, " \
                      "moving excess to ISA ")
                    
        return(lisa_allocation, isa_allocation)
    
    def run_simulation(self, num_years, emigration_prob = 0.1, apply_penalty = True):
        """
        Simulate investment growth over a number of years, applying emigration penalities if enabled.

        Parameters:
            num_years(int): Number of years to simulate.
            emigration_prob(float): Probability of emigrating in a given year (Used for penalty calculation).
            apply_penalty(bool): Whether to apply the LISA penalty for emigration.
            
        Returns:
            list of float: Total portfolio value at the end of each year.
        """
        #Calculate the ISA/LISA contributions based on investment and ratio
        yearly_lisa_contribution, yearly_isa_contribution = self.allocate_funds()
        
        #Create LISA and ISA account objects
        lisa_account = LISA(yearly_lisa_contribution, self.interest_rate)
        isa_account = ISA(yearly_isa_contribution, self.interest_rate)
        
        #Run compound interest simulations
        lisa_amount_list = lisa_account.compound_interest(num_years)
        isa_amount_list = isa_account.compound_interest(num_years)
        
        #Optionally apply LISA penalties due to emigration
        if apply_penalty:
            lisa_amount_list = lisa_account.apply_emigration_penalty(lisa_amount_list, emigration_prob)
        
        #Store yearly portfolio value (LISA + ISA)
        self.total_money_list = [l + i for l, i in zip(lisa_amount_list, isa_amount_list)]
        
        return(self.total_money_list)

def optimal_ratio(yearly_investment, interest_rate, num_years, lisa_ratios, emigration_prob, print_result=False):
    """
    Find the optimal LISA/ISA allocation ratio for maximum final portfolio value

    Parameters:
        yearly_investment(float): Total amount invested annually.
        interest_rate(float): Annual interest rate multiplier. 
        num_years(int): Number of years to simulate 
        lisa_ratios(list of float): List of LISA allocation ratios to test.
        emigration_prob(float): Probability of emigrating.
        print_result(bool): Whether to print the best result.

    Returns:
        float: The optimal LISA allocation ratio.
    """
    results = []
    
    for i in range(len(lisa_ratios)):
        portfolio = Portfolio(yearly_investment, interest_rate, lisa_ratios[i])
        results.append(portfolio.run_simulation(num_years, emigration_prob)[-1])
        
    best_value_index = np.argmax(results)
    best_value = results[best_value_index]
    best_ratio = lisa_ratios[best_value_index]
    
    if print_result:
        print("Highest total =", best_value)
        print("Best ratio =", best_ratio)
    
    return(best_ratio)
    
def optimize_portfolio(yearly_investment, interest_rate, num_years, lisa_ratios, emigration_probs):
    """
    Find the optimal LISA allocation ratios across different emigration probabilities.

    Parameters:
        yearly_investment(float): Total amount invested annually.
        interest_rate(float): Annual interest rate multiplier. 
        num_years(int): Number of years to simulate 
        lisa_ratios(list of float): List of LISA allocation ratios to test.
        emigration_probs(list of float): List of emigration probabilities to test.

    Returns:
        list of float: Best LISA ratios corresponding to emigration probability.
    """
    best_ratios = []
    for prob in emigration_probs:
        best_ratio = optimal_ratio(
            yearly_investment, 
            interest_rate, 
            num_years, 
            lisa_ratios, 
            emigration_prob = prob)
        best_ratios.append(best_ratio)
    return(best_ratios)



lisa_ratios = np.arange(0,0.401,0.01)
emigration_probs = np.arange(0,1.01,0.01)

y = optimize_portfolio(10000, 1.1, 5, lisa_ratios, emigration_probs)

plt.plot(emigration_probs, y)
plt.show()