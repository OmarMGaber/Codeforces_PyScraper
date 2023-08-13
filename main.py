from bs4 import BeautifulSoup
import re
import requests

# url = "https://codeforces.com/contest/1822/submission/218624330"
url = "https://codeforces.com/submissions/OmarMGaber"
result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")
submissions = doc.find_all('tr', partymemberids=True)
links = doc.find_all('a', href=re.compile(r'^/contest.*problem'))

submissions_list = []

for i in submissions:
    cleaned_text = i.text.splitlines()
    cleaned_text = [item.replace('\xa0', ' ').strip() for item in cleaned_text if item.strip() != ""]
    cleaned_text[4] = cleaned_text[4].lower()

    if cleaned_text[4].__contains__("c++"):
        cleaned_text[4] = ".cpp"
    elif cleaned_text[4].__contains__("clang"):
        cleaned_text[4] = ".c"
    elif cleaned_text[4].__contains__("java"):
        cleaned_text[4] = ".java"
    elif cleaned_text[4].__contains__("javascript"):
        cleaned_text[4] = ".js"
    elif cleaned_text[4].__contains__("pypy"):
        cleaned_text[4] = ".py"
    elif cleaned_text[4].__contains__("python"):
        cleaned_text[4] = ".py"
    elif cleaned_text[4].__contains__("c#"):
        cleaned_text[4] = ".cs"
    else:
        cleaned_text[4] = ".txt"

    submissions_list.append(cleaned_text)

problems_map = {}

for link in links:
    href = link['href']
    name = link.get_text(strip=True)

    match = re.search(r'/contest/(\d+)/problem', href)
    if match:
        contest_number = match.group(1)
        problems_map[name] = contest_number

for i in submissions_list:
    try:
        f = open(i[3] + i[4], "w")
        url = "https://codeforces.com/contest/" + problems_map[i[3]] + "/submission/" + i[0]
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        code = doc.find(class_="linenums")
        code_text = code.get_text(strip=True)
        f.write(code_text)
        f.close()
    except:
        print("An error occurred")
        print("problem: " + i[3] + " couldn't load")