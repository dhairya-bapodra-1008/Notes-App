# Notes App

## Setup the Project

1. Install Python 3.10 or above
2. Create a virtual environment and activate it
   ```bash
   python -m venv venv
   ```
    - For Windows
   ```bash
   venv/Scripts/activate
   ```
    - For Linux
   ```bash
   source venv/bin/activate 
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Apply database migrations
   ```bash
   python manage.py migrate
   ```

## Run the Project

Start the server

   ```bash
   python manage.py runserver
   ```

Please use the postman collection for manually testing APIs.

## Run Test Cases

Unittests can be executed using the following command

   ```bash
   python manage.py test
   ```

## Author

- [@dhairya-bapodra](https://linkedin.com/in/dhairya-bapodra)