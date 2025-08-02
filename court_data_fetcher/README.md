#Court Data Fetcher & Dashboard

This is a mini web application built using Flask, Python, HTML, and MySQL that allows users to search for Indian court case data by providing case type, case number, and year. It scrapes metadata and displays orders or judgments from selected Indian court websites (e.g., Faridabad District Court) 


#Features

- Form-based input for case details  
- Backend web scraping (Selenium + BeautifulSoup)  
- Displays case metadata and latest orders  
- Stores query history in a MySQL database  
- Clean UI using HTML templates

#Tech Stack
- Python 3.x
- Flask
- Selenium
- BeautifulSoup (bs4)
- MySQL
- HTML/CSS

# How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/court_data_fetcher.git
   cd court_data_fetcher
   ```

2. Install dependencies:
   pip install -r requirements.txt
Setup MySQL database:
   - Create a database called `court_data`
   - Import schema (optional)
   - Update DB credentials in `app.py`

4. Run the Flask app:
   -python app.py

5. Open in browser:
   -http://127.0.0.1:5000


#Folder Structure

court_data_fetcher/
│
├── app.py
├── scraper.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── result.html


#Author

Made by Umesh More
