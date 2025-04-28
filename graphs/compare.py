import numpy as np
import matplotlib.pyplot as plt


def gnfs_time_complexity(N):
    return np.exp((64 / 9) ** (1 / 3) * (np.log(N)) ** (1 / 3) * (np.log(np.log(N))) ** (2 / 3))

def shor_time_complexity(N):
    return (np.log(N)) ** 3

N_values = np.linspace(1e3, 1e8, 500)
gnfs_values = gnfs_time_complexity(N_values)
shor_values = shor_time_complexity(N_values)

plt.figure(figsize=(10, 6))
plt.plot(N_values, gnfs_values, label="GNFS", color='b')
plt.plot(N_values, shor_values, label="Shor's Algorithm", linestyle='--', color='r')

plt.xlabel("N (size of number to factor)")
plt.ylabel("Time Complexity (arbitrary units)")
plt.yscale("log") 
plt.title("Comparison of GNFS and Shor's Algorithm Time Complexities")
plt.legend()
plt.grid(True)


plt.savefig('shorvsgnfs2.png', dpi=300)

plt.show()
