import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

    ## St = 0.4 , Re = 10**4 , spacing = 2c , phase= 1.75*pi
    
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
    fluid_df = fluid_df[fluid_df.cycle != 20]

    ## here you make groups ##
    grouped = fluid_df.groupby('cycle')
    
## Thrust coefficient    
    
    thrust_averaged1=grouped['thrust1'].mean()
    mean_thrust1 = round(np.mean(thrust_averaged1),3)
#    thrust_averaged1.plot(label='fore')        

    thrust_averaged2=grouped['thrust2'].mean()
    mean_thrust2 = round(np.mean(thrust_averaged2),3)
    
## Plot averaged thrust and total
    plt.figure(figsize=[4,4], dpi=1000)

    ax = plt.gca()
    
    fluid_df.plot(x='time', y='thrust1', label='fore', ax=ax, color='red', linewidth='0.75')
    fluid_df.plot(x='time', y='thrust2', label='hind', ax=ax, color='darkturquoise', linewidth='0.75')
    thrust_averaged1.plot(linestyle='dashed', label='fore', color='red', linewidth='0.75')  
    thrust_averaged2.plot(linestyle='dashed', label='hind', color='darkturquoise', linewidth='0.75')
    
    plt.xlim([10, 11])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.ylabel("$C_T$", rotation=0, labelpad=10)
    plt.xlabel('cycle')
    plt.show()
    plt.close()
    
## Power

    power_averaged1=(grouped['p1'].mean())
    mean_power1 = round(np.mean(power_averaged1),3)
    power_averaged1.plot(label='fore')    
    
    power_averaged2=(grouped['p2'].mean())
    mean_power2 = round(np.mean(power_averaged2),3)
    power_averaged2.plot(label='hind')
    
## Plot averaged power and total
    plt.figure(figsize=[4,4], dpi=1000)

    ax = plt.gca()
    
    fluid_df.plot(x='time', y='p1', label='fore', ax=ax, color='red', linewidth='0.75')
    fluid_df.plot(x='time', y='p2', label='hind', ax=ax, color='darkturquoise', linewidth='0.75')
    power_averaged1.plot(linestyle='dashed', label='fore', color='red', linewidth='0.75')  
    power_averaged2.plot(linestyle='dashed', label='hind', color='darkturquoise', linewidth='0.75')
    
    plt.xlim([10, 11])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.ylabel("$C_P$", rotation=0, labelpad=10)
    plt.xlabel('cycle')
    plt.show()
    plt.close()
    
## Efficiency

    efficiency_averaged1=thrust_averaged1/power_averaged1
    mean_eff1 = round(np.mean(efficiency_averaged1),3)
    efficiency_averaged1.plot(label='fore')

    efficiency_averaged2=thrust_averaged2/power_averaged2
    mean_eff2 = round(np.mean(efficiency_averaged2),3)
    efficiency_averaged2.plot(label='hind')   

    plt.legend()
    plt.ylabel("$\eta$", rotation=0)
    plt.xlabel('cycle')
    plt.show(loc='bbox')
    plt.close()
    
    
    print('Lily pad 20 cycles, St=0.4:')

    print('Mean fore thrust coeff:', mean_thrust1)
    print('Mean hind thrust coeff:', mean_thrust2)
    
    print('Mean fore power:', mean_power1)
    print('Mean hind power:', mean_power2)
    
    print('Mean fore eff:', mean_eff1)
    print('Mean hind eff:', mean_eff2)

    print()
    print()    

    frontT = 0.523619678901779
    backT = 1.02476340828307
    Tratio = 1.95707581203284
    frontE = 0.504246975061259
    totalE = 0.530901512468026
    
    thrust1_dif = (mean_thrust1 - frontT) / frontT
    thrust2_dif = (mean_thrust2 - backT) / backT
    thrust_ratio_dif = ((mean_thrust2/mean_thrust1) - Tratio) / Tratio
    eff1_dif = (mean_eff1 - frontE) / frontE
    efficiency_total_dif = (((mean_eff2 + mean_eff1)/2) - totalE) / totalE
    
#    print('Lily pad 20 cycles, St=0.4:')
    
    print('Thrust fore % dif:', thrust1_dif * 100)
    print('Thrust hind % dif:', thrust2_dif * 100)
    print('Thrust ratio % dif:', thrust_ratio_dif * 100)
    print('Efficiency fore % dif:', eff1_dif * 100)
    print('Total efficiency % dif:', efficiency_total_dif * 100)

    
    return()
