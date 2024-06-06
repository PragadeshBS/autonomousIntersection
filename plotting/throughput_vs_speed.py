import matplotlib.pyplot as plt

plt.plot([0,8.304349334,24.83503987, 44.91156555, 48.57064392, 66.40320391, 83.05810674], [0,129.4731163,388.852884, 694.8465547,
762.2685789,930.927835,
961.785228],color='blue', marker='o', markersize=5, markerfacecolor='blue')

plt.plot([40, 39.9, 27], [0, 100, 600] ,color='yellow', marker='o', markersize=5, markerfacecolor='yellow')

plt.xlim(-5, 100)
plt.ylim(-8, 1750)

# plt.axhline(0, color='black', linestyle='-', linewidth=0.5) 
# plt.axvline(0, color='black', linestyle='-', linewidth=0.5) 

plt.title('Average Vehicle speed vs Throughput')
plt.xlabel('Average Speed')
plt.ylabel('Throughput (vehicles/lane/hour)')

# plt.savefig("plotting/output/spf vs reward.png", format="png", dpi=600)
plt.show()
