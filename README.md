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

#Screenshots 
<img width="1471" height="282" alt="image" src="https://github.com/user-attachments/assets/ceb71dec-1add-442e-81ce-6afb375da993" />
<img width="1917" height="582" alt="image" src="https://github.com/user-attachments/assets/3698a42a-a470-44bc-9fb2-652e62d05e06" />
<img width="1918" height="600" alt="image" src="https://github.com/user-attachments/assets/5ed3bbf5-3cf4-4e22-b685-40b9acab7411" />
<img width="1918" height="522" alt="image" src="https://github.com/user-attachments/assets/307727d7-5fce-4004-9c2b-08761409adc7" />

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
