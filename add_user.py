#!/usr/bin/python3

"""
Linux Add User Python Script
Author @ Travis Hill
10/6/2021
"""

import csv
import subprocess
import os

def check_if_user_exists(username):
    """
    Returns true if the user exists in the system.
    False if the user doesnt exist
    """
    comProcess = subprocess.Popen(["getent", "passwd", username], shell=False, stdout=subprocess.PIPE)
    output = comProcess.stdout.read().decode()
    if output == "":
        return False
    return True


def check_if_group_exists(group):
    """
    Returns true if the group exists in the system.
    False if the group doesnt exist
    """
    comProcess = subprocess.Popen(["getent", "group", group], shell=False, stdout=subprocess.PIPE)
    output = comProcess.stdout.read().decode()
    if output == "":
        return False
    return True

def make_home_directory(department):
    """
    Creates a home directory if it doesnt exist.
    """
    os.chdir("/home")
    if os.path.isdir("/home/" + department):
        pass
    else:
        os.system("sudo mkdir " + department)

    

def create_user(username, group, home):
    """
    Creates a user on the linux system. Checks if the group exists, if not
    it creates the group. If the user is in the office group it sets their shell to use csh
    and bash otherwise. Sets their group and home directives respectfully.
    Then sets their default password to be password and makes it expire instantly.
    """
    make_home_directory(home)
    if check_if_group_exists(group) == False:
        os.system("sudo groupadd " + group)
    if group == "office":
        os.system("sudo useradd -G " + group + " -m -d /home/" + home + "/" + username + " -s /bin/csh " + username)
    else:
       os.system("sudo useradd -G " + group + " -m -d /home/" + home + "/" + username + " -s /bin/bash " + username)
    
    os.system("sudo echo " + username + ":password | sudo chpasswd")
    os.system("sudo passwd -e " + username + " > /dev/null")
    print("          " + username + " added to the system.")
    
def main():
    """
    Gathers information from the CSV file and uses it to create the new user on the system.
    Addresses the issue of two users having the same username.
    """
    os.system("clear")
    print("Adding new users to the system.")
    print("Please note: The default password for new users is password.")
    print("For testing purposes. Change the password to 1$4pizz@.")
    print()
    users = []
    with open('linux_users.csv') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            employee_id = row[0]
            last_name = row[1].lower()
            first_name = row[2].lower()
            office = row[3]
            phone = row[4]
            department = row[5]
            group = row[6]
            if first_name == "" or last_name == "":
                print("Cannot process employee id " + str(employee_id) + "        Insufficient Data.")
                continue
            elif office == "":
                print("Cannot process employee id " + str(employee_id) + "        Not a valid Office.")
                continue
            elif group == "":
                print("Cannot process employee id " + str(employee_id) + "         Not a valid group.")
                continue
            elif department == "":
                print("Cannot process employee id " + str(employee_id) + "        Not a valid Department.")
                continue
            elif phone == "":
                print("Cannot process employee id " + str(employee_id) + "        Not a valid Phone.")
            else:
                print("Processing employee ID ", employee_id, end = " ")
                username = first_name[0] + last_name
                if "'" in username:
                    username = username.replace("'","")
                originalName = username
                count = 1
                while(check_if_user_exists(username) == True):
                    username = originalName + str(count)
                    count += 1
                users.append(username)
                create_user(username, group, department)
        csv_file.close()
main()