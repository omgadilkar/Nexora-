# Software Requirements Specification (SRS)
## For NEXORA: Education ERP System

---

### Document Information
- **Project Title**: NEXORA — The Next Era of Learning
- **Version**: 1.0.0
- **Document Status**: Approved Baseline
- **Standard**: IEEE Standard 830-1998 for SRS
- **Date**: November 2026

---

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to define the functional and non-functional requirements for the **NEXORA Education Enterprise Resource Planning (ERP) System**. It serves as a contractual specification for the engineering team, project guides, evaluators, and institutional administrators to guide the implementation, testing, and deployment of the platform.

### 1.2 Document Conventions
- **Requirement Priorities**:
  - `[M]`: Mandatory (Core MVP requirement).
  - `[D]`: Desirable (Second phase requirement).
  - `[O]`: Optional (Future expansion requirement).
- **Standards**: All RESTful APIs adhere to OpenAPI 3.0 specification; database entities follow Third Normal Form (3NF) standards.

### 1.3 Intended Audience
This document is prepared for:
1. Technical Stakeholders, Project Reviewers, and Evaluators reviewing engineering rigor.
2. System Architects and Developers implementing the backend API, web frontend, and mobile application.
3. Quality Assurance (QA) testers designing validation and integration test suites.
4. Institutional Administrators reviewing functional scope.

### 1.4 Project Scope
NEXORA is a comprehensive educational resource planning system designed to replace fragmented spreadsheets, manual paperwork, and isolated software in schools, colleges, and training institutes. It provides:
- Centralized student, guardian, and staff dossier management.
- Academic structure definition (grades, courses, sections, and subject mapping).
- Timetable planning and daily attendance recording.
- Assignment publishing and digital submissions.
- Examination scheduling, marks entry, and automated report card compilation.
- Student fee structure assignment, payment ledger tracking, and receipt generation.
- Role-based multi-client accessibility (Web Dashboard for Administrators, Mobile App for Teachers, Students, and Parents).

---

## 2. Overall Description

### 2.1 Product Perspective
NEXORA operates as an autonomous, self-contained tri-tier client-server enterprise application. 
- **Data Tier**: Relational PostgreSQL database managed via SQLAlchemy 2.0 ORM and Alembic migrations.
- **Application Tier**: Asynchronous Python FastAPI microservice enforcing business rules, data validation via Pydantic, and JWT-based authentication.
- **Presentation Tier**: 
  - **Web ERP Dashboard**: React 19 + TypeScript + Tailwind CSS for high-volume administrative tasks.
  - **Mobile Client**: Flutter + Dart for on-the-go access by teachers, students, and parents.

### 2.2 User Classes & Characteristics

| User Role | Access Medium | Profile & Responsibilities |
| :--- | :--- | :--- |
| **Administrator (Principal / Management)** | Web ERP Dashboard | Full system permissions. Manages staff onboarding, student admissions, class structures, fee categories, institutional audits, and system configuration. |
| **Teacher / Faculty** | Mobile App & Web | Records class attendance, views daily timetable, creates homework assignments, evaluates submissions, enters exam marks, and monitors student attendance health. |
| **Student** | Mobile App | Views daily schedules, checks real-time attendance percentage, submits homework, checks examination routines, views term report cards, and inspects fee balances. |
| **Parent / Guardian** | Mobile App | Monitors child's attendance records, tracks academic results, receives disciplinary/attendance alerts (<75%), and views/downloads fee receipts. |

### 2.3 Operating Environment
- **Server OS**: Linux (Ubuntu 22.04 LTS / Debian 12) or Windows 10/11 / Server 2022.
- **Database**: PostgreSQL 15+ (SQLite supported for local development environment).
- **Backend Runtime**: Python 3.9+ with FastAPI and Uvicorn ASGI server.
- **Web Browser Support**: Google Chrome 110+, Mozilla Firefox 110+, Microsoft Edge 110+, Safari 16+.
- **Mobile Platform**: Android 8.0+ (API level 26+) and iOS 14.0+.

### 2.4 Design & Implementation Constraints
- **Security**: Passwords must be hashed using industry-standard algorithms (Argon2 or bcrypt). Plaintext passwords must never be stored or logged.
- **Data Integrity**: Relational constraints (Foreign Keys, Unique Keys, Not-Null) must be strictly enforced at the database level.
- **Response Latency**: API responses for basic CRUD requests must return within 200ms under standard local network conditions.
- **Offline Resilience**: The mobile app must gracefully handle transient network loss and alert the user without crashing.

---

## 3. System Features & Functional Requirements

### 3.1 Module 1: User Identity, Authentication & Role-Based Access Control (RBAC)
- **FR-1.1 [M]**: The system shall permit users to authenticate using an email/username and password.
- **FR-1.2 [M]**: The system shall issue cryptographically signed JSON Web Tokens (JWT) containing user ID, role scopes, and expiration timestamps.
- **FR-1.3 [M]**: The system shall enforce role-based route protection on all protected endpoints, returning HTTP 401 (Unauthorized) or HTTP 403 (Forbidden) on violation.
- **FR-1.4 [M]**: The system shall provide a secure password reset and recovery workflow.

### 3.2 Module 2: Institutional & Academic Structure
- **FR-2.1 [M]**: The system shall support hierarchical organization: Academic Year -> Class (Grade Level) -> Section.
- **FR-2.2 [M]**: The system shall allow administrators to create and manage Courses and Subjects with associated codes (e.g., `PHY101`).
- **FR-2.3 [M]**: The system shall allow assigning one or more teachers to specific subjects within specific class sections.
- **FR-2.4 [M]**: The system shall allow building a weekly timetable mapping day of the week, period slots, subjects, classrooms, and assigned teachers.

### 3.3 Module 3: Student & Staff Lifecycle Management
- **FR-3.1 [M]**: The system shall maintain comprehensive student records including admission number, full name, date of birth, gender, blood group, guardian contact details, address, and enrollment status (`ACTIVE`, `INACTIVE`, `ALUMNI`).
- **FR-3.2 [M]**: The system shall allow administrators to search, filter (by class, section, status), and paginate through student directories.
- **FR-3.3 [M]**: The system shall maintain staff and faculty records including employee code, department, qualifications, joining date, and active status.

### 3.4 Module 4: Attendance Tracking & Low-Attendance Alerts
- **FR-4.1 [M]**: The system shall allow authorized teachers to take attendance for their assigned class section for any given date and period.
- **FR-4.2 [M]**: The attendance status for each student shall be recorded as `PRESENT`, `ABSENT`, `LATE`, or `EXCUSED`.
- **FR-4.3 [M]**: The system shall automatically compute cumulative attendance percentages per student for the current term/semester.
- **FR-4.4 [M]**: The system shall flag students whose attendance falls below the institutional minimum threshold (default: 75%) and surface them on the administrator and teacher dashboard.

### 3.5 Module 5: Assignments & Learning Resources
- **FR-5.1 [M]**: Teachers shall be able to post assignments with title, description, attached file URL, maximum marks, and submission deadline.
- **FR-5.2 [M]**: Students enrolled in the corresponding class section shall view active assignments and submit work (text or document links) before the deadline.
- **FR-5.3 [M]**: Teachers shall be able to review submissions, record marks obtained, and provide qualitative feedback.

### 3.6 Module 6: Examinations & Gradebook Management
- **FR-6.1 [M]**: Administrators shall create examination schedules (e.g., Mid-Term 2026, Annual Finals) defining subject, exam date, duration, total marks, and passing marks.
- **FR-6.2 [M]**: Teachers shall be able to enter student marks through a batch tabular interface with validation against the maximum marks limit.
- **FR-6.3 [M]**: The system shall auto-generate individual student report cards displaying subject scores, letter grades, percentage, GPA, and pass/fail outcome.

### 3.7 Module 7: Fee Structures, Payments & Receipts
- **FR-7.1 [M]**: Administrators shall configure fee categories (e.g., Tuition Fee, Science Lab Fee, Sports Fee, Transport).
- **FR-7.2 [M]**: The system shall allocate fee dues to students based on their enrolled class level.
- **FR-7.3 [M]**: The system shall record payments (Cash, Bank Transfer, Online) and track student fee balances (`PAID`, `PARTIAL`, `OVERDUE`).
- **FR-7.4 [M]**: The system shall generate a unique printable payment receipt with a sequential receipt number and transaction timestamp.

### 3.8 Module 8: Analytics, Dashboards & Reporting
- **FR-8.1 [M]**: The administrator dashboard shall display real-time Key Performance Indicators (KPIs): Total Enrolled Students, Active Teachers, Daily Attendance Rate %, and Fee Realization.
- **FR-8.2 [M]**: The system shall produce downloadable reports (CSV/PDF) for attendance registers and term mark sheets.

---

## 4. External Interface Requirements

### 4.1 User Interfaces
- **Web ERP Dashboard**: Clean, responsive, high-contrast dashboard with left sidebar navigation, top KPI stat widgets, search-enabled data grids, modal dialogs for record creation, and print-ready document styling.
- **Mobile Application**: Native mobile layout featuring bottom navigation tabs, touch-friendly card list views, swipeable attendance toggles, and circular visual progress gauges.

### 4.2 Software Interfaces
- **Database Interface**: SQLAlchemy 2.0 ORM communicating over asynchronous PostgreSQL wire protocol (`asyncpg` or `psycopg2`).
- **RESTful API Interface**: JSON data payloads over standard HTTP/1.1 and HTTP/2 protocols with standardized error response bodies (`{"detail": "..."}`).

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements
- **NFR-1**: Standard read queries (student listing, timetable retrieval) shall return within 150 milliseconds.
- **NFR-2**: Batch attendance logging for a class of 50 students shall complete within 300 milliseconds.

### 5.2 Security Requirements
- **NFR-3**: User passwords must never be stored in plain text. Argon2 or bcrypt with a minimum work factor of 12 must be utilized.
- **NFR-4**: API endpoints must validate all user inputs against defined Pydantic schemas to prevent SQL injection, XSS, and parameter tampering.
- **NFR-5**: Access tokens must expire within 60 minutes; refresh tokens must be securely stored and rotated.

### 5.3 Reliability & Maintainability
- **NFR-6**: The system codebase must follow clean separation of concerns (API routers, Service layer, ORM models, Pydantic schemas).
- **NFR-7**: Core business logic must be accompanied by automated Pytest unit tests achieving >80% code coverage.
