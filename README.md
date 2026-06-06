# Homework-Management-App-

Homework Management App is a Console Python Application designed to help students organize, prioritize, and monitor their homework tasks in a centralized system. The application provides a simple and user-friendly platform where students can manage assignments from different subjects, track deadlines, and monitor academic progress.

## Features

The application allows users to:

- Create and manage homework tasks by entering details such as title, subject, description, deadline, and subtasks.
- Verify that required homework information is provided before saving tasks to the system.
- Organize large assignments through subtasks, allowing students to break work into smaller and more manageable activities.
- Mark homework tasks and subtasks as complete to track progress effectively.
- Generate academic progress reports showing completed tasks, pending tasks, overdue tasks, subject-wise performance, and upcoming deadlines.
- Save and retrieve homework records using local storage for easy access and data persistence.

Built with a clean Command-Line Interface (CLI), the system emphasizes simplicity, usability, and efficiency. It follows a structured input-process-output model where homework information is collected, checked for completeness, processed through priority computation, and displayed through organized task lists and progress reports.

## OOP Concepts Used

This project demonstrates core Object-Oriented Programming (OOP) principles:

- **Encapsulation:** Homework, Subtask, and Report classes protect internal data through controlled methods and attributes.
- **Abstraction:** Interfaces and service classes hide implementation details while exposing essential functionalities.
- **Polymorphism:** Different storage and reporting components can be used interchangeably through shared interfaces.
- **Single Responsibility Principle (SRP):** Each class performs a specific task such as homework management, validation, priority calculation, storage management, or report generation.
- **Open/Closed Principle (OCP):** The application can be extended with additional features without modifying existing code.

## Technologies Used

- **Python** (core programming language)
- **Command-Line Interface (CLI)** for user interaction
- **File Handling** for data storage and report generation
- **Object-Oriented Programming (OOP)** principles
- **Local Data Storage** for homework persistence

## Project Structure

```text
HomeworkManagementApp/
│
├── interfaces/
│   └── storage.py
│
├── models/
│   ├── homework.py
│   ├── subtask.py
│   ├── report_data.py
│   └── subject_stats.py
│
├── services/
│   ├── validation_service.py
│   ├── priority_engine.py
│   ├── report_generator.py
│   └── homework_service.py
│
├── tests/
│   └── test_services.py
│
├── main.py
└── README.md
```

How to Run the Application

Requirements

- Python 3.x

Clone the Repository

git clone <repository-url>

Navigate to the Project Folder

cd HomeworkManagementApp

Run the Application

python main.py

Run the Tests

pytest -v

Export Report Inside the Application

1. Open the Report Tab.
2. Click Generate Report.
3. View the summary of completed, pending, and overdue homework.
4. Export the report.

Developers

Rhandie Marie A. Guan

GitHub: https://github.com/rhandiemarieaguan-dotcom/CC-103

Aldred C. Valdez

GitHub: https://github.com/aldredmon54-bot

Aloha Jill M. Gozarin

GitHub: https://github.com/gozarinalohajil

Acknowledgment

In partial fulfillment of the requirements for the subject CC103 Computer Programming 2 under the course of Bachelor of Science in Information Technology at Sorsogon State University Bulan Campus, with the supervision of Professor John Mark Gabrentina.