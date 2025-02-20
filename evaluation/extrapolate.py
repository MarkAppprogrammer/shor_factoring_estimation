import csv
import matplotlib.pyplot as plt

data = [line.split(",") for line in open('errorratevariation(1).csv')]

bits = [int(exps[0]) for exps in data]   
qubits = [int(exps[2]) for exps in data] 
hours = [float(exps[4]) for exps in data] 
error_rates = sorted(set(float(exps[1]) for exps in data))  

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()

colors = ['b', 'g', 'r', 'c', 'm']

for i, err in enumerate(error_rates):
   x = [bits[j] for j in range(len(data)) if float(data[j][1]) == err]
   y_qubits = [qubits[j] for j in range(len(data)) if float(data[j][1]) == err]
   y_hours = [hours[j] for j in range(len(data)) if float(data[j][1]) == err]

   ax1.plot(x, y_qubits, marker='o', linestyle='-', color=colors[i], label=f'Qubits (err={err:.0e})')

   ax2.plot(x, y_hours, marker='s', linestyle='--', color=colors[i], label=f'Hours (err={err:.0e})')

ax1.set_xlabel("Bits of RSA Integers")
# ax1.set_ylabel("Qubits (megaqubits)")
ax2.set_ylabel("Hours")

ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

plt.title("Qubits and Hours vs Size of RSA Integers for Different Error Rates")
plt.show()
