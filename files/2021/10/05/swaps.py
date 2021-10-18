import matplotlib.pyplot as plt 
import csv
import numpy as np

values_of_n = []
swaps_insert = []
swaps_delete_min = []
with open('swaps.csv','r') as csvfile:
  data = csv.reader(csvfile , delimiter = ',')
  for row in data:
    values_of_n.append((float)(row[0]))
    swaps_insert.append((float)(row[1]))
    swaps_delete_min.append((float)(row[2]))
values_of_n = np.asarray(values_of_n)

plt.bar(values_of_n-0.2 , swaps_insert , 0.4 , label = "Insert")
plt.bar(values_of_n+0.2 , swaps_delete_min , 0.4, label = "Delete_min")
plt.xlabel("Values of logn to the base 10")
plt.ylabel("Average swaps")
plt.legend()
plt.savefig("swaps.png")
plt.show()


