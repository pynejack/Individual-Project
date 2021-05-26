import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

    ## Lotus
    
def data():
    fluid_df = pd.read_csv('fort.9', delim_whitespace = True, 
                           names=["time","CFL","fx1","fy1","m1","p1","fx2","fy2","m2","p2"])
    fluid_df.drop(['CFL', 'fy1', 'm1'],axis=1, inplace=True)

    fluid_df['thrust1'] = -(fluid_df.fx1)
    fluid_df['thrust2'] = -(fluid_df.fx2)

    ## prepares the data for the groups (rounds time column to have the cycle)
    fluid_df['cycle'] = np.floor(fluid_df['time'])

    ## Gets rid of the start and end cycles ##
    fluid_df = fluid_df[fluid_df.cycle != 0]
    fluid_df = fluid_df[fluid_df.cycle != 1]
    fluid_df = fluid_df[fluid_df.cycle != 2]
    fluid_df = fluid_df[fluid_df.cycle != 3]
    fluid_df = fluid_df[fluid_df.cycle != 10]

    ## here you make groups ##
    grouped = fluid_df.groupby('cycle')
    
## Thrust coefficient    
    
    thrust_averaged1=grouped['thrust1'].mean()
    mean_thrust1 = np.mean(thrust_averaged1)
    thrust_averaged1.plot(label='fore')        

    thrust_averaged2=grouped['thrust2'].mean()
    mean_thrust2 = np.mean(thrust_averaged2)
    thrust_averaged2.plot(label='hind')
    
    plt.legend()
    plt.ylabel("$C_T$", rotation=0)
    plt.xlabel('cycle')
    plt.show()
    plt.close()
    
## Plot averaged thrust and total
    ax = plt.gca()
    
    fluid_df.plot(x='time', y='thrust1', label='fore', ax=ax)
    fluid_df.plot(x='time', y='thrust2', label='hind', ax=ax)
    thrust_averaged1.plot(label='fore')  
    thrust_averaged2.plot(label='hind')
    
    plt.xlim([10, 13])
    plt.legend()
    plt.ylabel("$C_T$", rotation=0)
    plt.xlabel('cycle')
    plt.show()
    plt.close()
    
## Power

    power_averaged1=(grouped['p1'].mean())
    mean_power1 = np.mean(power_averaged1)
    power_averaged1.plot(label='fore')    
    
    power_averaged2=(grouped['p2'].mean())
    mean_power2 = np.mean(power_averaged2)
    power_averaged2.plot(label='hind')
    
    plt.legend()
    plt.ylabel("P", rotation=0)
    plt.xlabel('cycle')
    plt.show()
    plt.close()
    
## Efficiency

    efficiency_averaged1=thrust_averaged1/power_averaged1
    mean_eff1 = np.mean(efficiency_averaged1)
    efficiency_averaged1.plot(label='fore')

    efficiency_averaged2=thrust_averaged2/power_averaged2
    mean_eff2 = np.mean(efficiency_averaged2)
    efficiency_averaged2.plot(label='hind')   

    plt.legend()
    plt.ylabel("$\eta$", rotation=0)
    plt.xlabel('cycle')
    plt.show()
    plt.close()
    
    
    print('Mean fore thrust coeff:', mean_thrust1)
    print('Mean hind thrust coeff:', mean_thrust2)
    
    print('Mean fore power:', mean_power1)
    print('Mean hind power:', mean_power2)
    
    print('Mean fore eff:', mean_eff1)
    print('Mean hind eff:', mean_eff2)


    return()
