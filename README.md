# vMessenger

vMessenger is a web-based messaging application designed to provide seamless and secure communication. This project is currently in development.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

vMessenger is a web application that allows users to send and receive messages in real-time. It is built with a focus on simplicity, performance, and security.

## Features

- User registration and authentication
- Real-time messaging
- User profile management
- Secure data handling
- Responsive design

## Tech Stack

- **Backend**: Python, Django
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript (jQuery)
- **Data Handling**: AJAX for asynchronous communication

## Screenshots

### Login Page
![Login Page](https://i.imgur.com/e7EYNF9.png)

### Registration Page
![Registration Page](https://i.imgur.com/e9d1izg.png)

### Messaging Interface
![Messaging Interface](https://i.imgur.com/UUQBuol.png)

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/vMessenger.git
   cd vMessenger
   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database**:
   
   - Create a database and user in PostgreSQL.
   - Update the `DATABASES` settings in `vMessenger/settings.py` with your database credentials.

5. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

## Usage

1. Open your web browser and go to `http://localhost:8000`.
2. Register a new user or log in with the superuser account.
3. Start messaging!

## Project Structure

```
vMessenger/
├── vMessenger/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── UserManager/
│   ├── models.py
│   ├── views.py
│   └── ...
├── DataHub/
│   ├── models.py
│   ├── views.py
│   └── ...
├── AssetManager/
│   ├── models.py
│   ├── views.py
│   └── ...
├── PathManager/
│   ├── models.py
│   ├── views.py
│   └── ...
├── static/
├── templates/
└── manage.py
```

## API Endpoints

- **User Registration**: `POST /api/register/`
- **User Login**: `POST /api/login/`
- **Send Message**: `POST /api/messages/send/`
- **Retrieve Messages**: `GET /api/messages/`


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

Please ensure your code follows the project's coding standards and passes all tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or feedback, please contact me at [vigneshar24@protonmail.com](mailto:vigneshar24@protonmail.com).
