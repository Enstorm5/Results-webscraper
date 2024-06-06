import requests
from bs4 import BeautifulSoup
import time
from tabulate import tabulate

def fetch_data():
    url = "https://www.nibmworldwide.com/exams/mis"

    with requests.Session() as session:
        response = session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            programme_dropdown = soup.find('select', {'name': 'F[Programme]'})
            if programme_dropdown:
                options = programme_dropdown.find_all('option')
                programme_value = None
                for option in options:
                    if option.text.strip() == 'Diploma in Software Engineering':
                        programme_value = option['value']
                        break

                if programme_value:
                    payload = {
                        'F[Programme]': programme_value,
                        'Submit': 'Submit'
                    }

                    response = session.post(url, data=payload)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        batch_dropdown = soup.find('select', {'name': 'F[Batch]'})
                        if batch_dropdown:
                            options = batch_dropdown.find_all('option')
                            batch_value = None
                            for option in options:
                                if option.text.strip() == 'DSE22.3F/CO':
                                    batch_value = option['value']
                                    break

                            if batch_value:
                                payload['F[Batch]'] = batch_value
                                response = session.post(url, data=payload)
                                if response.status_code == 200:
                                    soup = BeautifulSoup(response.content, 'html.parser')
                                    student_dropdown = soup.find('select', {'name': 'F[Student]'})
                                    if student_dropdown:
                                        options = student_dropdown.find_all('option')
                                        student_value = None
                                        for option in options:
                                            if option.text.strip() == 'CODSE223F-140':
                                                student_value = option['value']
                                                break

                                        if student_value:
                                            payload['F[Student]'] = student_value
                                            response = session.post(url, data=payload)
                                            if response.status_code == 200:
                                                time.sleep(5)
                                                soup = BeautifulSoup(response.content, 'html.parser')
                                                table_data = []
                                                tbody = soup.find('tbody')
                                                if tbody:
                                                    tr_elements = tbody.find_all('tr')
                                                    for tr in tr_elements:
                                                        row_data = []
                                                        td_elements = tr.find_all('td')
                                                        for td in td_elements:
                                                            row_data.append(td.get_text(strip=True))
                                                        table_data.append(row_data)

                                                    column_headers = ["No", "Exam", "Special", "Date", "CW", "Exam", "Final Grade", "Points"]
                                                    print(tabulate(table_data, headers=column_headers))
                                                else:
                                                    print("Couldn't find the table body.")
                                            else:
                                                print("Couldn't get data after selecting student. Status code:", response.status_code)
                                        else:
                                            print("Couldn't find the right student.")
                                    else:
                                        print("Couldn't find the student dropdown.")
                                else:
                                    print("Couldn't get data after selecting batch. Status code:", response.status_code)
                            else:
                                print("Couldn't find the right batch.")
                        else:
                            print("Couldn't find the batch dropdown.")
                    else:
                        print("Couldn't get data after selecting programme. Status code:", response.status_code)
                else:
                    print("Couldn't find the right programme.")
            else:
                print("Couldn't find the programme dropdown.")
        else:
            print("Couldn't fetch the initial data. Status code:", response.status_code)

        input("Press Enter to exit...")

if __name__ == "__main__":
    fetch_data()
