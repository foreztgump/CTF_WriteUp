import requests
import sys

#  A function to take the URL and print the version of Joomla
def get_version(url):
    url = url + "/administrator/manifests/files/joomla.xml"
    #  Send a request to the URL
    r = requests.get(url)
    #  If the request is successful
    if r.status_code == 200:
        #  Split the response into lines
        lines = r.text.splitlines()
        #  Loop through the lines
        for line in lines:
            #  If the line contains the version
            if '<version>' in line:
                # split <version>3.7.0</version> into ['<version>', '3.7.0', '</version>']
                version = line.split('>')
                #  Print the version
                print("Joomla version : "+version[1].split('<')[0])
    #  If the request is not successful
    else:
        #  Return an error
        return "Error"

#  If the script is run from the command line
if __name__ == "__main__":
    #  If the script is run with the correct number of arguments
    if len(sys.argv) == 2:
        #  Run the get_version function
        get_version(sys.argv[1])
    #  If the script is run with the wrong number of arguments
    else:
        #  Print the usage
        print("Only works on Joomla websites >= 1.6.0\n")
        print("Usage: python3 joomla_version_checker.py [url]")
        print("Example: python3 joomla_version_checker.py http://10.10.11.13")