import requests
from bs4 import BeautifulSoup
import sys

# Check if the script received the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: ./read_problem.py <problem_number>")
    sys.exit(1)

# Get the problem number from command line arguments
problem_number = sys.argv[1]

# URL setting
url = f'https://www.acmicpc.net/problem/{problem_number}'

# Set HTTP GET request headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send HTTP GET request
response = requests.get(url, headers=headers)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Extract problem title and description
title = soup.find('span', id='problem_title').text
description = soup.find('div', id='problem_description').text
input_spec = soup.find('div', id='problem_input').text
output_spec = soup.find('div', id='problem_output').text

# Extract example input and output
examples = soup.find_all('pre')
example_input = examples[0].text if len(examples) > 0 else "No example input found"
example_output = examples[1].text if len(examples) > 1 else "No example output found"

with open('input.txt', 'w', encoding='utf-8') as file:
    file.write(example_input.strip())

with open('output.txt', 'w', encoding='utf-8') as file:
    file.write(example_output.strip())

# Save the information to a local text file
filename = f'{problem_number}.cpp'
with open(filename, 'a', encoding='utf-8') as file:
    file.write(f"/* Title: {title}\n\n")
    file.write("Description:\n")
    file.write(description.strip() + "\n\n")
    file.write("Input Specification:\n")
    file.write(input_spec.strip() + "\n\n")
    file.write("Output Specification:\n")
    file.write(output_spec.strip() + "\n*/")

print(f"Problem information has been saved to {filename}")
