# 🎓 Student Productivity Planner

A full-stack web application for students to manage tasks with **2-Factor Authentication (2FA)** using email OTP verification.

![Project Banner](images\dashboard.png)

## ✨ Features

- 🔐 **Email-based 2FA** - Secure login with OTP verification
- ✅ **Task Management** - Create, update, delete tasks
- 📊 **Dashboard** - Track pending and completed tasks
- 🌓 **Dark Mode** - Eye-friendly interface
- 📱 **Responsive Design** - Works on all devices
- 🔒 **JWT Authentication** - Secure API access

## 🛠️ Tech Stack

**Frontend:**

- React 18
- Tailwind CSS
- React Router
- Axios
- GSAP (animations)

**Backend:**

- Django 6.0
- Django REST Framework
- JWT Authentication
- SQLite Database
- Email Integration (Gmail SMTP)

## 📦 Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Backend Setup

```bash
# Clone repository
git clone https://github.com/yashika-salonia/Student-Planner.git
cd student-planner/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Mac/iOS: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your email credentials

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Frontend Setup

```bash
# In new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔑 Environment Variables

Create `backend/.env` file:

```bash
SECRET_KEY=your-django-secret-key
DEBUG=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Get Gmail App Password:**

1. Enable 2-Step Verification in your Google Account
2. Go to Security → App Passwords
3. Generate password for "Mail"
4. Copy 16-character password (visible only once)

## 🚀 Usage

1. **Register:** Create account with email
2. **Verify Email:** Click link in email
3. **Login:** Enter username + password
4. **OTP:** Check email for 6-digit code
5. **Dashboard:** Manage your tasks

## 📸 Screenshots

![Login Page](images\login.png)
![Register Page](images\register.png)
![Dashboard](images\dashboard-1.png)
![Dashboard](images\dashboard-2.png)

## 🔐 Security Features

- Two-Factor Authentication (2FA)
- Email verification before login
- JWT token-based authentication
- Time-limited OTP (5 minutes)
- Password hashing
- CORS protection

## 📝 API Endpoints

```
POST   /api/auth/register/           - Register new user
GET    /api/auth/verify-email/:token - Verify email
POST   /api/auth/login-step1/        - Send OTP
POST   /api/auth/login-step2/        - Verify OTP & login
GET    /api/tasks/                   - Get all tasks
POST   /api/tasks/                   - Create task
PATCH  /api/tasks/:id/               - Update task
DELETE /api/tasks/:id/               - Delete task
```

## 🤝 Contributing

Contributions welcome! Please open an issue first.

## 👨‍💻 Author

**Yashika Salonia**

- GitHub: [@yashika-salonia](https://github.com/yashika-salonia)
- LinkedIn: [Yashika Salonia](https://www.linkedin.com/in/yashikasalonia/)

## 🙏 Acknowledgments

- Built as a learning project
- Inspired by modern productivity tools
- Thanks to open-source community

---

⭐ Star this repo if you found it helpful!
