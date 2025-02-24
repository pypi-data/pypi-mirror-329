# Flaskion

Flaskion is a lightweight MVC boilerplate for Flask designed to give developers a structured starting point for building Flask applications. Inspired by Laravel, Flaskion brings a clean and modular structure to Flask, enabling easier scalability and maintenance.

---

## Features
- **MVC Architecture**: Clear separation of concerns with `controllers`, `models`, and `templates`.
- **Centralized Routing**: All routes are managed in a single file (`routes.py`).
- **Scalability**: Ready to integrate extensions like SQLAlchemy, Flask-Migrate, and more.
- **Reusability**: Easily adaptable for any Flask project.

---

## Project Structure
```
flaskion/
├── app/
│   ├── init.py         # Application factory
│   ├── routes.py           # Centralized routes
│   ├── controllers/        # Logic layer
│   ├── models/             # Database models
│   ├── templates/          # HTML templates
│   ├── static/             # Static files
│   └── config.py           # Configuration
├── run.py                  # Entry point
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

---

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/flaskion.git
   cd flaskion
    ```
2.	Create a virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
    pip install -r requirements.txt
   ```
   
## Running the app

1. Start the Flask development server:
    ```bash
    python run.py
   ```
2. Visit the app in your browser:
http://127.0.0.1:5000