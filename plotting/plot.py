import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df=pd.read_csv('reward.csv', names=['speed reduction factor','reward'])

plt.plot(df['speed reduction factor'], df['reward'],color='blue', marker='o', markersize=5, markerfacecolor='red')

plt.xlim(-0.1, 1.5)
plt.ylim(-105, 10)

plt.axhline(0, color='black', linestyle='-', linewidth=0.5) 
plt.axvline(0, color='black', linestyle='-', linewidth=0.5) 

plt.title('SRF vs Reward')
plt.xlabel('Speed Reduction Factor')
plt.ylabel('Reward')

plt.savefig("image2.png", format="png", dpi=600)
plt.show()
