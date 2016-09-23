""""    This file simply pulls passes a file as the first argurment and parses GPGGA sentences, line-by-line    ""

import sys, re

path = sys.argv[1]
list_line = []
with open(path,'r') as file:
    for line in file:
        if (re.search('GGA',line)):
            line = line.split("$")
            line = line[1].split(',')
            list_line.append(line)

cvs_file = path + ".csv"
with open(cvs_file, 'w') as cvs_f:
    writer  = cvs_file
    for i in range(len(list_line)):
        writer.writerow( (i+1, list_line[i]) )
