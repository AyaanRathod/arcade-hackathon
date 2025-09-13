# 🎓 StudyBalance AI - Arcade Hackathon Submission

> **AI-Powered Student Burnout Prevention System using Arcade.dev Toolkits**

StudyBalance AI is an intelligent web application that helps students prevent burnout by analyzing their email patterns, optimizing study schedules, and sending personalized wellness nudges - all powered by **Arcade.dev Gmail and Google Calendar toolkits**.

![StudyBalance AI Dashboard](https://img.shields.io/badge/Status-Ready%20for%20Demo-brightgreen)
![Arcade.dev Integration](https://img.shields.io/badge/Arcade.dev-Integrated-blue)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)

## 🌟 Features

### 🔍 **Gmail Pattern Analysis** (via Arcade.dev Gmail Toolkit)
- **Real-time email analysis** using Arcade.dev Gmail API
- **Stress keyword detection** (urgent, deadline, ASAP, etc.)
- **Workload assessment** based on email volume and content
- **Peak hour identification** to optimize email checking
- **Burnout risk calculation** with personalized recommendations

### 📅 **Smart Schedule Optimization** (via Arcade.dev Google Calendar Toolkit)
- **AI-powered study block creation** using real calendar data
- **Conflict-free scheduling** by checking existing events
- **Cognitive load balancing** with optimal break timing
- **Subject difficulty ordering** for maximum efficiency
- **Wellness score calculation** for schedule quality

### 💚 **Wellness Nudging System** (via Arcade.dev Gmail Toolkit)
- **Automated wellness emails** sent through Gmail
- **Personalized break reminders** based on study intensity
- **Hydration and posture check-ins** at optimal intervals
- **Motivational achievement messages** to boost morale
- **Stress relief techniques** delivered at the right time

## 🛠️ Technology Stack

- **Backend**: Python 3.11+ with Flask 2.3.3
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Arcade.dev Integration**: 
  - `arcadepy` SDK for toolkit access
  - Gmail toolkit for email analysis and wellness emails
  - Google Calendar toolkit for schedule optimization
- **Charts**: Chart.js for data visualization
- **Authentication**: Arcade.dev OAuth flow
- **Environment**: dotenv for configuration management

## 🚀 Arcade.dev Integration

This project showcases the power of **Arcade.dev toolkits** for real-world applications:

### 📧 Gmail Toolkit Usage
```python
# Real email analysis
emails_response = self.client.tools.execute(
    tool_name="Gmail.ListEmails",
    input={"n_emails": 50},
    user_id=self.user_id
)

# Send wellness emails
email_response = self.client.tools.execute(
    tool_name="Gmail.SendEmail",
    input={
        "to": user_email,
        "subject": reminder_content['subject'],
        "body": reminder_content['body']
    },
    user_id=self.user_id
)
```

### 📅 Google Calendar Toolkit Usage
```python
# Get calendar events for conflict detection
events_response = self.client.tools.execute(
    tool_name="GoogleCalendar.ListEvents",
    input={
        "min_end_datetime": f"{today}T00:00:00",
        "max_start_datetime": f"{tomorrow}T23:59:59",
        "calendar_id": "primary"
    },
    user_id=self.user_id
)
```

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Arcade.dev account and API credentials
- Gmail and Google Calendar access

### 1. Clone the Repository
```bash
git clone https://github.com/AyaanRathod/arcade-hackathon.git
cd arcade-hackathon
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements_simple.txt
```

### 4. Configure Arcade.dev Credentials
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials:
ARCADE_API_KEY=your_arcade_api_key_here
ARCADE_USER_ID=your_arcade_user_id_here
```

**Get your credentials from**: https://api.arcade.dev/dashboard

### 5. Run the Application
```bash
python app.py
```

Visit: http://localhost:5000

## 🔐 OAuth Authentication Flow

StudyBalance AI uses Arcade.dev's OAuth system for secure Gmail and Calendar access:

1. **First Analysis**: Click "Start Analysis" → OAuth popup appears
2. **Grant Permissions**: Authorize Gmail access through Google OAuth
3. **Automatic Integration**: Future requests use authorized access
4. **Privacy Protected**: Only you control your data access

## 📊 Demo Workflow

### Step 1: Gmail Analysis
1. Navigate to `/analyze`
2. Click "Start Analysis"
3. Authorize Gmail access (first time only)
4. View real email stress patterns and workload assessment

### Step 2: Schedule Optimization
1. Navigate to `/schedule`
2. Set preferences (study duration, subjects, time range)
3. Generate AI-optimized schedule using real calendar data
4. Get wellness-focused study blocks with perfect break timing

### Step 3: Wellness Nudging
1. Navigate to `/wellness`
2. Configure reminder preferences
3. Receive personalized wellness emails automatically
4. Track improvement in study-life balance

## 🎯 Key Achievements

- ✅ **Real Gmail Integration**: Actual email analysis using Arcade.dev
- ✅ **Calendar Conflict Detection**: Smart scheduling with real Google Calendar data
- ✅ **Automated Email Sending**: Wellness nudges via Gmail toolkit
- ✅ **OAuth Flow**: Secure authentication through Arcade.dev
- ✅ **Production Ready**: Error handling, fallbacks, and user guidance
- ✅ **Privacy Focused**: User-controlled data access

## 🏗️ Project Structure

```
StudyBalance-AI/
├── app.py                 # Main Flask application
├── configs.py             # Configuration settings
├── utils.py              # Utility functions
├── requirements_simple.txt # Dependencies
├── .env.example          # Environment template
│
├── arcade_tools/         # Arcade.dev toolkit integrations
│   ├── gmail_analyzer.py    # Gmail pattern analysis
│   ├── calendar_optmizer.py # Schedule optimization
│   └── wellness_nudger.py   # Wellness email system
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── analyze.html
│   ├── schedule.html
│   └── wellness.html
│
└── static/               # Frontend assets
    ├── css/styles.css
    ├── js/main.js
    └── sw.js
```

## 🤝 Contributing

This project was built for the **Arcade.dev Hackathon** to demonstrate real-world toolkit integration. Contributions are welcome!

## 📧 Contact

**Developer**: AyaanRathod  
**Email**: ayaanrathod466@gmail.com  
**Hackathon**: Arcade.dev Integration Challenge

## 🏆 Hackathon Submission

This project demonstrates:
- **Practical Arcade.dev Usage**: Real Gmail and Calendar integration
- **User-Centric Design**: Solving actual student burnout problems
- **Technical Excellence**: Production-ready code with proper error handling
- **Innovation**: AI-powered wellness through email pattern analysis

---

*Built with ❤️ for the Arcade.dev Hackathon*
