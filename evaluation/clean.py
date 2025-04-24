
def remove_array(wholelist, target):
   return [arr for arr in wholelist if arr != target]

def print_array(array):
   for item in array:
      print(item)


def extract_data(fileName):
   data = [line.split(",") for line in open(fileName)]

   for line in data:
      if line[0] != 'rsaeh':
         data = remove_array(data, line)

   cared_data = [tuple([int(line[1]), float(line[7].strip("\n"))]) for line in data]
   
   return cared_data

def extract_dataEx(fileName):
   data = [line.split(",") for line in open(fileName)]

   cared_data = [tuple([int(line[0]), float(line[1].strip("\n"))]) for line in data]
   
   return cared_data

#fileName = 'C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\circuits\\Shor1991\\Agib25\\openingdata1e3wrunway.csv'