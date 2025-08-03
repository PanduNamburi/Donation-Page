# 💼 Fundraising Intern Portal - Full Stack Web Application

A modern, full-stack web application built with Django and vanilla JavaScript, demonstrating proficiency in backend development, frontend design, and database management.

## 🚀 **Live Demo**
[Add your live demo link here once deployed]

## 🛠️ **Technical Stack**

### **Backend**
- **Django 5.2.4** - Python web framework
- **Django REST Framework 3.16.0** - API development
- **SQLite3** - Database management
- **Token Authentication** - Secure API access
- **Django Admin** - Data management interface

### **Frontend**
- **Vanilla JavaScript** - No frameworks, pure JS
- **HTML5/CSS3** - Modern responsive design
- **Fetch API** - Asynchronous data handling
- **LocalStorage** - Client-side data persistence
- **CSS Grid/Flexbox** - Modern layout techniques

## 🎯 **Key Features**

### **Authentication System**
- User registration and login functionality
- Token-based authentication for API security
- Automatic token generation and management
- Client-side authentication state handling

### **Real-time Dashboard**
- Live statistics and data visualization
- Dynamic leaderboard with rankings
- Achievement system with badges
- Notification center with modal popups

### **Donation Management**
- Public donation forms with referral codes
- Donor information tracking
- Message system for donors
- Automatic intern profile updates

### **Gamification Features**
- Achievement unlocking system
- Points-based ranking system
- Progress tracking and visualization
- Real-time notification badges

## 📊 **Project Structure**
```
FSD1/
├── api/                    # Django app (models, views, serializers)
├── intern_portal/          # Django project settings
├── static/                 # Frontend files (HTML/CSS/JS)
├── db.sqlite3             # SQLite database
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- pip (Python package installer)

### **Installation**
```bash
# Clone the repository
git clone https://github.com/PanduNamburi/Donation-Page.git
cd Donation-Page

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

### **Access Points**
- **Main Application**: `http://localhost:8000`
- **Admin Panel**: `http://localhost:8000/admin/`

## 🔧 **API Endpoints**

### **Authentication**
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### **Core Data**
- `GET /api/intern/` - Current user's intern data
- `GET /api/leaderboard/` - Leaderboard data
- `GET /api/dashboard-stats/` - Comprehensive dashboard stats

### **Notifications**
- `GET /api/notifications/` - User's notifications
- `POST /api/notifications/<id>/read/` - Mark notification as read

### **Donations**
- `POST /api/donations/add/` - Add donation (public)

## 🎨 **Features**

### **Backend Architecture**
- Designed and implemented 8+ RESTful API endpoints
- Built comprehensive data models with proper relationships
- Implemented automatic rank calculation system
- Developed achievement unlocking logic
- Created notification system with read/unread status

### **Frontend Development**
- Built responsive UI without external frameworks
- Implemented real-time data updates using Fetch API
- Created modal-based notification system
- Developed copy-to-clipboard functionality
- Built dynamic leaderboard with live data

### **Database Design**
- Designed normalized database schema with 5 core models
- Implemented proper foreign key relationships
- Created efficient queries for leaderboard calculations
- Built automatic data validation and integrity checks

## 🔒 **Security Features**
- Token-based authentication
- Input validation and sanitization
- CSRF protection
- SQL injection prevention through Django ORM
- XSS protection through proper escaping

## 📈 **Performance Optimizations**
- Efficient database queries with proper indexing
- Client-side caching using localStorage
- Minimal API calls with comprehensive data endpoints
- Responsive images and optimized assets

## 🚀 **Deployment Ready**
- Clean, production-ready code
- Comprehensive error handling
- Proper logging and debugging
- Scalable architecture
- Environment variable configuration

## 🤝 **Contributing**
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**
**Pandu Namburi**
- GitHub: [@PanduNamburi](https://github.com/PanduNamburi)

---

**This project demonstrates proficiency in full-stack web development, database design, API development, and modern frontend techniques without relying on external frameworks.** 