import numpy as np
import matplotlib.pyplot as plt
from portfolio import Portfolio, optimal_ratio, optimize_portfolio


class Visual_Analysis(Portfolio):
    """
    Extends Portfolio to provide visual analysis tools for investment simulations
    across varying LISA allocation ratios and emigration probabilities.

    Attributes:
        lisa_ratios (list of float): List of proportions allocated to LISA.
        emigration_probs (list of float): List of emigration probabilities.
    """
    
    def __init__(self, yearly_investment, interest_rate, lisa_ratios, emigration_probs, lisa_cap = 4000):
        """
        Initialize Visual_Analysis with investment details and analysis parameters.
        
        Parameters:
            yearly_investment(float): Total amount invested annually.
            interest_rate(float): Annual interest rate multiplier.
            lisa_ratios(list of float): List of LISA allocation ratios to test.
            emigration_probs(list of float): List of emigration probabilities to test.
            lisa_cap(float, options): Annual LISA contribution cap. Default is 4000.
        
        """
        # Initialize base Portfolio class
        super().__init__(yearly_investment, interest_rate, lisa_ratios) 
        self.lisa_ratios = lisa_ratios
        self.emigration_probs = emigration_probs
        
    def limit_values(self, values_list, num_values = 1):
        """
        Select a limited number of representative values from a list.

        If num_values == 1, returns the median value.
        If num_values > 1, returns evenly spaced values across the list.
        Returns an empty list if num_values exceeds list length.

        Parameters:
            values_list (list): List of values to sample from.
            num_values (int, optional): Number of values to return. Default is 1.

        Returns:
            list or single value: Selected values or a single median value.
        """
        if num_values > len(values_list):
            return[]
        if num_values == 1:
            # Return median value
            return(values_list[int(0.5*len(values_list))])
        else:
            # Generate evenly spaced indices and return corresponding values
            indices = np.linspace(0,len(values_list) - 1, num_values)
            indices = np.round(indices).astype(int)
            return[values_list[i] for i in indices]
    
    def plot_yearly_investments(self, num_years, save_fig = False, num_lines_to_plot=5):
        """
        Plot investment growth over a number of years for different LISA allocation ratios.

        Parameters:
            num_years (int): Number of years to simulate.
            save_fig (bool, optional): Whether to save the plot as an image. Default is False.
            num_lines_to_plot (int, optional): Number of allocation ratios to plot. Default is 5.
        """
        years = range(1, num_years+1)
        em_prob = self.limit_values(self.emigration_probs, 1) # Get median emigration probability
        
        plt.figure(figsize=(10, 6))
        
        # Choose evenly spaced indices from lisa_ratios to plot
        total_ratios = len(self.lisa_ratios)
        if total_ratios <= num_lines_to_plot:
            indices_to_plot = range(total_ratios)
        else:
            indices_to_plot = np.linspace(0, total_ratios - 1, num_lines_to_plot, dtype=int)
        
        # Plot portfolio growth for each selected LISA ratio
        for i in indices_to_plot:
            ratio = self.lisa_ratios[i]
            port = Portfolio(self.yearly_investment, self.interest_rate, ratio)
            money_list = port.run_simulation(num_years, em_prob)
            plt.plot(years, money_list, label = f"Ratio LISA to ISA: {self.lisa_ratios[i]:.2f}")
        
        plt.title(f"Total money over years given {em_prob*100:.1f}% emigration chance")
        plt.xlabel("Number of Years")
        plt.ylabel("Total Money (£)")
        plt.grid(True)
        plt.legend()
        
        if save_fig:
            save_string = "images/money_over_years.png"
            print("Saving image to " + save_string)
            plt.savefig(save_string)
            
        plt.show()
        
    def plot_total_money_vs_ratio(self, num_years, save_fig = False):
        """
        Plot final total money after a set number of years as a function of LISA allocation ratio.

        Parameters:
            num_years (int): Number of years to simulate.
            save_fig (bool, optional): Whether to save the plot as an image. Default is False.
        """
        results = []
        em_prob = self.limit_values(self.emigration_probs, 1) # Median emigration probability
        
        # Run simulation for each LISA ratio and record final total money
        for ratio in self.lisa_ratios:
            port = Portfolio(self.yearly_investment, self.interest_rate, ratio)
            money_list = port.run_simulation(num_years, em_prob)
            results.append(money_list[-1])
            
        plt.figure(figsize=(10, 6))
        plt.plot(self.lisa_ratios, results)
        
        plt.title(f"Total money after {num_years} years based on ratio split")
        plt.legend([f"Emigration probabilty = {em_prob}"])
        plt.xlabel("Ratio of money split")
        plt.ylabel("Total Money (£)")
        plt.grid(True)
        
        if save_fig:
            save_string = "images/total_money_vs_ratio_split.png"
            print("Saving image to " + save_string)
            plt.savefig(save_string)
        
        plt.show()
        
    def plot_ratio_vs_emigration_prob(self, num_years, save_fig = False):
        """
        Plot the optimal LISA allocation ratio as a function of emigration probability.
    
        Uses the `optimize_portfolio` function to find the best ratio for each emigration chance.
    
        Parameters:
            num_years (int): Number of years for simulation.
            save_fig (bool, optional): Whether to save the plot as an image. Default is False.
        """
        # Get list of best ratios optimized over emigration probabilities
        list1 = optimize_portfolio(self.yearly_investment, self.interest_rate, num_years, self.lisa_ratios, self.emigration_probs)
        plt.figure(figsize=(10, 6))
        plt.plot(self.emigration_probs, list1)
        
        plt.title("Best ratio vs emigration chance")
        plt.xlabel("Emigration Chance")
        plt.ylabel("Best ratio")
        plt.grid(True)
        
        if save_fig:
            save_string = "images/ideal_ratio_vs_emigration_chance.png"
            print("Saving image to " + save_string)
            plt.savefig(save_string)
        
        plt.show()
    
    def plot_tmvr_blocks(self, num_years, num_ratios_per_block, num_em_probs_to_plot, save_fig=False):
        """
        Plot total money over time for blocks of LISA ratios across selected emigration probabilities.
    
        Each emigration probability block is color-coded, plotting multiple LISA ratios.
    
        Parameters:
            num_years (int): Number of years to simulate.
            num_ratios_per_block (int): Number of LISA ratios to plot per block.
            num_em_probs_to_plot (int): Number of emigration probabilities to plot.
            save_fig (bool, optional): Whether to save the plot as an image. Default is False.
        """
        years = range(1, num_years+1)
        em_probs_to_plot = self.limit_values(self.emigration_probs, num_em_probs_to_plot)
        ratios_to_plot = self.limit_values(self.lisa_ratios, num_ratios_per_block)
        
        # Get distinct colors for each emigration probability block
        color_map = plt.get_cmap("viridis", len(em_probs_to_plot))
        
        plt.figure(figsize=(10, 6))
        
        # Plot lines for each combination of emigration probability and LISA ratio
        for i, em_prob in enumerate(em_probs_to_plot):
            color = color_map(i)
            for j, ratio in enumerate(ratios_to_plot):
                port = Portfolio(self.yearly_investment, self.interest_rate, ratio)
                money_list = port.run_simulation(num_years, em_prob)
    
                # Label only the first line per emigration block to keep legend clean
                label = f"Emigration: {em_prob * 100:.0f}%" if j == 0 else None
                plt.plot(years, money_list, color=color, label=label, linewidth=1)
    
        plt.title("Total Money Over Time for Different LISA Ratios vs an Emigration Probabilities")
        plt.xlabel("Years")
        plt.ylabel("Total Money (£)")
        plt.legend(title="Emigration Probability")
        plt.grid(True)
    
        if save_fig:
            save_string = "images/lisa_blocks_by_emigration_prob.png"
            print(f"Saving plot to {save_string}")
            plt.savefig(save_string)
    
        plt.show()
        
    def plot_average_tvmr_blocks(self, num_years, num_ratios_per_block, num_em_probs_to_plot, show_optimal_path=True, save_fig=False):
        """
        Plot average total money over time for blocks of LISA ratios aggregated by emigration probabilities.
    
        Calculates average portfolio value across selected LISA ratios for each emigration probability.
    
        Parameters:
            num_years (int): Number of years to simulate.
            num_ratios_per_block (int): Number of LISA ratios to include in averaging.
            num_em_probs_to_plot (int): Number of emigration probabilities to plot.
            show_optimal_path (bool, optional): Unused parameter, retained for interface consistency.
            save_fig (bool, optional): Whether to save the plot as an image. Default is False.
        """
        years = range(1, num_years+1)
        em_probs_to_plot = self.limit_values(self.emigration_probs, num_em_probs_to_plot)
        ratios_to_plot = self.limit_values(self.lisa_ratios, num_ratios_per_block)
        
        color_map = plt.get_cmap("viridis", len(em_probs_to_plot))
        
        plt.figure(figsize=(10, 6))
        
        # Compute and plot average portfolio values for each emigration probability
        for i, em_prob in enumerate(em_probs_to_plot):
            color = color_map(i)
            temp_list=[]
            for ratio in ratios_to_plot:
                port = Portfolio(self.yearly_investment, self.interest_rate, ratio)
                money_list = port.run_simulation(num_years, em_prob)
                temp_list.append(money_list)
            
            # Average portfolio values year-by-year
            avg_money = []
            for year_idx in range(num_years):
                year_sum = sum(temp_list[r][year_idx] for r in range(len(temp_list)))
                avg_money.append(year_sum / len(temp_list))
            
            plt.plot(years, avg_money, label=f"Emigration Prob = {em_prob:.2f}", color=color)
            
        plt.title("Total Money Over Time for Averaged LISA ratios vs Emigration Probabilities")
        plt.xlabel("Years")
        plt.ylabel("Total Money (£)")
        plt.legend(title="Emigration Probability")
        plt.grid(True)
    
        if save_fig:
            save_string = "images/average_tvmr_blocks.png"
            print(f"Saving plot to {save_string}")
            plt.savefig(save_string)
    
        plt.show()

    def plot_heatmap(self, num_years, save_fig=False, show_optimal_path=True):
        """
        Generate a heatmap displaying final portfolio values across all LISA ratios and emigration probabilities.
    
        Optionally overlays the optimal LISA ratio path maximizing portfolio value per emigration probability.
    
        Parameters:
            num_years (int): Number of years to simulate.
            save_fig (bool, optional): Whether to save the heatmap as an image. Default is False.
            show_optimal_path (bool, optional): Whether to overlay the optimal ratio path. Default is True.
    
        Returns:
            np.ndarray: Matrix of final portfolio values with shape (num_ratios, num_em_probs).
        """
        print(f"Computing heatmap: {len(self.lisa_ratios)} ratios × {len(self.emigration_probs)} emigration probabilities...")
        
        # Initialize matrix to hold final portfolio values for each ratio/probability combination
        results_matrix = np.zeros((len(self.lisa_ratios), len(self.emigration_probs)))
        
        # Populate matrix with final portfolio values
        for i, ratio in enumerate(self.lisa_ratios):
            for j, emigration_prob in enumerate(self.emigration_probs):
                port = Portfolio(self.yearly_investment, self.interest_rate, ratio)
                final_value = port.run_simulation(num_years, emigration_prob)[-1]
                results_matrix[i, j] = final_value
            
            # Progress update every 10 ratios or on first iteration
            if (i + 1) % 10 == 0 or i == 0:
                print(f"Completed {i + 1}/{len(self.lisa_ratios)} ratios...")
        
        plt.figure(figsize=(10, 6))
        
        # Plot heatmap using imshow with appropriate axis scaling
        im = plt.imshow(results_matrix, 
                       cmap='viridis',
                       aspect='auto', 
                       origin='lower',
                       extent=[self.emigration_probs[0], self.emigration_probs[-1], 
                              self.lisa_ratios[0], self.lisa_ratios[-1]])
        
        # Add colorbar with label
        cbar = plt.colorbar(im)
        cbar.set_label('Final Portfolio Value (£)', rotation=270, labelpad=20)
        
        plt.xlabel('Emigration Probability')
        plt.ylabel('LISA Allocation Ratio')
        plt.title(f'Portfolio Value Heatmap: {num_years} Years, £{self.yearly_investment:,}/year')
        
        # Overlay optimal LISA ratio path (optional)
        if show_optimal_path:
            optimal_ratios = []
            for j, emigration_prob in enumerate(self.emigration_probs):
                best_ratio_idx = np.argmax(results_matrix[:, j])
                optimal_ratios.append(self.lisa_ratios[best_ratio_idx])
            
            plt.plot(self.emigration_probs, optimal_ratios, 'r-', linewidth=2, 
                    label='Optimal Ratio Path', alpha=0.8)
            plt.legend()
        
        # Add grid for readability
        plt.grid(True, alpha=0.5)
        plt.tight_layout()
        
        if save_fig:
            save_string = "images/portfolio_heatmap.png"
            print(f"Saving heatmap to {save_string}")
            plt.savefig(save_string, dpi=300, bbox_inches='tight')
        
        plt.show()
        
        return results_matrix

