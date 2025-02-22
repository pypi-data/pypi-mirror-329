# changed to fit with ui instead of as standalone prgrm
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()
    return logs

def filter_logs(logs, websites, ip_address):
    access_counts = {website: [0] * 24 for website in websites}

    for line in logs:
        parts = line.strip().split('|')
        if len(parts) < 3:
            continue

        timestamp_str, client_ip, domain = parts[0], parts[1], parts[2]
        if client_ip != ip_address:
            continue

        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

        for website in websites:
            if domain.endswith(website):
                hour = timestamp.hour
                access_counts[website][hour] += 1

    return access_counts

def plot_combined_access_data(access_counts):
    plt.figure(figsize=(14, 8))
    hours = np.arange(24)  # Each hour of the day

    bar_width = 0.25  
    num_websites = len(access_counts)
    colors = plt.cm.tab10.colors  # Use a color map for distinct bar colors

    # Plot bar graphs for each website
    for i, (website, counts) in enumerate(access_counts.items()):
        plt.bar(
            hours + i * bar_width,  # Offset each website's bars
            counts,
            width=bar_width,
            label=website,
            color=colors[i % len(colors)]  # Cycle through colors
        )

    # Format the graph
    plt.xlabel("Hour")
    plt.ylabel("Visits")
    plt.title("Visits per Hour (Bar Graph)")
    plt.xticks(hours + bar_width * (num_websites - 1) / 2, hours)  
    plt.legend()
    plt.grid(visible=True, linestyle="--", alpha=0.6)

    return plt
