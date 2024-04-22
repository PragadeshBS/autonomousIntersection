import seaborn as sns
import matplotlib.pyplot as plt

# Create a 2D array of data
data = [
    [0, 5040],
    [4320, 0]
]

# Create a heatmap using Seaborn
sns.heatmap(data, annot=True, cmap='viridis', xticklabels=['Lane 1', 'Lane 2'], yticklabels=['Lane 1', 'Lane 2'])

# Add labels to the x and y axis
plt.xlabel('Destination Lane')
plt.ylabel('Source Lane')

# Add a title to the heatmap
plt.title('Throughput Matrix for a T-junction (vehicles/hour)', pad=20)

# Display the heatmap
plt.show()