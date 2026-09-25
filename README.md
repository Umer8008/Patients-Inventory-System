# Patient Management System API

A lightweight RESTful API built with **FastAPI** and **Pydantic** to manage patient records. The application uses a local JSON file for data persistence and automatically computes patient health metrics such as Body Mass Index (BMI) and health category verdicts upon creation or update.

## Features

- **Full CRUD Operations**: Create, read, update, and delete patient records.
- **Automated Health Metrics**: Dynamically calculates `bmi` and weight status (`verdict`) using computed Pydantic fields.
- **Sorting**: Filter and sort patients dynamically by `height`, `weight`, or `bmi` in ascending or descending order.
- **Data Validation**: Strict type-checking and value range enforcement on patient profiles (age, height, weight, gender, etc.).
- **JSON File Persistence**: Stores data locally in `patients.json`.

---

## Technical Stack

- **Framework**: FastAPI
- **Data Validation**: Pydantic v2
- **Data Storage**: JSON (`patients.json`)
- **Server**: Uvicorn

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
