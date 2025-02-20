import csv
import matplotlib.pyplot as plt

data = []

# with open('\\estimates\\errorratevariation(1).csv', 'r') as file:
#    for line in file:
#       data.append(line.split(","))
# file.close()

err_rate, n_bits, volumes = zip(*[(exps[0], exps[1], float(exps[6].strip("\n"))) for exps in (line.split(",") for line in open('\\estimates\\errorratevariation(1).csv'))])

err_rate = [exps[0] for exps in data]
n_bits = [exps[1] for exps in data]
volumes = [float(exps[6].strip("\n")) for exps in data]

fig, ax1 = plt.subplots()

ax1.set_xlabel('Error Rates')
ax1.set_ylabel('Number of Bits')
ax1.plot(err_rate, n_bits)
ax1.tick_params(axis='y')

ax2 = ax1.twinx() 
ax2.plot(err_rate, volumes, color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.set_ylabel('Volume (megaqubitdays)')
plt.title("Simple Line Plot")

fig.tight_layout()
plt.show()
