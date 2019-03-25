#!/usr/bin/env python
#Freddy Rayes - 2019
#
#This program retrieves files from FTP Server if found missing in local directory. 
#Takes in an input file 'login.txt' that is stored in the same directory
#containing the python file. 
#
#The text file should contain on a seperate line for each:
#  address of server
#  username
#  password

import ftplib 
import os

def main():
    
    #get login details
    login_info = getLoginInfo('login.txt')

    #specify paths below
    ftp_path = '/incoming/test_dir'
    local_path = '/home/userid/test'
    
    #login to FTP server
    ftp = ftpLogin(login_info)

    #ftp filelist
    ftp.cwd(ftp_path) #navigate to intended server directoy
    ftp_filelist = ftp.nlst()  #get list of files in server directory
    print("Files in the FTP directory:", ftp_filelist)
    
    #local path filelist
    os.chdir(local_path)
    local_filelist = getDestinationFileList(local_path)
    print("Files in local directory: ", local_filelist)  

    #get list of missing files
    missingFiles = compareFileLists(ftp_filelist, local_filelist)

    #download missing files from server
    if len(missingFiles) > 0:
        print("Downloading the following files: ", missingFiles)
        ftpDownload(ftp, missingFiles)
    else:
        print("All files from FTP server are already in the local path, nothing to download!")
    
    #disconnect from server
    ftp.quit() 


    
def getLoginInfo(filename):
    #retrieve ftp server information from text file
    with open( filename, 'r') as f:
        return f.read().splitlines()   


def compareFileLists(ftpList, destinationList):
    #sort both lists incrementing order
    ftpList = sorted(ftpList)
    destinationList = sorted(destinationList)

    #compare two lists for missing files
    destListSet = set(destinationList)
    missingFiles = [x for x in ftpList if x not in destListSet]
    return missingFiles


def getDestinationFileList(dir_path):
    #returns a list of files from the directory
    return os.listdir(dir_path)


def ftpDownload(ftp, filelist):
    #retrieves filename from list and downloads from server
    for filename in filelist:
        fhandle = open(filename, 'wb')
        try: 
            ftp.retrbinary('RETR ' + filename, fhandle.write)                                
        except:
            print("ERROR")    
        fhandle.close()  


def ftpLogin(login_info):
    #extract login information
    ftp_srv = login_info[0]
    ftp_usr = login_info[1]
    ftp_pass = login_info[2]

    #ftp setup and login
    ftp = ftplib.FTP(ftp_srv)
    ftp.login(ftp_usr, ftp_pass)

    #display server message
    print( ftp.getwelcome() )
   
    return ftp


if __name__ == '__main__':
    main()
