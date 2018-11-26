#!/usr/bin/env python

import paramiko
import time
import re
import sys

#Open telnet connection to devices
def open_ssh_conn(ip):
    #Change exception message
    try:
        
        user_file = sys.argv[1]
        
        cmd_file = sys.argv[2]
        
        selected_user_file = open(user_file, 'r')
        
        selected_user_file.seek(0)
        
        username = selected_user_file.readlines()[0].split(',')[0]
        
        selected_user_file.seek(0)
        
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")

        session = paramiko.SSHClient()
        
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        session.connect(ip, username = username, password = password)
        
        connection = session.invoke_shell()
        
        
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        time.sleep(1)
        
        #Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        
        #Open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r')
        
        #Starting from the beginning of the file
        selected_cmd_file.seek(0)
        
        #Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(1)
            
        
        selected_user_file.close()
            
        #Closing the file
        selected_cmd_file.close()
        
        router_output = connection.recv(65535)
        
        if re.search(r"% Invalid input detected at", router_output):
            print "* There was at least one IOS syntax error on device %s" % ip
        else:
            print "\nDONE for device %s" % ip
        
        print router_output + "\n"
        
        session.close()
    
    except paramiko.AuthenticationException:
        print "* Invalid username or password. \n* Please check the username/password file or the device config"
        print "* Closing program...\n"
        
#Calling the Telnet function
open_ssh_conn("192.168.2.101")


