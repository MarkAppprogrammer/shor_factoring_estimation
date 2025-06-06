
def remove_array(wholelist, target):
   return [arr for arr in wholelist if arr != target]

def print_array(array):
   for item in array:
      print(item)


def extract_data(fileName, onevar=True):
   data = [line.split(",") for line in open(fileName)]

   for line in data:
      if line[0] != 'rsaeh':
         data = remove_array(data, line)


   if (onevar) :
      cared_data = [tuple([int(line[1]), float(line[7].strip("\n"))]) for line in data]
   else:
      cared_data = [tuple([int(line[1]), float(line[7]), float(line[6]), float(line[5].strip("\n"))/24]) for line in data]
   return cared_data

def extract_dataEx(fileName, onevar = True):
   data = [line.split(",") for line in open(fileName)]

   if (onevar) :
      cared_data = [tuple([int(line[0]), float(line[1].strip("\n"))]) for line in data]
   else:
      cared_data = [tuple([int(line[0]), float(line[1]), float(line[2]), float(line[3].strip("\n"))]) for line in data]
   
   return cared_data

# fileName = 'openingdata1e3wrunway(1).csv'
# print(extract_data(fileName=fileName, onevar=False))