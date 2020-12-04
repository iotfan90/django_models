# citybestrenovations
city best Renovations
## Installation

- Clone this repository and install dependencies

    ```commandline
    git clone https://github.com/nirbhaisidhu/citybestrenovations.git
    pip install -r requirements.txt
    cd citybestrenovations/frontend
    npm install      
  ```
- Create DB
    ```commandline
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```  

- Run

    ```commandline
    python manage.py runserver
    cd frontend
    npm start
    ```    