
#Grabs all the config profiles you have in your .aws/config file and puts them into a profiles.txt file
import re
from pathlib import Path


def updateprofiles():
    home = str(Path.home()) #Your home dir - at least in windows
    credfile = home+'/.aws/config' #your aws cred file
    file = open(credfile, "r") #open the file
    #regex search based on open bracket
    pattern = "\[" #regex pattern we're going to look for  - open bracket
    list1 = [] #list that we'll output all the data to
    for line in file:
        if re.search(pattern, line): #if the line starts with a [ bracket
            line = line.replace("[profile ", "") #remove the "[profile"
            line = line.replace("]", "")#remove the close bracket]
            list1.append(line) #append that to the list to return
    return(list1) #return that list

    
if __name__ == "__main__":
    updateprofiles()