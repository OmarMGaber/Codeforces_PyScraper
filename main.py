from datetime import datetime

from bs4 import BeautifulSoup
import re
import requests


def menu():
    global handle
    global should_get_status
    should_get_status = False
    handle = input("Enter your Codeforces Handle: ")
    while True:
        user_input = input("Do you want to get a .txt file for your submissions details? (Y/N): ").lower()
        if user_input == "y":
            should_get_status = True
            break
        elif user_input == "n":
            should_get_status = False
            break
        else:
            print("Invalid input. Please enter a valid boolean value.")


def set_file_extension(compiler):
    if compiler.__contains__("c++"):
        return ".cpp"
    elif compiler.__contains__("clang"):
        return ".c"
    elif compiler.__contains__("java"):
        return ".java"
    elif compiler.__contains__("javascript"):
        return ".js"
    elif compiler.__contains__("pypy"):
        return ".py"
    elif compiler.__contains__("python"):
        return ".py"
    elif compiler.__contains__("c#"):
        return ".cs"
    else:
        return ".txt"


def get_statues(doc):
    submissions = doc.find_all('tr', partymemberids=True)
    global submissions_list
    submissions_list = []

    for i in submissions:
        cleaned_text = i.text.splitlines()
        cleaned_text = [item.replace('\xa0', ' ').strip() for item in cleaned_text if item.strip() != ""]
        submissions_list.append(cleaned_text)


def get_problems_map(doc):
    links = doc.find_all('a', href=re.compile(r'^/contest.*problem'))

    global problems_map
    problems_map = {}
    print("requesting problems")
    for link in links:
        # print(link)
        href = link['href']
        name = link.get_text(strip=True)
        match = re.search(r'/contest/(\d+)/problem', href)
        if match:
            contest_number = match.group(1)
            problems_map[name] = contest_number


def get_max_page_index(url):
    try:
        res = requests.get(url)
        if res.status_code != 200:
            print("Failed to scrap the data.")
            return -1

        doc = BeautifulSoup(res.text, "html.parser")
        page_index = doc.find_all("span", class_="page-index")

        if len(page_index) > 0:
            if str(page_index[0]).__contains__("submissions"):
                return page_index[len(page_index) - 1].text
            else:
                print("The entered handle doesn't have any public submission or doesn't exist.")
                return -1
        else:
            print("The entered handle doesn't have any public submission or doesn't exist.")
            return -1
    except:
        print("An error occurred while scraping submissions page index.")
        return -1


def write_submissions():
    with open("submissions_status.txt", "a") as file:
        for submission in submissions_list:
            formatted_submission = [
                f"{submission[0]:<15}",
                f"{submission[1]:<20}",
                f"{submission[2]:<15}",
                f"{submission[3]:<45}",
                f"{submission[4]:<25}",
                f"{submission[5]:<35}",
                f"{submission[6]:<15}",
                f"{submission[7]:<15}"
            ]
            formatted_line = "\t".join(formatted_submission) + "\n"
            file.write(formatted_line)


def main():
    menu()
    url = "https://codeforces.com/submissions/" + handle + "/page/1"
    max_page_index = int(get_max_page_index(url)) + 1

    if should_get_status:
        with open("submissions_status.txt", "a") as file:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write("Data fetched at: " + current_time + '\n')

    for i in range(1, max_page_index, 1):
        url = "https://codeforces.com/submissions/" + handle + "/page/" + str(i)

        result = requests.get(url)
        if result.status_code != 200:
            print("Failed to scrap the data at page no." + str(i))
            return
        doc = BeautifulSoup(result.text, "html.parser")

        get_statues(doc)
        if should_get_status:
            write_submissions()

        # get_problems_map(doc)


if __name__ == "__main__":
    main()

#
# links = doc.find_all('a', href=re.compile(r'^/contest.*problem'))
#
# problems_map = {}
#
# for link in links:
#     print(link)
#     href = link['href']
#     name = link.get_text(strip=True)
#
#     match = re.search(r'/contest/(\d+)/problem', href)
#     if match:
#         contest_number = match.group(1)
#         problems_map[name] = contest_number

# for i in submissions_list:
#     try:
#         f = open(i[3] + i[4], "w")
#         url = "https://codeforces.com/contest/" + problems_map[i[3]] + "/submission/" + i[0]
#         result = requests.get(url)
#         doc = BeautifulSoup(result.text, "html.parser")
#         code = doc.find(class_="linenums")
#         code_text = code.get_text(strip=True)
#         f.write(code_text)
#         f.close()
#     except:
#         print("An error occurred")
#         print("problem: " + i[3] + " couldn't load")
