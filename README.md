# Task Management and Timetable App

## Description
A web application that helps users schedule their tasks and manage their timetables. The app includes user authentication for a personalized experience.

## Features
- **Task Scheduling**: Add, edit, and delete tasks with optional details like due date, time, priority, and completion status.
- **Timetable Management**: Add, edit, and delete timetable entries with start and end times.
- **User Authentication**: Secure login and signup functionality.

## Live Demo
- Visit the live demo at [cs50Project.shoaibssm.me](http://cs50Project.shoaibssm.me)
- Please allow up to 1 minute for the server to activate (this is a hosting-related issue that will be resolved shortly).

## Installation (For Local Installation)
1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    ```

2. **Navigate to the project directory**:
    ```sh
    cd project-directory
    ```

3. **Set up a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Initialize the database**:
    ```sh
    python init_db.py
    ```

6. **Start the application**:
    ```sh
    python app.py
    ```

## Usage (For Local Installation)
1. Open your web browser and go to `http://localhost:5000`.
2. Register for an account or log in if you already have one.
3. Start scheduling your tasks and managing your timetable!

## Contributing
1. **Fork the repository**.
2. **Create a new branch**:
    ```sh
    git checkout -b feature-branch
    ```
3. **Make your changes**.
4. **Commit your changes**:
    ```sh
    git commit -m 'Add some feature'
    ```
5. **Push to the branch**:
    ```sh
    git push origin feature-branch
    ```
6. **Open a pull request**.

## License
This project is licensed under the MIT License.