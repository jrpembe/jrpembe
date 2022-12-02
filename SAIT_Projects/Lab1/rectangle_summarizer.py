import csv
from statistics import mean

with open("DATA475_lab_rectangles_data.csv", newline="") as f:  # read the content of the csv file into f
  next(f) # skip the header line
  area=[]
  reader = csv.reader(f)
  for row in reader:
    width = float(row[1])
    length = float(row[2])
    area.append(width*length)
    
summary = {
  "Count:": len(area),
  "Total:": sum(area),
  "Average:": mean(area),
  "Max:": max(area),
  "Min:": min(area)
}

# for key in summary:
#   print(key, summary[key])

for key, value in summary.items():
  print(key, value)
  
with open("summary.csv", "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerow(summary.keys())
  writer.writerow(summary.values())
