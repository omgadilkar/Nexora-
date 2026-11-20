# NEXORA — Daily Development Log (Project Diary)

This diary records daily progress, technical decisions, and milestones achieved during the 8-week development lifecycle. It serves as an authentic progress log for review by the project guide / evaluators.

---

## 🗓️ Week 1: Requirements, System Design & Repository Architecture

### Day 1: Project Kickoff, PRD Review & Formal SRS Specification
- **Date**: November 20, 2026
- **Time Dedicated**: 2 Hours (120 minutes)
- **Status**: Completed

#### Objectives & Work Completed:
1. **Product Requirements Analysis**:
   - Reviewed the core PRD document for the NEXORA Education ERP system.
   - Identified the 4 core stakeholder personas: Administrator, Teacher/Faculty, Student, and Parent.
2. **Software Requirements Specification (SRS)**:
   - Authored the formal IEEE 830-compliant SRS document (`docs/SRS.md`).
   - Detailed functional requirements across 8 core modules:
     - Authentication & RBAC
     - Institutional & Academic Structure
     - Student & Staff Lifecycle Management
     - Daily Attendance Engine (<75% At-Risk alerts)
     - Assignments & Submissions
     - Examinations & Gradebook
     - Fee Ledger & Receipt Generation
     - Reporting & Dashboard Analytics
   - Defined non-functional requirements (security, latency benchmarks, data integrity).
3. **Repository Initialization**:
   - Created project repository structure (`/docs`, `/backend`, `/web`, `/mobile`).
   - Configured root `.gitignore` covering Python, Node.js, Flutter, and environment secrets.
   - Initialized Git version control system.

#### Key Architectural Decisions:
- **Decision 1**: Adopt a Tri-Tier Decoupled Architecture. The FastAPI backend serves as the single centralized API engine for both the React Web ERP and the Flutter Mobile App.
- **Decision 2**: Dual-database compatibility. Develop with PostgreSQL for production and support SQLite for zero-friction local development and automated testing.

#### What to Show Sir for Day 1:
- The completed IEEE 830 SRS Document (`docs/SRS.md`).
- Initialized Git repository with clean commit history.

#### Plan for Day 2:
- Design the complete Relational Database Schema (ER Diagram) with all 14 tables, foreign key constraints, and index mappings.
