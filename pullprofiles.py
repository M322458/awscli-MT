
#Grabs all the config profiles you have in your .aws/config file and puts them into a profiles.txt file
import re
from pathlib import Path


def updateprofiles():
    home = str(Path.home()) #for windows
    credfile = home+'/.aws/config'
    file = open(credfile, "r")
    #regex search based on open bracket
    pattern = "\["
    list1 = []
    for line in file:
        if re.search(pattern, line): #if the line starts with a [ bracket
            line = line.replace("[profile ", "") #remote the "[profile"
            line = line.replace("]", "")#remote the close bracket]
            list1.append(line) #append that to the list to return
    return(list1)

    
if __name__ == "__main__":
    updateprofiles()