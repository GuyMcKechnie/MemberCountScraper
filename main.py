import os
import subprocess
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# URL of the WhatsApp channel invite page
url = 'https://whatsapp.com/channel/0029VaHkSUX2P59srKXDBa0H'

# Send a request to fetch the webpage content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element that contains the member count (you'll need to inspect the webpage to find the right element)
    # For example, if the member count is inside a span with a certain class, it could be something like this:
    # Modify with the correct class
    member_count_element = soup.find('h5', class_='_9vd5 _9scy')

    if member_count_element:
        member_count = member_count_element.text.split('|')[1].strip()
        # member_count = "Channel | 8.3K followers"
        member_count = member_count.split('|')[1].strip()
        member_count = member_count.split(' ')[0].strip()
        if 'K' in member_count:
            member_count = float(member_count.replace('K', '')) * 1000
        elif 'M' in member_count:
            member_count = float(member_count.replace('M', '')) * 1000000
        print(f'Member count: {int(member_count)}')
    else:
        print('Member count not found.')
else:
    print(f'Failed to retrieve page. Status code: {response.status_code}')

# get the difference in days since January 27 2024 and current day

reference_date = datetime(2024, 1, 27)
current_date = datetime.now()
difference_in_days = (current_date - reference_date).days
print(f'Difference in days: {difference_in_days}')

# index html file path
index_path = "C:/Users/mckec/OneDrive/Coding/TheBibleApp.github.io/index.html"
# open the file in read mode
with open(index_path, 'r') as file:
    # read the content of the file
    lines = file.readlines()

# find the y list and add the member count to it
y_values = []
in_y_list = False
for i, line in enumerate(lines):
    if 'y: [' in line:
        in_y_list = True
    elif in_y_list:
        if ']' in line:
            in_y_list = False
            lines[i-1] = lines[i-1].strip() + str(int(member_count)) + ',\n'
            lines[i] = '                ],\n'
            break
    else:
        y_values.extend(line.strip().replace(',', '').split())

# find the x list and add the days since January 27 to it
x_values = []
in_x_list = False
for i, line in enumerate(lines):
    if 'x: [' in line:
        in_x_list = True
    elif in_x_list:
        if '],' in line:
            in_x_list = False
            lines[i-1] = lines[i-1].strip() + str(difference_in_days) + ',\n'
            lines[i] = '                ],\n'
            break
        else:
            x_values.extend(line.strip().replace(',', '').split())

# write to file
# open the file in write mode
with open(index_path, 'w') as file:
    file.writelines(lines)

os.chdir('C:/Users/mckec/OneDrive/Coding/TheBibleApp.github.io/')
# Add the updated file to the git staging area
subprocess.run(['git', 'add', index_path])
# Commit the changes with a meaningful commit message
commit_message = f"Update member count and days since January 27 to {
    member_count} and {difference_in_days} respectively"
subprocess.run(['git', 'commit', '-m', commit_message])
# Push the changes to the GitHub repo
subprocess.run(
    ['git', 'push', 'https://github.com/GuyMcKechnie/TheBibleApp.github.io.git', 'master'])

root = tk.Tk()
root.withdraw()
messagebox.showinfo(
    "Success", "Member count and difference in days have been successfully updated in the index.html file.")
