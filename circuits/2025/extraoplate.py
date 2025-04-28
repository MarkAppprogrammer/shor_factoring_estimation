import csv
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
from scipy.optimize import curve_fit
from numpy.polynomial.polynomial import Polynomial


data = [line.split(",") for line in open('openingdata1e3wrunway(1).csv')]

bits = [int(exps[1]) for exps in data]  
bits = sorted(list(set(bits))) 
qubits = [int(exps[3]) for exps in data] 
hours = [float(exps[5]) for exps in data] 
mqds = [float(exps[7]) for exps in data] 
error_rates = sorted(set(float(exps[2]) for exps in data))  
fig, ax1 = plt.subplots()

# ax2 = ax1.twinx()

colors = ['b', 'g', 'r', 'c', 'm']

"""

TO-DO:

   1) qubtis scale off and hours scale off most likely swapped for some reason
   2) Create graphs for comparison of diffrent optmizations? or tables?
   3) RUNWAYS checkmark

"""
# Create figure and axis with desired size BEFORE plotting
# fig, ax1 = plt.subplots(figsize=(11, 7))

# for i, err in enumerate(error_rates):
#     y_mqds = [mqds[j] for j in range(len(data)) if float(data[j][2]) == err]
#     ax1.plot(bits, y_mqds, marker='s', linestyle='--', color=colors[i], label=f'Volume (error ={err:.0e})')

# # Axis labels and formatting
# ax1.set_xlabel("RSA Key Size (bits)")
# ax1.set_ylabel("Expected Volume (Megaqubitdays)")
# ax1.set_yscale("log")
# ax1.legend(loc="upper left")

# # X-axis spacing
# plt.xticks(np.arange(0, 64001, 8000))
# plt.tick_params(axis='x', pad=10)

# # Grid and title
# plt.grid(True)
# plt.title("RSA Key Size vs Expected Volume for Diffrent Error Rates")

# # Show the plot
# #plt.show()


# plt.savefig("graphs/errorratersa.png", bbox_inches='tight', dpi=300)
# plt.close()

#create a plot w/ each algo and hours and bits 
"""
key:

rsaeh: RSA via Ekera-HÃ¥stad with s = 1 in a single run
dlpss: Discrete logarithms Schnorr group via Shor
dlpseh: Discrete logarithms Schnorr group via Ekera-HÃ¥stad with s = 1 in a single run
dlpseeh: Discrete logarithms short exponent via EkerÃ¥-HÃ¥stad with s = 1 in a single run
dlps: Discrete logarithms general via Shor
dlpe: Discrete logarithms general via EkerÃ¥ with s = 1 in a single run

"""
algonames = ["RSA via Ekera-HÃ¥stad", "Schnorr DLP via Shor", "Schnorr or Short DLP via EH", "Short DLP via EH", "General DLP via Shor", "General DLP via EH"]
algos = ["rsaeh", "dlpss", "dlpseh", "dlpseeh", "dlps", "dlpe"]

markers = ['o', 's', 'v', '^', 'D', 'P']
colors = ['b', 'g', 'r', 'c', 'm', 'C6']


data = [line.split(",") for line in open('openingdata1e3.csv')]
new_data = [[] for _ in range(len(algos))]

for i, line in enumerate(data):
   for j in range(len(algos)):
      if line[0] == algos[j]:
         new_data[j].append(line)

# x = [row[1] for row in data[0]]  
fig, ax1 = plt.subplots(figsize=(11, 7))

for i, algo in enumerate(new_data):
   if i != 3: #schnorr and short dlp via eh produce the same results
      y_hours = [float(row[5]) for row in algo]

      if i == 0:
         x = [int(row[1]) for row in algo] 
         print(x)

      y_qubits = [float(row[3]) for row in algo]
      #y_mqd = [float(row[7]) for row in algo]
      
      # print(i)
      

      ax1.plot(x, y_qubits, marker=markers[i], linestyle='-', color=colors[i], label=f'{algonames[i]} Qubits')
      # ax1.plot(x, y_hours, marker=markers[i], linestyle='--', color=colors[i], label=f'{algonames[i]} Hours')

      #ax2.plot(x, y_hours, marker='s', linestyle='--', color=colors[i], label=f'Hours (err={err:.0e})')

#print(x)

#ax1.loglog(x, y_hours)

ax1.set_xlabel("Modulus Length (bits)")
ax1.set_ylabel("Qubits")

ax1.legend(loc="upper left")
#ax1.set_yscale("log")

#plt.xticks(x, rotation=45)
plt.xticks(np.arange(0, 64001, 8000))

plt.title("Modulus Length vs Total Qubits for Problems and their Algorithms")
plt.grid(True)

plt.savefig("C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\graphs\\qubitsforeach.png", bbox_inches='tight', dpi=300)
plt.close()

#plt.show()
#print()
# def exp_func(x, a, b):
#     return a * np.exp(b * x)

# fig, ax1 = plt.subplots()

# for i, algo in enumerate(new_data):
#    if i == 0: #only rsa
#       x = [int(row[1]) for row in algo] 
#       x = np.array(x, dtype=int)

#       #y_qubits = [float(row[3]) for row in algo]
#       y_hours = [float(row[5]) for row in algo]
#       y = np.array(y_hours, dtype=float)


#       #ax1.plot(x, y_qubits, marker=markers[i], linestyle='-', color=colors[i], label=f'{algonames[i]} Qubits')
#       ax1.plot(x, y_hours, marker=markers[i], linestyle='None', color=colors[i], label=f'{algonames[i]} Hours')

#       #stats test
#       # popt, pcov = curve_fit(exp_func, x, y_hours)

#       # a, b = popt

#       # y_pred = exp_func(x, *popt)
#       # ss_res = np.sum((y_hours - y_pred) ** 2)
#       # ss_tot = np.sum((y_hours - np.mean(y_hours)) ** 2)
#       # r_squared = 1 - (ss_res / ss_tot)

#       # print(f"Fitted equation: y = {a:.2f} * e^({b:.2f}x)")
#       # print(f"R² = {r_squared:.4f}") 

#       # plt.scatter(x, y_hours, label="Data")
#       # plt.plot(x, y_pred, label="Exponential Fit", color="red")
#       # plt.legend()
#       # plt.show()

#       # x = np.array(x, dtype=float)
#       # log_y = np.log(y_hours) 

#       # slope, intercept, r_value, _, _ = linregress(x, log_y)

#       # print(f"Slope (b) = {slope:.2f}, R² = {r_value**2:.4f}")

#       # # Plot log-transformed data
#       # import matplotlib.pyplot as plt
#       # plt.scatter(x, log_y, label="Log-Transformed Data")
#       # plt.plot(x, slope * x + intercept, color="red", label="Linear Fit")
#       # plt.xlabel("x")
#       # plt.ylabel("log(y_hours)")
#       # plt.legend()
#       # plt.show()

#       growth_factors = [y_hours[i+1] / y_hours[i] for i in range(len(y_hours)-1)]
#       print("Growth Factors:", growth_factors)

#       # Scale data to avoid large coefficients
#       x_scaled = x / max(x)
#       y_scaled = y / max(y)

#       # Fit a quadratic model
#       coefs = np.polyfit(x_scaled, y_scaled, 2)
#       p = np.poly1d(coefs)

#       # Generate predicted values
#       x_fit = np.linspace(min(x_scaled), max(x_scaled), 100)
#       y_fit = p(x_fit)

#       # Compute R²
#       y_pred_scaled = p(x_scaled)
#       ss_res = np.sum((y_scaled - y_pred_scaled) ** 2)
#       ss_tot = np.sum((y_scaled - np.mean(y_scaled)) ** 2)
#       r_squared = 1 - (ss_res / ss_tot)

#       # Scale coefficients back to original values
#       a, b, c = coefs[0], coefs[1], coefs[2]
#       equation_text = f"$y = {a:.3f}x^2 + {b:.3f}x + {c:.3f}$\n$R^2 = {r_squared:.4f}$"

#       # Plot data points and fitted curve
#       plt.scatter(x_scaled, y_scaled, color="blue", label="Original Data", zorder=2)
#       plt.plot(x_fit, y_fit, color="red", label="Quadratic Fit", zorder =1)
#       plt.xlabel("x (scaled)")
#       plt.ylabel("y (scaled)")
#       plt.legend()
#       plt.title("Quadratic Fit")

#       # Add equation as text on the plot
#       plt.text(0.05, 0.85, equation_text, transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.7))

#       plt.show()



#print(x)

# ax1.set_xlabel("Bits of RSA Integers")
# ax1.set_ylabel("Hours")

# # ax1.legend(loc="upper left")
# #ax1.set_yscale("log")

# plt.title("Total Hours vs Size of RSA Integers for Different Algorithms")

# #plt.savefig("hours_every_algo.png", bbox_inches='tight', dpi=300)
# plt.show()


"""
w/runways: [312.7488571808906, 2242.647054307973, 6834.21062320976, 15998.743277171072, 30996.25970619373, 55818.06257872592, 85881.74750665535, 133706.9862427167, 259071.86220288335, 442691.68263467844, 740428.3948361782, 1075562.1740069115, 2105652.4026730424, 3852585.027474984, 5994894.571145596, 8743701.903620146, 17848241.35374431, 33055447.747433994, 46955616.849538274, 70070147.48727427]
w/o runways: [390.19687577370865, 3532.196124605099, 13189.084992647227, 30094.9544313143, 270204.859291302, 933385.2526999761, 2280809.0400966895, 4535126.702942901, 8254649.7755240165, 12757890.030489247, 19669177.068654463, 36992132.73010083, 63954614.95783627, 101626003.69326676, 151823603.6835037]
"""

