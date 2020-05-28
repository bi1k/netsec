#!/bin/bash

# Text colour variables.
YELLOW="\e[1;93m"
CYAN="\e[0;96m"
CYAN_B="\e[1;96m"
RESET="\e[0m"

# File location variables.
INPUT_FILE="initial_enum_resources/ips.txt"			# List of IP addresses to scan.
WORDLIST="initial_enum_resources/custom_web_wordlist.txt"	# Custom wordlist for dirbuster.
FAST_FILE="results/quick_scan.txt"				# Location of Nmap quick scan output file.
AUTORECON="/usr/bin/autorecon"					# Location of autorecon script.

# Autorecon symblols used throughout the program.
STAR=$CYAN"["$CYAN_B"*"$CYAN"]"$RESET
EXCL=$CYAN"["$CYAN_B"!"$CYAN"]"$RESET

# Run dirbuster for any port services containing the string http.
go_dirbust () {
	printf $STAR" Running task "$CYAN_B"dirbuster"$RESET" on "$YELLOW"$1"$RESET":$2\n"

	# If the custom wordlist doesn't exist, use one of the OOTB dirbuster wordlists.
	if test -f $WORDLIST
	then
		wordlist=$WORDLIST
	elif test -f /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
	then
		wordlist=/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
		printf $EXCL" Specified wordlist not found at "$CYAN_B$WORDLIST$RESET". Using dirbuster medium wordlist\n"
	else
		printf $EXCL" Unable to find wordlist at "$CYAN_B$WORDLIST$RESET" or at "$CYAN_B"/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt"$RESET".\n"
fi

	dirbuster -u http://$1:$2 -l $wordlist > results/$1/dirbuster_$2.txt 2> results/$1/dirbuster_$2_errors.txt &
}

init_enum () {

	# Make sure the results directory exists.
	if test -d "results"
	then
		:
	else
		mkdir results
	fi

	# Make sure the FAST_FILE doesn't exist from previous scans.
	if test -f $FAST_FILE
	then
		rm $FAST_FILE
	fi

	# Runs a quick nmap scan so that manual enumeration can start immediately.
	printf $STAR" Running quick nmap scan - "$CYAN_B"top 1000 TCP ports"$RESET" on hosts in "$CYAN_B$INPUT_FILE"\n"$RESET
	nmap -iL $INPUT_FILE -T4 --open --top-ports=1000 -oN $FAST_FILE > /dev/null
	printf $STAR" Quick nmap scan - "$CYAN_B"top 1000 TCP ports "$RESET"on hosts in "$CYAN_B$INPUT_FILE$RESET" finished successfully\n"
	cat $FAST_FILE

	# For each IP address in ips.txt, run the following:
	while read -r ip_add
	do

		# Make sure the results/ip directory exists.
		if test -d "results/$ip_add"
		then
			:
		else
			mkdir results/$ip_add
		fi

		# Run full Nmap TCP scan for the given IP address. It runs with -T4 so it may miss a port or two.
		# The double-check scans at the end of the program will run this scan again slower to make sure nothing is missed.
		printf $STAR" Running nmap scan - "$CYAN_B"all TCP ports "$RESET"on "$CYAN_B"$ip_add\n"$RESET
		nmap -p- $ip_add -T4 -oG results/"$ip_add"/nmap_tcp_oG.txt > /dev/null
		printf $STAR" Nmap scan - "$CYAN_B"all TCP ports "$RESET"on "$YELLOW"$ip_add"$RESET" finished successfully\n"

		# If any ports are open, format the results in a way that can be easily read by the program.
		if grep -q "open" results/$ip_add/nmap_tcp_oG.txt
		then
			tcp_ports=$(cat results/"$ip_add"/nmap_tcp_oG.txt | tr " " "\n" | grep "/open" | cut -d "/" -f 1 | tr "\n" ",")
			tcp_ports=${tcp_ports::-1}
			cat results/"$ip_add"/nmap_tcp_oG.txt | tr " " "\n" | grep "/open" | cut -d "/" -f 1,5 | tr "/" " " > results/$ip_add/nmap_tcp_summary.txt
			printf "PORT & SERVICE\n"
			cat results/$ip_add/nmap_tcp_summary.txt
			printf "\n"

			# Read ports detected and determine which enumeration to perform. Line format = <port> - <service>
			while read -r port_line
			do

				# port variable removes the service name from the portcat _line variable.
				port=$(printf "$port_line" | cut -d " " -f 1)

				# For http/https, perform the following enumeration.
				if [[ "$port_line" == *"http"* ]]
				then
					go_dirbust $ip_add $port
				fi
			done < results/$ip_add/nmap_tcp_summary.txt

			# Run Nmap scan on ports that are open. Check for service information + safe / vulnerability NSE scripts.
			printf $STAR" Running nmap service & vulnerability detection - "$CYAN_B"open TCP ports "$RESET"on "$YELLOW"$ip_add\n"$RESET
			nmap -p $tcp_ports $ip_add -sC -sV --script=*vuln* -T2 -oN results/"$ip_add"/nmap_tcp_serv_vuln.txt > /dev/null
			printf $STAR" Nmap service & vulnerability detection - "$CYAN_B"open TCP ports "$RESET"on "$YELLOW"$ip_add"$RESET" finished successfully\n"
			cat results/"$ip_add"/nmap_tcp_serv_vuln.txt
		fi
	done < $INPUT_FILE
}

# This function checks to see whether any nmap processes are running from autorecon.
# Once all autorecon nmap scans are finished,
# a three full TCP nmap scans are run slowly to make sure no ports were missed in the previous nmap scans.
double_check () {
	declare -i nmap_doublecheck=0
	nmap_source_output="results/nmap_tcp_all.txt"
	nmap_compare_output="results/nmap_tcp_compare.txt"
	while [[ $nmap_doublecheck -ne 3 ]]
	do
		if [[ $nmap_doublecheck -eq 0 ]]
		then
			sleep 5
		fi

		# Checks to see whether the string nmap exists in any running processes.
		# The way nmap is written in the grep statement
		# is to prevent grep from picking up the process that is searching for nmap.
		if ps aux | grep -q "[n]map"
		then
			:
		else
			if [[ $nmap_doublecheck -eq 0 ]]
			then
				sleep 5
			fi

			# The same check is run in case another nmap scan has started for some reason.
			# Both checks need to not have nmap running in succession in order for the double-check nmap scans to begin.
			if ps aux | grep -q "[n]map"
			then
				:
			else
				nmap_doublecheck+=1
				printf $STAR" Running nmap scan to double check results ("$CYAN_B$nmap_doublecheck$RESET"/"$CYAN_B"3"$RESET") - "$CYAN_B"all TCP ports"$RESET" on hosts in "$CYAN_B$INPUT_FILE"\n"$RESET

				# If this is the first double-check scan, results will be stored in nmap_stored_output
				if [[ $nmap_doublecheck -eq 1 ]]
				then
					nmap -p- -iL $INPUT_FILE -T4 --open -oN $nmap_source_output > /dev/null
					printf $STAR" Nmap scan - "$CYAN_B"all TCP ports "$RESET"on hosts in "$CYAN_B$INPUT_FILE$RESET" finished successfully.\n"
					cat $nmap_source_output

				# Else, results will be stored in nmap_compare_output so that it can be compared with nmap_stored_output.
				# The nmap_compare_output file should not exist at this point.
				else
					if test -f $nmap_compare_output
					then
						rm $nmap_compare_output
					fi
					nmap -p- -iL $INPUT_FILE -T3 --open -oN $nmap_compare_output > /dev/null
					printf $STAR" Nmap scan - "$CYAN_B"all TCP ports "$RESET"on hosts in "$CYAN_B$INPUT_FILE$RESET" finished successfully.\n"

					# If the results from the later scans contain more lines than the earlier scans, alert the user.
					if [[ $(wc -l <$nmap_source_output) -lt $(wc -l <$nmap_compare_output) ]]
					then
						mv $nmap_compare_output $nmap_source_output
						printf $EXCL" The latest nmap scan has more findings than the previous scan. Check the latest nmap output.\n"
						cat $nmap_source_output
					fi
					rm $nmap_compare_output
				fi
			fi
		fi
	done
}

# Check if ips.txt exists and contains contents.
if test -f $INPUT_FILE
then
	if [[ $(wc -c <$INPUT_FILE) -lt 7 ]]
	then
		printf $EXCL" The ips.txt file containing IP addresses to scan is missing or doesn't contain any IP addresses.\n"
		exit 0
	fi
else
	printf $EXCL" The ips.txt file within 'initial_enum_resources' containing IP addresses to scan doesn't exist.\n"
	exit 0
fi

# Check to see whether the user wants to run initial scans or to skip straight to autorecon.
# If Y, run initial scans. If N, skip to autorecon. Else, terminate the program and advise the user on what they need to input.

read -p "Do you want to run initial scans? Skipping this will start autorecon immediately. (Y/N): " u_input
#read -p Caution: initial_enum resets the CLI once it has finished (Y/N):  u_input
if [[ $u_input == "y" ]] || [[ $u_input == "Y" ]]
then
	init_enum
fi

if [[ $u_input == "y" ]] || [[ $u_input == "Y" ]] || [[ $u_input == "n" ]] || [[ $u_input == "N" ]]
then
	if test -f $AUTORECON
	then
		double_check &
		double_pid=$!
		$AUTORECON -t $INPUT_FILE

		# Don't terminate the program until double_check finished.
		wait $double_pid
		sleep 1
		printf $EXCL" Note: /usr/bin/reset may need to be run to reset the CLI.\n"
	else
		printf $EXCL$CYAN_B" Autorecon "$RESET"was not found at "$CYAN_B$AUTORECON"\n"$RESET
	fi

else
	printf $EXCL" Invalid input, please rerun the script and enter either "$CYAN_B"Y"$RESET" for yes or "$CYAN"N"$RESET" for no\n"
fi
