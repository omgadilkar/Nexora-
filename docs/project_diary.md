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
