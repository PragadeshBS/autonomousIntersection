import matplotlib.pyplot as plt

# Define the bar labels and values
labels = ['Traditional Traffic Light', 'Q Learning based controller']
values = [2, 1.34]

# Create the bar chart
plt.bar(labels, values, color=['blue', 'green'])

# Add a title
plt.title('Comparison of Time Taken to Clear the Intersection')

plt.ylabel("Time taken (s)")

# Show the plot
plt.show()