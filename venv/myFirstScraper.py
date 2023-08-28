import requests
from bs4 import BeautifulSoup

# Link to tutorial: https://realpython.com/beautiful-soup-web-scraper-python/

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
job_elements = results.find_all("div", class_="card-content")

# each job object is a BeautifulSoup() object
# for job_element in job_elements:
#     title_element = job_element.find("h2", class_="title")
#     company_element = job_element.find("h3", class_="company")
#     location_element = job_element.find("p", class_="location")
#     print(title_element.text.strip())
#     print(company_element.text.strip())
#     print(location_element.text.strip())
#     print()

# not all job listings are developer jobs, filter using keyword "Python"
# you can pass functions as arguments to Beautiful Soup methods
# lambda function looks at text of each <h2> element, converts it to lowercase, and checks whether substring "python" is found
python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower()
)

# for job_element in python_jobs:
    # title_element = job_element.find("h2", class_="title")
    # company_element = job_element.find("h3", class_="company")
    # location_element = job_element.find("p", class_="location")
    # print(title_element.text.strip())
    # print(company_element.text.strip())
    # print(location_element.text.strip())
    # print(job_element.text)

    # AttributeError: 'NoneType' object has no attribute 'text'


# BeautifulSoup can help to select sibling, child, and parent elements of BeautifulSoup object
python_job_elements = [
    h2_element.parent.parent.parent for h2_element in python_jobs
]

for job_element in python_job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    links = job_element.find_all("a", string="Apply")
    for link in links:
        link_url = link["href"]
        # link_url = job_element.find_all("a")[1]["href"] to grap 2nd link from results 
        print(f"Apply here: {link_url}\n")