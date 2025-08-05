import numpy as np

def penalty_function(x, central_point=20000, max_value=0.5, scale=2000):
    """
    Calculate 'penalty' value, using a sigmoid function.
    
    Parameters:
        x (float): The current balance/value to evaluate.
        central_point(float, optional): The centre of sigmoid function, defaults to 20,000.
        max_value(float, optional): The maximum penalty value, defaults to 0.5.
        scale(float, optional): Controls steepness of sigmoid curve, defaults to 2000.
        
    Returns:
        float: The calculated penalty between 0 and max_value.
    """
    
    #Shift the x position so the 'steep' part centres are central point
    #Divide by scale to avoid runtime warning since using very large numbers generally (>1e4)
    shifted_x = (-x+central_point)/scale
    
    #Apply the sigmoid function around the shifted x
    sigmoid = 1 / (1 + np.e**(shifted_x))
    
    #Further scale output based on maximal penalty function
    #In base case, the middle penalty function 0.25, which matches the
    #25% withdrawal charge for early withdrawal.
    output = max_value * sigmoid
    
    return output

class Account:
    """
    Base class for a savings account.
    Attributes:
        yearly_contribution(float): Amount contributed annually.
        interest_rate(float): Annual interest rate multiplier (e.g. 1.1 for 10%)
    """
    
    def __init__(self, yearly_contribution, interest_rate):
        """ 
        Initialize account with yearly contribution and interest rate
        
        Parameters:
            yearly_contribution(float) : Amount contributed annually.
            interest_rate(float) : Annual interest rate multiplier (e.g. 1.1 for 10%)
        """
        
        self.yearly_contribution = yearly_contribution
        self.interest_rate = interest_rate
        
    def compound_interest(self, num_years):
        """ 
        Calculate account balance over specified number of years with compound interest.
        
        Parameters:
            num_years (int): Number of years to simulate.
            
        Returns:
            list of float: Account balance at end of each year.
        """
        
        self.num_years = num_years
        
        total_money = 0 #Initial account balance
        total_money_per_year = [] #Used to store balance year by year
        
        for i in range(num_years):
            #Apply yearly contribution, and calculate interest
            total_money = (total_money + self.yearly_contribution) * self.interest_rate
            total_money_per_year.append(total_money)
        
        return(total_money_per_year)
    
class ISA(Account):
    """
    Individual Savings Account (ISA) with standard behavior.
    """
    
    def __init__(self, yearly_contribution, interest_rate):
        """ 
        Initialize ISA.
        
        Parameters:
            yearly_contribution(float): Amount contributed annually.
            interest_rate(float): Annual interest rate multiplier
        """
        super().__init__(yearly_contribution, interest_rate) 

    def compound_interest(self, num_years):
        """
        Use the parent class's compound_interest method directly.
        
        Parameters:
            num_years (int): Number of years to simulate.
        
        Returns:
            list of float: Account balance at end of each year.
        """
        return super().compound_interest(num_years)
            
class LISA(Account):
    """
    Lifetime ISA (LISA) account with government bonus applied to contribution
    """
    
    def __init__(self, yearly_contribution, interest_rate):
        """ 
        Initialize LISA account with adjusted contribution including government bonus
        
        Parameters:
            yearly_contribution(float): Amount contributed annually.
            interest_rate(float): Annual interest rate multiplier
        """
        #The adjusted contribution is 25% of deposited amount each year
        #Max contribution is 4000, so bonus is capped at 1000
        adjusted_contribution = yearly_contribution + min(1000, 0.25*yearly_contribution)
        
        super().__init__(adjusted_contribution, interest_rate) 
        
    def compound_interest(self, num_years):
        """
        Use the parent class's compound_interest method directly.
        
        Parameters:
            num_years (int): Number of years to simulate.
        
        Returns:
            list of float: Account balance at end of each year.
        """
        return super().compound_interest(num_years)
    
    def apply_emigration_penalty(self, money_list, emigration_prob):
        """
        Adjust emigration-based penalty to yearly balances.
        
        Parameters:
            money_list(list of float): Account balances per year.
            emigration_prob(float): Probability (0-1) of emigration, scaling penalty impact.
            
        Returns:
            list of float: Adjusted balances based on penalty.
        """
        corrected_money = [] #List to store balances after penalty adjustment
        
        for money in money_list:
            #Calculate the penalty rate based on current balance for sigmoid function
            penalty = penalty_function(money)
            
            #Further scale the penalty based on emigration probabilty
            corrected_value = money * (1 - emigration_prob * penalty)
            
            corrected_money.append(corrected_value)
            
        return corrected_money
