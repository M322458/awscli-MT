#Runs a multithreaded AWS command accross all the accounts you have access to.
presuming your .aws/config file has a bunch of lines like [profile account123.administratoraccess]
and you're running aws commands like "aws ec2 describe-addresses --region us-east-1 --profile account123.administratoraccess

pullprofiles.py will extract the profile names into list

AWSCLI-Multithread.py will run commands across the regions at the top of the file against the profiles that pullprofiles.py found
edit the variables at the top of AWSCLI-Multithread.py, then run the file.
Probably best to ensure your AWSCLI command only returns a single item.