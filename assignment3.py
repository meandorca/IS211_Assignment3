import argparse
import urllib.request
import csv
import re
from datetime import datetime

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    filename = "weblog.csv"

    urllib.request.urlretrieve(args.url, filename)

    total_requests = 0
    image_requests = 0

    browser_counts = {
        "Firefox": 0,
        "Chrome": 0,
        "Internet Explorer": 0,
        "Safari": 0
    }

    hour_counts = {i: 0 for i in range(24)}

    image_pattern = re.compile(r'\.(jpg|gif|png)$', re.IGNORECASE)

    with open(filename, newline='') as file:
        reader = csv.reader(file)

        for row in reader:

            total_requests += 1

            path = row[0]
            agent = row[2]
            dt = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")

            if image_pattern.search(path):
                image_requests += 1

            # REGEX browser detection
            if re.search(r'Firefox', agent, re.IGNORECASE):
                browser_counts["Firefox"] += 1
            elif re.search(r'Chrome', agent, re.IGNORECASE):
                browser_counts["Chrome"] += 1
            elif re.search(r'MSIE|Trident', agent, re.IGNORECASE):
                browser_counts["Internet Explorer"] += 1
            elif re.search(r'Safari', agent, re.IGNORECASE):
                browser_counts["Safari"] += 1

            hour_counts[dt.hour] += 1

    percentage = (image_requests / total_requests) * 100
    print(f"Image requests account for {percentage:.1f}% of all requests")

    most_popular = max(browser_counts, key=browser_counts.get)
    print(f"The most popular browser is {most_popular}")

    sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)

    for hour, count in sorted_hours:
        print(f"Hour {hour:02d} has {count} hits")

if __name__ == "__main__":
    main()
