# Projet-MeetingPro

- [Projet-MeetingPro](#projet-meetingpro)
  - [Project Overview](#project-overview)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Testing](#testing)


## Project Overview

This project is developed by **Matthieu GRIMM-KEMPF** and **Lucas DAGON** as part of the Object-Oriented Programming in Python course at **ENSISA**, under the supervision of **Loic RIEGEL** and **Francois LUDWINSKI**.

The aim of the project is to create a tool for managing rooms and clients, which also facilitates the management of room reservations.

## Project Structure

```bash
.
├── rapport
├── src
│   ├── persons
│   ├── room
│   └── room_project
│       ├── controller
│       ├── gui
│       ├── person_logic
│       └── room_logic
└── tests
```


- `rapport`: Contains the project report.
- `src`: Contains all the source code.
- `tests`: Contains the tests for the code.

## Installation

To set up the project, follow these steps:

1. Clone the repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Install the project in editable mode by running:
```bash
   pip install -e .
```

## Running the Application

To launch the application, use the following command in the terminal:

```bash
room_project
```

## Testing

To test the code, follow these steps:

1) Install the test dependencies by running:

```bash
pip install .[test]
```
2) Run the tests using pytest:

```bash
pytest
```
3) For a coverage report, use the following command:

```bash
python -m pytest --cov=. -cov-report=html --cov-report=html:./coverage_report.html
```

This will generate a coverage report in HTML format, which can be viewed by opening coverage_report.html in a web browser.