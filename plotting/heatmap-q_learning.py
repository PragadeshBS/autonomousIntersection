import seaborn as sns
import matplotlib.pyplot as plt

# Create a 2D array of data
data = [
    [0, 5040, 312],
    [4320, 0, 1440],
    [1080, 216, 0]
]

# data = [
#     [0, 920],
#     [920, 0]
# ]

# Create a heatmap using Seaborn
sns.heatmap(data, annot=True, cmap='viridis', xticklabels=['Lane 1', 'Lane 2'], yticklabels=['Lane 1', 'Lane 2'], vmin=0, vmax=5000, fmt='g')

# Add labels to the x and y axis
plt.xlabel('Destination Lane')
plt.ylabel('Source Lane')

# Add a title to the heatmap
plt.title('Throughput Matrix for a T-junction with RL controller (vehicles/hour)', pad=20)

# Display the heatmap
plt.show()