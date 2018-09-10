# Import libraries to handle the filetypes
import csv
import json

# Import the csv and create the JSON file to be written to
jdat = open('jdat.json', 'w')
dat = open('CL_4H.csv', 'rb')

# Count the rows in the input data by creating a list to get the length
counter = csv.DictReader(dat)
rows = list(counter)
rownum = len(rows)

# Delete the objects to free up memory
del counter
del rows

# Reset the data object to 0
dat.seek(0)

# Create reader object and iterator value for json writing
reader = csv.DictReader(dat)
i = 0

# Iterate through each row in the csv data object, incrementing the iterator and
# write it to the JSON file.  Additionally add a '[' to the start of the file
# to create an object within the JSON file
jdat.write('[')
for row in reader:
    i = i + 1
    json.dump(row, jdat, separators=(',', ':'), indent=4)
    # Check if the current row is the last and if not append comma to separate
    # the collection from the next
    if i < rownum:
        jdat.write(',')
# Append ']' to the end of the file to closr the object
jdat.write(']')

# For a more readable JSON file add 'indent=4' into the json.dump parameters
# File names may need to be shortened to make a more space efficient json file
# Due to an error with 'csv.DictReader' python version 2 is required 
