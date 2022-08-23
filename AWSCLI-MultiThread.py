#let's run an AWS command across all the accounts we have access to and output the outputs as a CSV
import subprocess
import concurrent.futures
import csv
import pullprofiles #A lib that grabs your .aws/config file and pulls out just the profiles


profiles = pullprofiles.updateprofiles()
# profiles = ['maximus-Network-Lab.AdministratorAccess','Maximus-Logging.907357815766_ReadOnly'] #in case you want to test with only two profiles
regions = ["us-east-1","us-west-2"]
command = "aws ec2 describe-addresses"
# queryfilter= "HostedZones[?contains(Name, `maximus.com`) == `true`].Name"
queryfilter= "Addresses[*].[PublicIp]"
outputfile ="outputEIPS.txt"

outputlist1=[]
#makes a command from the inputs
#example - aws ec2 describe-nat-gateways --profile maximus-storage-oneloginreadonly --region us-east-1  --output text  --query NatGateways[*].NatGatewayId
def makecommand(region,profile, command, queryfilter):
    output = f'{command} --profile {profile} --region {region}  --output text'
    output = output.split(' ')
    if queryfilter:
        output.append("--query")
        output.append(queryfilter)
    # print(output)
    return output


def runcommand(region,profile, command):
    #Makes the command we want to run
    runcommand1 = makecommand(region,profile, command, queryfilter)
    #makes a command to pull the account name
    getaccountNum = makecommand(region,profile, 'aws sts get-caller-identity', '"Account"')
    #Get the output of command1
    ngws = subprocess.check_output(runcommand1)
    ngwsdecoded =ngws.decode("utf-8") #decode it
    # print(ngwsdecoded)
    if ngwsdecoded != "": #if we have data:
        account = subprocess.check_output(getaccountNum)# let's pull the account name, too
        accountdecoded = account.decode("utf-8") #decode that
        accountdecoded=accountdecoded.strip()
        profile2=profile[:profile.rfind('.')]#removes my permission level from the profile name
        ngwsplit = ngwsdecoded.splitlines()
        for line in ngwsplit:
            writeline=[accountdecoded,profile2 ,line] #put all the data we found into a list
            print(writeline)
            outputlist1.append(writeline) #append the data to outputlist1 - a list of lists
            # write.writerow(writeline)


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for profile in profiles[:]:
            for region in regions:
                # print ()
                profile = profile.strip("\n")
                future = executor.submit(runcommand, region, profile, command)
    rows = ['account','name', 'output'] #the top rows of the csv
    with open(outputfile, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(rows) #write the top row
        write.writerows(outputlist1) #write all the output

if __name__ == "__main__":
   main()


        
        