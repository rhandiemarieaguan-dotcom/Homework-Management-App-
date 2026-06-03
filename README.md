# Homework-Management-App-
Homework Management App is a standalone Python Application Design to help students organize, prioritize, and monitor their homework tasks in a centalized system. The application provides a simple and user-friendly platform where students can manage assignments from different subjects, track deadlines, and monitor academic progress.
Homework Management App

The application allows users to:
	-Create and manage homework tasks by entering details such as title, subject, description, deadline, and subtasks.
	-Verify that required homework information is provided before saving tasks to the system.
	-Organize large assignments through subtasks, allowing students to break work into smaller and more manageable activities.
	-Mark homework tasks and subtasks as complete to track progress effectively.
	-Generate academic progress reports showing completed tasks, pending tasks, overdue tasks, subject-wise performance, and upcoming deadlines.
	-Save and retrieve homework records using local storage for easy access and data persistence.

		Built with a clean Command-Line Interface (CLI), the system emphasizes simplicity, usability, and efficiency. It follows a structured input-process-output model where homework information is collected, checked for completeness, processed through priority computation, and displayed through organized task lists and progress reports.
Through this application, students can improve time management skills, avoid missed deadlines, increase productivity, and maintain better academic performance by having all homework-related information available in a single platform.

OOP Concepts Used
This project demonstrates core Object-Oriented Programming (OOP) principles:
	-Encapsulation: Homework, Subtask, and Report classes protect internal data through controlled methods and attributes.
	-Abstraction: Interfaces and service classes hide implementation details while exposing essential functionalities.
	-Polymorphism: Different storage and reporting components can be used interchangeably through shared interfaces.
	-Single Responsibility Principle (SRP): Each class performs a specific task such as homework management, validation, priority calculation, storage management, or report generation.
	-Open/Closed Principle (OCP): The application can be extended with additional features without modifying existing code.

Technologies Used
	-Python (core programming language)
-Command-Line Interface (CLI) for user interaction
	-File Handling for data storage and report generation
	-Object-Oriented Programming (OOP) principles
	-Local Data Storage for homework persistence

Project Structure
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
│
└── README.md
‘’’

How to Run the Application
1. Requirements python 3.x
2. Clone the Repositories:
Git clone:
3. Navigate the folder
Cd HomeworkManagementApp
4. Run Python Application
 -python main.py
-Run the Test
-Pytest -v
5. Export Report Inside the Application:
-Open the Report Tab
-Click Generate Report
-View the summary of completed, pending, and overdue, homework.
-Export the report.

Developed as a school project by:
Rhandie Marie A. Guan
Github: https://github.com/rhandiemarieaguan-dotcom/CC-103
Aldred C. Valdez
Github: https://github.com/aldredmon54-bot
Aloha jil M. Gozarin
Github: https://github.com/gozarinalohajil 

In Partial Fulfillment of the Requirements for the Subject CC103 Computer programming 2 Under the Course of Bachelor of Science in Information technology at Sorsogon State University Bulan Campus. With the Supervision of our professor John Mark Gabrentina.