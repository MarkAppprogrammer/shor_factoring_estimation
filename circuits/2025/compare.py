import math
import matplotlib.pyplot as plt


oldEstimates = {
   2048 : 4.1, 
   3072 : 19,
   4096 : 48,
   8192 : 480, 
   12288 : 1700, 
   16384 : 3900
}

newEstimates = {
   2048 : 1.15, 
   3072 : 4.15,
   4096 : 10.54,
   8192 : 102.31, 
   12288 : 389.49, 
   16384 : 1011.21
}

mean = 0
differences = []
percentageDifferences = []

fig, ax1 = plt.subplots()

for item in oldEstimates:
   old = oldEstimates[item]
   new = newEstimates[item]
   difference = old - new

   differences.append(difference)
   mean += difference
   percentageDifferences.append(difference / new * 100)

   print(f"RSA Integer size: {item} Old: {old} New: {new} Diffrence: {difference}x")

   ax1.plot(item, old, marker='o', linestyle='-', color='blue')
   ax1.plot(item, new, marker='o', linestyle='--', color='red')

mean = mean / len(oldEstimates)
sd = math.sqrt(sum((x - mean) ** 2 for x in differences) / (len(oldEstimates) - 1))

print()

print(f"Mean diffrence: {mean}x")
print(f"Standard deviation: {sd}x")
print(f"Paired T-test: {mean/ (sd / math.sqrt(len(differences)))}")

print()
print(percentageDifferences)
print(f"Mean percentage diffrence: {sum(percentageDifferences) / len(percentageDifferences)}%")
print(f"Max percentage diffrence: {max(percentageDifferences)}%")

plt.grid(True)
plt.xlabel("RSA Integer Size")
plt.ylabel("Estimation (in megaqubitdays)")
plt.title("Comparison of Old and New Estimates for RSA Integer Sizes")
plt.xticks(list(oldEstimates.keys()), rotation=45)

plt.show()