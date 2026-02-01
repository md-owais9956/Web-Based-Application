# Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop)
 A robust hybrid application designed to visualize and analyze chemical equipment data. This project features a unified Django **REST** **API** backend serving both a React.js web application and a PyQt5 desktop client.

### Project Architecture

The system follows a *Single Source of Truth* architecture:

Backend: Python Django + Django **REST** Framework (**DRF**)

Data Engine: Pandas for **CSV** parsing and statistical analytics

Web Frontend: React.js with Chart.js for visualization

Desktop Frontend: PyQt5 with Matplotlib integration

Reporting: ReportLab for automated **PDF** generation

### Folder Structure
```text
chemical_project/ 
    ├── backend/ # Django **API** & AnalyticsEngine 
    ├── frontend_web/ # React.js Web Application 
    ├── frontend_desktop/ # PyQt5 Desktop Application 
    ├── sample_data.csv # Sample **CSV** for testing 
    └── requirements.txt # Python dependencies
```
# Setup & Installation
 ## Prerequisites Python: 3.12+ (Tested on version 3.12.6)

Node.js: Latest stable version & npm

## Backend Setup 

Open your terminal in the `backend` folder:

Create a virtual environment: `python -m venv venv`

Activate it:

`Windows: venv\Scripts\activate`

`Mac/Linux: source venv/bin/activate`

Install libraries: `pip install -r requirements.txt`

Set up database: `python manage.py migrate`
Start server:
`python manage.py runserver`

## Web Frontend Setup

Open a new terminal in the frontend_web folder:

Install tools:`npm install`

Start website: `npm start`


Access via: [http://localhost:**3000**](http://localhost:**3000**)

## Desktop Frontend Setup

Open a new terminal in the `frontend_desktop` folder:

Install tools: `pip install PyQt5 requests matplotlib`

Start app:` python main.py`

### Key Features

**CSV** Data Processing: Upload equipment lists and receive instant averages for Pressure, Flowrate, and type distribution.

Hybrid Visualization: Unified charts using `Chart.js` (Web) and Matplotlib (Desktop).

History Tracking: The **API** stores and displays the last 5 uploaded datasets.

Automated Reporting: One-click **PDF** generation for equipment summaries.



### Sample Data Format

The application expects a **CSV** with the following columns: Equipment Name, Type, Flowrate, Pressure, Temperature

### Developer Information

Name: Mohd Owais

Education: B.Tech Computer Science , **VIT** Bhopal

email : md.owais111234@gmail.com

