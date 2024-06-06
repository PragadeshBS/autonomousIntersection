import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('plotting/data/vehicles_vs_second.csv')

average_vehicle_count = data['vehicles'].mean()

plt.plot(data['second'], data['vehicles'], color='blue', marker='o', markersize=5, markerfacecolor='blue')

plt.xlim(0, 65)
plt.ylim(0, 40)

plt.title('No. of Vehicles at Intersection Zone')
plt.axhline(y=average_vehicle_count, color='red', linestyle='--', label='Average Vehicle Count')
plt.legend(loc='upper right')

plt.xlabel('Time (seconds)')
plt.ylabel('No. of Vehicles')

plt.show()