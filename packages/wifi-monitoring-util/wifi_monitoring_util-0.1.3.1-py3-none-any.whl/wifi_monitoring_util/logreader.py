from wifi_monitoring_util.log import log_file_path
import csv
from datetime import datetime

def read_ftl_log(fpath):
    client_read_ip = "192.168.0.137"
    visits_times = {}

    exclude_subdomains = [
        "p16-sign-sg.tiktokcdn.com",
        "p16-sign-useast2a.tiktokcdn.com",
        "p16-tiktokcdn.com",
        "im-api.tiktok.com",
        "api2.musical.ly",
        "api.tiktok.com",
        "analytics.tiktok.com",
        "analytics.tiktokv.com",
        "ads.tiktok.com",
        "tiktok-ads.com",
        "v16-webapp-prime.us.tiktok.com",
        "im-ws.tiktok.com",
    ]

    try:
        with open(fpath, 'r') as file:
            for line in file:
                log_parts = [part.strip() for part in line.split('|')]
                if len(log_parts) == 3:
                    timestamp, client_ip, domain = log_parts
                    if client_ip == client_read_ip and not any(sub in domain for sub in exclude_subdomains):
                        visits_times[timestamp] = domain
                else:
                    print(f"Bad entry: {line.strip()}")
    except FileNotFoundError:
        print(f"File {fpath} not found.")
    return visits_times

def get_concern_level(hour):
    if 22 <= hour or hour < 3: 
        return "Most Concern"
    elif 3 <= hour < 8:
        return "Medium Concern"
    else:
        return "Least Concern"

def read_visits_times(visits_dict):
    websites = {"instagram.com", "tiktok.com", "twitch.tv"}
    results = []

    for timestamp, domain in visits_dict.items():
        visit_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        concern_level = get_concern_level(visit_time.hour)
        if any(site in domain for site in websites):
            results.append((domain, visit_time.strftime('%I:%M %p'), concern_level))
    return results
"""
# save it to a csv file if needed
def save_to_csv(results, output_path):

    headers = ["Domain", "Visit Time", "Concern Level"]
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers) 
            writer.writerows(results) 
        print(f"Data written to {output_path}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")
"""

searched_visits = read_visits_times(read_ftl_log(log_file_path))






