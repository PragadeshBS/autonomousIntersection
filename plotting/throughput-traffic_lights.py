import seaborn as sns
import matplotlib.pyplot as plt

# Create a 2D array of data
data = [
    [0, 917],
    [923, 0]
]

# Create a heatmap using Seaborn
sns.heatmap(data, annot=True, cmap='viridis', xticklabels=['Lane 1', 'Lane 2'], yticklabels=['Lane 1', 'Lane 2'], vmin=0, vmax=5000)

# Add labels to the x and y axis
plt.xlabel('Destination Lane')
plt.ylabel('Source Lane')

# Add a title to the heatmap
plt.title('Traffic Light Controller', pad=20)
plt.savefig("plotting/output/throughput-traditional.png", format="png", dpi=600)

# Display the heatmap
# plt.show()