# NEXORA — The Next Era of Learning
> **Enterprise Education Resource Planning (ERP) System**

[![Architecture: Tri-Tier](https://img.shields.io/badge/Architecture-Tri--Tier-indigo)](#)
[![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.110+-009688?logo=fastapi&logoColor=white)](#)
[![Database: PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_16-336791?logo=postgresql&logoColor=white)](#)
[![Web: React + TypeScript](https://img.shields.io/badge/Web-React_19_+_TypeScript-61DAFB?logo=react&logoColor=black)](#)
[![Mobile: Flutter](https://img.shields.io/badge/Mobile-Flutter_3.x-02569B?logo=flutter&logoColor=white)](#)

---

## 📖 Overview

**NEXORA** is a modern, role-based Education ERP designed for schools, colleges, and training institutions. It eliminates scattered records, manual paperwork, and fragmented communication by providing a centralized digital system for:
- **Student & Staff Lifecycle Management**
- **Classes, Sections, Courses & Subject Allocations**
- **Class Schedules & Daily Attendance Recording**
- **Examinations, Marksheets, GPA & Report Cards**
- **Student Fee Structures, Payments & Receipts**
- **Real-Time Academic Analytics & Low-Attendance Alerts (<75%)**

The platform provides a **Web ERP Administrative Dashboard** (React + TypeScript) for institution management, supported by a cross-platform **Mobile Application** (Flutter) for teachers, students, and parents, powered by a high-performance **FastAPI backend** and **PostgreSQL database**.

---

## 🏛️ System Architecture

```
┌────────────────────────────────────────────────────────┐
│                      NEXORA CLIENTS                    │
│   Web ERP Dashboard (React)     Mobile App (Flutter)   │
│   • School Administrators       • Teachers             │
│   • Academic Coordinators       • Students & Parents   │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTPS / JSON Web Tokens
                           ▼
┌────────────────────────────────────────────────────────┐
│                   BACKEND API ENGINE                   │
│                Python 3.9+ with FastAPI                │
│   • Role-Based Access Control (RBAC: Admin/Staff/User) │
│   • Business Rule Engine (Fee ledger, Pass/Fail logic) │
│   • Real-Time Metrics & At-Risk Student Aggregators    │
└──────────────────────────┬─────────────────────────────┘
                           │ SQLAlchemy 2.0 ORM
                           ▼
┌────────────────────────────────────────────────────────┐
│                   CENTRAL DATABASE                     │
│               PostgreSQL + Alembic Migrations          │
│   • Academic records, Attendance sessions, Exam marks  │
│   • Invoices, Receipts, and Audit history              │
└────────────────────────────────────────────────────────┘
```

---

## 📂 Project Repository Layout

```
NEXORA/
├── docs/                     # Project documentation, SRS, design specs & daily log
│   ├── SRS.md               # Software Requirements Specification (IEEE 830)
│   └── project_diary.md     # Daily development progress log
├── backend/                  # FastAPI Backend Application
│   ├── app/                 # Application source code
│   │   ├── api/v1/          # Modular API routers
│   │   ├── core/            # Config, security, database session
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic & services
│   ├── tests/               # Pytest test suite
│   ├── alembic/             # Database migrations
│   └── requirements.txt     # Python dependencies
├── web/                      # React + TypeScript Web ERP Dashboard
│   ├── src/                 # Web client source code
│   └── package.json
├── mobile/                   # Flutter Mobile Application
│   ├── lib/                 # Flutter source code
│   └── pubspec.yaml
├── docker-compose.yml        # Multi-container orchestration
└── README.md
```

---

## 🗓️ 8-Week Phased Development Roadmap

- **Week 1**: Requirements Specification (SRS), Database ER Design & Repository Setup
- **Week 2**: Backend Architecture, PostgreSQL Models, Alembic Migrations & JWT Auth
- **Week 3**: Institutional Structure, Student Profiles & Staff Management APIs
- **Week 4**: Class Timetable, Attendance Engine & At-Risk Analytics
- **Week 5**: Examination Gradebook, Report Card Generator & Student Fee Ledger
- **Week 6**: Web ERP Dashboard (React + TypeScript Admin Portal)
- **Week 7**: Web Attendance Register & Flutter Mobile App Scaffolding
- **Week 8**: Cross-Platform Mobile Flow, Docker Containerization & Final Release

---

## 📄 Documentation
- [Software Requirements Specification (SRS)](docs/SRS.md)
- [Database Design & ER Architecture](docs/DATABASE_DESIGN.md)
- [Daily Development Log](docs/project_diary.md)
