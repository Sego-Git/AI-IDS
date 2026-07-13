# main function for AI-IDS project
def main():
    print('AI-IDS journey begins!')

#Load and read logs from a file
def read_logs(file_name):
    with open(file_name, 'r') as file:
        logs = file.readlines()
    return logs

logs= read_logs('logs.txt')
suspicious_keywords = ['attack', 'suspicious', 'malware', 'intrusion', 'breach', 'failed password']


for log_entry in logs:
    #Clean the line 
    log_entry = log_entry.strip() #removes extra space or newline characters
    if any(keyword in log_entry.lower() for keyword in suspicious_keywords):
        print(f'Potential threat detected: {log_entry}')
    else:
        print(f'Normal log entry: {log_entry}')


    
    
    
    