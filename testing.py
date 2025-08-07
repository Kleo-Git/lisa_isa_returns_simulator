import numpy as np
import matplotlib.pyplot as plt
from data_analysis import Visual_Analysis
from accounts import penalty_function

lisa_ratios1 = np.arange(0,0.401,0.001)
emigration_probs1 = np.arange(0,1.01,0.01)

object1 = Visual_Analysis(10000, 1.1, lisa_ratios1, emigration_probs1)

#object1.plot_yearly_investments(5)

#object1.plot_total_money_vs_ratio(5)

object1.plot_ratio_vs_emigration_prob(5)

#object1.plot_tmvr_blocks(5,10,11)

#object1.plot_average_tvmr_blocks(5,10,11)

object1.plot_heatmap(5)

x=[];y=[]
for i in np.arange(-20,20,0.01):
    x.append(i)
    y.append(penalty_function(i, 0, 0.5, 2))
    
plt.xlabel("x")
plt.ylabel("y")
plt.title("Penalty function centered at 0")
plt.plot(x,y)
plt.grid(True)
plt.savefig("images/penalty_functin_centred_at_0")
#plt.show()