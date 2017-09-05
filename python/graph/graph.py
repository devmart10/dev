import numpy as np
import matplotlib.pyplot as plt
import random

# x = np.arange(1, 20, 1);
# y = np.arange(20, 50)

x = [i for i in range(10)]
y = [int(20 + i*random.random()) for i in range(10)]

plt.plot(x, y)
plt.axes([0, 10, 0, 30])
plt.show()