# create a 2d array of size 2x100 
# the values can either be 0, 0.48 or 0.76
# the second row should have a different value than the first row for the same column
import numpy as np

# Define the possible values
values = [0, 0.48, 0.76, 1]

# Initialize the 2D array
weights = np.zeros((2, 100))

# Fill the array
for i in range(100):
    weights[0, i] = np.random.choice(values)
    if weights[0, i] == 0 and np.random.rand() > 0.1:
        weights[0, i] = 0.48
    # Remove the chosen value for the first row from the options for the second row
    second_row_values = [value for value in values[1:] if value != weights[0, i]]
    weights[1, i] = np.random.choice(second_row_values)
    if np.random.rand() > 0.65:
        # set the second row value to be the same as the first row value
        weights[1, i] = weights[0, i]

# plot the values in a line graph with two lines of different colors

import matplotlib.pyplot as plt

# set y axis limit to be 0 to 5

plt.ylim(0, 1.5)
plt.plot(weights[0], color='blue')
plt.plot(weights[1], color='red')

# set the x axis label to be "time"
plt.xlabel("Time")
plt.ylabel("Weight/Speed")
plt.title("Values of edge weights in two successive edges of a lane")
plt.show()