# 📈 DataScraperViz

**DataScraperViz** is a Python-based project that scrapes and analyzes real-time stock market data and job listings from LinkedIn. It provides rich visual insights using both static and interactive visualizations.

Built with data science tools like **yFinance**, **Selenium**, **Matplotlib**, **Seaborn**, and **Plotly**, this suite serves as a practical demonstration of web scraping, data cleaning, and data visualization.

---

## 🚀 Features

### 🧾 Stock Market Scraper
- Scrapes real-time data using `Alpha Vantage`
- Extracts financial indicators like:
  - Company name
  - Stock price
  - Market cap
  - Volume
  - P/E Ratio
- Saves output to a structured CSV

### 📊 Data Visualization
- Uses `Matplotlib`, `Seaborn`, and `Plotly`
- Generates:
  - 📌 Market cap distribution by sector
  - 📌 Top 10 companies by market cap
  - 📌 Stock price vs trading volume (interactive)
  - 📌 PE ratio distribution by sector

### 💼 LinkedIn Job Scraper
- Automates job search on LinkedIn using `Selenium`
- Searches for roles like *Data Scientist*, *AI Engineer*, and *Full-Stack Developer* across countries
- Extracts:
  - Job title
  - Company name
  - Location
  - Job link
- Saves job data to CSV

---

## 🗂 Directory Structure

```
DataScraperViz/
│
├── Stocks_scraper.py         # Scrapes stock data
├── visulize_data.py          # Generates plots and visualizations
├── Job_scraper.py            # Automates job search and scraping
├── requirements.txt          # Dependencies
├── README.md                 # You're here!
├── data/                     # (Optional) CSV and screenshot output folder
└── outputs/                  # PNG/HTML visualizations
```

---

## 🛠 Requirements

Install all required libraries with:

```bash
pip install -r requirements.txt
```

OR use `pipreqs` to generate it:

```bash
pipreqs . --force
```

Main dependencies:
- `Alpha Vantage`
- `pandas`
- `matplotlib`
- `seaborn`
- `plotly`
- `selenium`

---

## 🔐 Security Warning

> ⚠️ Never upload your personal LinkedIn credentials to a public repo!  
Use a `.env` file or config manager instead.

---

## 💡 Use Cases

- Resume project to demonstrate scraping + data viz skills
- Academic portfolio for Data Science / AI internships
- Financial & market research exploration
- Career trend analysis across job roles

---

## 📸 Screenshots
![image](https://github.com/user-attachments/assets/e2760168-b886-4f4d-9877-53b1ad6ec722)



---

## ✍️ Author

**Aditya Tawde**  
B.Tech in AI & Data Science  
Jawaharlal Nehru Engineering College, MGMU  
[GitHub](https://github.com/adityatawde9699) • [LinkedIn](https://www.linkedin.com/in/aditya-s-tawde-7a1392315?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BiJCrjr%2FTQJWM6iTXo52upQ%3D%3D)

---

## 📌 License

This project is open source and available under the [MIT License](LICENSE).
