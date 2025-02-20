import csv
import matplotlib.pyplot as plt

# Read data from file
data = [line.split(",") for line in open('C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\circuits\\Shor1991\\Agib25\\errorratevariation(1).csv')]

newdata = sorted(data, key=lambda l:l[1])

data3d = [[] for _ in range(6)]  

current_err = None
i = 0

for array in newdata:
    err_value = float(array[1])
    
    if current_err is None or err_value != current_err:
        current_err = err_value
        i += 1
        i = min(i, 5)
    
    data3d[i].append(array)

print(data3d)
data3d.remove(data3d[0])

colors = ['red', 'blue', 'green', 'orange', 'purple']

for i, arrays in enumerate(data3d):
   n_bits = [float(exps[0]) for exps in arrays]
   qubits = [float(exps[5]) for exps in arrays]
   
   plt.plot(n_bits, qubits, 
            label=f'Qubits with error rate: {arrays[0][1]}', 
            color=colors[i % len(colors)])



# Extract values
# n_bits = [float(exps[0]) for exps in newdata]
# err_rate = [float(exps[1]) for exps in data]
# volumes = [float(exps[6].strip("\n")) for exps in data]
# hours = [float(exps[4]) for exps in data]
# qubits = [float(exps[5]) for exps in newdata]

# print(volumes)
# print(n_bits)
# print(err_rate)

# Plot data
# plt.plot(n_bits, hours, label='hours')
# plt.plot(n_bits, qubits, label='qubits', color='red')
plt.xlabel('Number of bits')
plt.ylabel('Number of qubits (megaqubits)')
plt.legend()
plt.title("Not ready yet")
plt.show()
