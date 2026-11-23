# NEXORA — Engineering Development Log

This log tracks architectural decisions, technical specifications, and development milestones across the project lifecycle.

---

## 🗓️ Sprint 1: Requirements, System Architecture & Repository Setup

### Session 1: Project Kickoff, PRD Review & Formal SRS Specification
- **Date**: November 20, 2026
- **Status**: Completed

#### Objectives & Work Completed:
1. **Product Requirements Analysis**:
   - Analyzed core operational workflows for the NEXORA Education ERP system.
   - Defined role boundaries and permissions for four core user groups: Administrators, Faculty/Staff, Students, and Parents.
2. **Software Requirements Specification (SRS)**:
   - Authored the formal IEEE 830-compliant SRS document (`docs/SRS.md`).
   - Defined functional requirements across 8 core modules:
     - Authentication & Role-Based Access Control (RBAC)
     - Institutional & Academic Structure
     - Student & Staff Lifecycle Management
     - Daily Attendance Engine (<75% threshold alerts)
     - Assignments & Submissions
     - Examinations & Gradebook
     - Fee Ledger & Receipt Generation
     - Reporting & Dashboard Analytics
   - Established non-functional requirements (security, latency benchmarks, data integrity).
3. **Repository Architecture**:
   - Structured multi-tier repository layout (`/docs`, `/backend`, `/web`, `/mobile`).
   - Configured `.gitignore` covering Python, Node.js, Flutter, and environment configurations.
   - Initialized Git version control.

#### Key Architectural Decisions:
- **Architecture**: Decoupled Tri-Tier architecture with FastAPI as the centralized API gateway serving both React Web ERP and Flutter Mobile clients.
- **Persistence**: Relational PostgreSQL database managed via SQLAlchemy 2.0 ORM with Alembic migration tracking.

#### Deliverables & Milestones:
- Published IEEE 830 SRS Document (`docs/SRS.md`).
- Clean repository baseline initialized with version control.

#### Next Session:
- Relational Database Schema Design (ER Diagram) with entity relationships, foreign keys, and indexing strategy.

---

### Session 2: Relational Database Schema & Entity-Relationship (ER) Architecture
- **Date**: November 23, 2026
- **Status**: Completed

#### Objectives & Work Completed:
1. **Third Normal Form (3NF) Relational Modeling**:
   - Designed 14 normalized database tables across 6 functional domains:
     - Identity & Access Management: `roles`, `users`
     - Academic Hierarchy: `academic_years`, `classes`, `sections`, `subjects`, `teacher_subject_allocations`
     - Profiles: `student_profiles`, `staff_profiles`
     - Scheduling & Daily Attendance: `timetable_slots`, `attendance_sessions`, `attendance_records`
     - Evaluations: `examinations`, `exam_schedules`, `exam_results`
     - Finance: `fee_structures`, `student_fees`, `fee_payments`
2. **Visual ER Diagram & Data Dictionary**:
   - Built a comprehensive Mermaid Entity-Relationship diagram illustrating table linkages and Crow's foot cardinality (`docs/DATABASE_DESIGN.md`).
   - Documented explicit column data types, nullability, constraints, primary keys, and foreign keys.
3. **Data Integrity & Indexing Strategy**:
   - Implemented cascading rules: `ON DELETE CASCADE` for tightly bound dependent records (attendance records), and `ON DELETE RESTRICT` for financial and historical student entities.
   - Designed composite indexes for high-frequency queries (e.g., student attendance history, fee balances, and timetable schedules) to achieve sub-150ms latency.

#### Key Architectural Decisions:
- **Decoupled Auth & Profiles**: Kept authentication credentials in `users` isolated from demographic data in `student_profiles` and `staff_profiles` to prevent schema bloat and adhere to 3NF.
- **Two-Tier Attendance Model**: Modeled attendance via `attendance_sessions` and `attendance_records` to eliminate data redundancy across class rosters.
- **Financial Audit Safety**: Implemented immutable payment logs (`fee_payments`) with unique alphanumeric receipt numbers.

#### Deliverables & Milestones:
- Published Database Specification & Visual ER Architecture (`docs/DATABASE_DESIGN.md`).
- Updated project documentation index (`README.md`).

#### Next Session (Session 3):
- Backend Foundation: Setup FastAPI application structure, virtual environment, `requirements.txt`, and Pydantic configuration (`.env`).
