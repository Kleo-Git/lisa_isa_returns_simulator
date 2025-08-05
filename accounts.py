import numpy as np

def penalty_function(x, central_point=20000, max_value=0.5, scale=2000):
    shifted_x = (-x+central_point)/scale
    sigmoid = 1 / (1 + np.e**(shifted_x))
    output = max_value * sigmoid
    return output

class Account:
    
    def __init__(self, yearly_contribution, interest_rate):
        
        """ Initialize account with yearly contribution and annual interest rate"""
        
        self.yearly_contribution = yearly_contribution
        self.interest_rate = interest_rate
        
    def compound_interest(self, num_years):
        
        """ Calculate compounding growth of the account balance over given number of years """
        
        self.num_years = num_years
        
        total_money = 0 #Initial account balance
        total_money_per_year = [] #Used to store balance year by year
        
        for i in range(num_years):
            #Apply yearly contribution, and calculate interest
            total_money = (total_money + self.yearly_contribution) * self.interest_rate
            total_money_per_year.append(total_money)
        
        return(total_money_per_year)
    
class ISA(Account):
    
    """Standard ISA account using base account constructor"""
    
    def __init__(self, yearly_contribution, interest_rate):
        super().__init__(yearly_contribution, interest_rate) 

    def compound_interest(self, num_years):
        """Use the parent class's compound_interest method directly."""
        return super().compound_interest(num_years)
            
class LISA(Account):
    
    """Lifetime ISA account with annual government bonus (25% up to £1000)."""
    
    def __init__(self, yearly_contribution, interest_rate):
        """Adjust the total based on governement bonus."""
        adjusted_contribution = yearly_contribution + min(1000, 0.25*yearly_contribution)
        super().__init__(adjusted_contribution, interest_rate) 
        
    def compound_interest(self, num_years):
        """Use the parent class's compound_interest method directly."""
        return super().compound_interest(num_years)
    
    def apply_emigration_penalty(self, money_list, emigration_prob):
        """Adjust yearly balances by applying emigration based probability"""
        
        corrected_money = [] #List to store balances after penalty adjusment
        
        for money in money_list:
            #Calculate the penalty rate based on current balance for sigmoid function
            penalty = penalty_function(money)
            
            #Further scale the penalty based on emigration probabilty
            corrected_value = money * (1 - emigration_prob * penalty)
            
            corrected_money.append(corrected_value)
            
        return corrected_money
