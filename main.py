# main function for AI-IDS project

def main():
    print('AI-IDS journey begins!')


# Step: Add log reading and basic anomaly detection 
try:
    with open("logs.txt", "r") as file: #open and read the log file
        logs = file.readlines() #read all lines into a list
    for log_entry in logs:
        log_entry = log_entry.strip() #re;ove whitespace/newline characters
        if 'attack' in log_entry.lower() or "suspicious" in log_entry.lower(): #Enhanced anamaly check
            print(f'Alert: suspicious activity detected in log: {log_entry}')
        else: 
            print(f'Log processed: {log_entry}')
except FileNotFoundError:
    print('Error: logs.txt not found. Please create it.')
if __name__ == '__main__':
    main()