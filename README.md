🍱 Corporate Food Matrix

A Flask-based Corporate Food Management System that allows employees to request meals, HR to approve requests, and Admin to manage food distribution with reporting and menu upload features.

🚀 Features
👨‍💼 Employee Panel
Login system
Request meals (daily or subscription)
Select meal date / range
View weekly menu uploaded by admin
Submit food requests easily
🧑‍💼 HR Panel
View all employee requests
Approve meal requests
Track pending/approved requests
Dashboard with statistics
🧑‍💻 Admin Panel
Full control over system
Mark meals as served
Upload weekly menu image
View all requests
Export data to Excel report
Dashboard analytics
🖼️ Weekly Menu Feature
Admin can upload weekly menu image
Automatically visible to HR & Employees
Stored securely in database + static folder
📊 Export Feature
Download complete request data as Excel file
Helps HR/Admin for reporting and records
🛠️ Tech Stack
Backend: Flask (Python)
Database: SQLite
Frontend: HTML, CSS (Jinja Templates)
Data Processing: Pandas
File Handling: Werkzeug
📁 Project Structure
food-matrix/
│
├── app.py
├── food.db (ignored in git)
├── static/
│   ├── style.css
│   └── uploads/
│
├── templates/
│   ├── login.html
│   ├── employee.html
│   ├── hr.html
│   └── admin.html
│
├── food_report.xlsx (ignored in git)
└── .gitignore
⚙️ Installation & Setup
1. Clone repo
git clone https://github.com/Vinayakgarg2/Corporate-food-matrix.git
2. Move into folder
cd Corporate-food-matrix
3. Install dependencies
pip install flask pandas openpyxl
4. Run project
python app.py
5. Open browser
http://127.0.0.1:5000
🔐 Default Login Credentials
Employee
username: vinayak
password: 1234
HR
username: hr1
password: 1234
Admin
username: admin1
password: 1234
📌 Key Modules
Authentication System (Role-based login)
Meal Request Management
HR Approval System
Admin Control Panel
Weekly Menu Upload System
Excel Reporting System
📤 Export Data

Admin can export all requests into Excel:

/export
⚠️ Notes
food.db and food_report.xlsx are ignored in GitHub
Upload folder is auto-managed
This project runs in development mode (Flask debug server)
🚀 Future Improvements
Live database (MySQL/PostgreSQL)
Email notifications
Employee auto-fetch from company directory
Calendar-based meal scheduling
Mobile responsive UI upgrade
👨‍💻 Author

Vinayak Garg
GitHub: Vinayakgarg2
