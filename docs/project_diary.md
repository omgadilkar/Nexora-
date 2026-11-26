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

---

### Session 3: Backend Application Scaffolding & FastAPI Engine Setup
- **Date**: November 23, 2026
- **Status**: Completed

#### Objectives & Work Completed:
1. **Backend Directory Structure**:
   - Structured decoupled enterprise folder architecture under `/backend`:
     - `app/core/config.py`: Centralized environment loader using Pydantic Settings (`BaseSettings`).
     - `app/api/v1/`: Versioned routing gateway with modular sub-routers.
     - `app/main.py`: ASGI application entrypoint with CORS middleware support.
     - `backend/tests/`: Automated unit testing suite with Pytest and Starlette TestClient.
2. **Environment & Security Configuration**:
   - Implemented `.env.example` template and local `.env` configuration.
   - Configured cross-origin resource sharing (CORS) allowing communication from React Web (`localhost:5173`) and Flutter Mobile clients.
3. **Automated Unit Testing & Verification**:
   - Implemented `test_health.py` validating the root endpoint (`/`) and system status endpoint (`/api/v1/health/`).
   - All tests passing with 100% success rate (0.43s).

#### Key Architectural Decisions:
- **Pydantic v2 Settings Management**: All secrets and environment variables are strictly validated and loaded through `pydantic-settings`.
- **API Versioning**: Enforced `/api/v1` namespace across all domain routers to ensure backward compatibility as the mobile app evolves.

#### Deliverables & Milestones:
- Working FastAPI application skeleton with automatic Swagger (`/docs`) and Redoc (`/redoc`) generation.
- Passing unit test suite (`pytest backend/tests`).

#### Next Session (Session 4):
- Database Connection & Base ORM Model: Setup SQLAlchemy 2.0 database engine, session factory (`get_db`), Alembic migration environment, and base audit model (`created_at`, `updated_at`).

---

### Session 4: Database Connection Engine & SQLAlchemy 2.0 Base Model
- **Date**: November 23, 2026
- **Status**: Completed

#### Objectives & Work Completed:
1. **Database Session Manager (`backend/app/db/session.py`)**:
   - Created SQLAlchemy database engine connected via `DATABASE_URL`.
   - Built session factory (`SessionLocal`) and FastAPI dependency (`get_db`) that provides a transactional database session per request and cleanly closes it afterwards.
2. **Base Declarative Model (`backend/app/db/base_class.py`)**:
   - Defined custom `Base` class using modern SQLAlchemy 2.0 `DeclarativeBase`.
   - Added automatic table naming logic (converts `StudentProfile` class into `student_profiles` table).
   - Added audit columns (`created_at` and `updated_at`) automatically inherited by all future tables.
3. **Automated Testing (`backend/tests/test_db.py`)**:
   - Wrote unit tests verifying engine connectivity, table name generation, and session lifecycle.
   - All 5 test cases passing (100% success rate).

#### Key Architectural Decisions:
- **Automatic Lifecycle Management**: Using FastAPI's `yield` dependency pattern in `get_db()` guarantees zero connection leaks even if an endpoint raises an unhandled exception.
- **Unified Base Class**: Standardized timestamp fields across all tables ensure consistent auditing across academic and financial records.

#### Deliverables & Milestones:
- Working database connection engine and declarative base model.
- 5/5 automated unit tests passing.

#### Next Session (Session 5):
- Alembic Database Migrations: Configure Alembic, generate the initial migration script, and create the database initialization seed script.

---

### Session 5: Alembic Database Migration Framework & Sprint 1 Completion
- **Date**: November 24, 2026
- **Status**: Completed (Sprint 1 Milestone Achieved)

#### Objectives & Work Completed:
1. **Alembic Migration Environment Setup**:
   - Initialized migration tracking engine (`backend/alembic/` and `backend/alembic.ini`).
   - Configured `alembic/env.py` to dynamically load `DATABASE_URL` from application settings and bind to `Base.metadata` for automated schema diffing.
   - Configured SQLite batch mode (`render_as_batch=True`) for cross-database migration compatibility.
2. **Database Initialization Helper (`backend/app/db/init_db.py`)**:
   - Implemented `init_db()` to create and seed initial tables for automated testing and sandbox environments.
3. **Automated Testing & Sprint 1 Verification**:
   - Authored `backend/tests/test_alembic.py` verifying Alembic configuration loading and table creation lifecycle.
   - All 7 test cases across database, migrations, and health endpoints passed successfully (1.38s).

#### Sprint 1 Summary (Week 1 Achieved):
- ✅ IEEE 830 Software Requirements Specification (`docs/SRS.md`).
- ✅ 3NF Relational Database Schema & Visual ER Diagram (`docs/DATABASE_DESIGN.md`).
- ✅ Modular FastAPI Application Structure with CORS and Live Swagger Documentation.
- ✅ SQLAlchemy 2.0 Database Session Manager with automatic lifecycle closing.
- ✅ Alembic Migration Framework for version-controlled database evolutions.

#### Next Session (Sprint 2, Session 6 - Week 2 Kickoff):
- Identity & User Models: Define SQLAlchemy models for `User` and `Role`, implement password hashing via bcrypt, and create registration/login Pydantic validation schemas.

---

## 🗓️ Sprint 2: Identity, Authentication & Role-Based Access Control

### Session 6: User & Role Database Models + Bcrypt Password Security
- **Date**: November 24, 2026
- **Status**: Completed

#### Objectives & Work Completed:
1. **Password Hashing & Security Engine (`backend/app/core/security.py`)**:
   - Implemented `verify_password()` and `get_password_hash()` utilizing bcrypt algorithm with adaptive work factors.
   - Enforced rule that plaintext passwords must never be stored in the database or exposed via logs.
2. **Database Models for Identity (`backend/app/models/`)**:
   - `Role` model: Defines system roles (`ADMIN`, `TEACHER`, `STUDENT`, `PARENT`).
   - `User` model: Stores credentials, names, contact numbers, active status, and links to `role_id` via foreign key.
   - Mapped bidirectional relationship between `Role` and `User`.
3. **Data Transfer Validation Schemas (`backend/app/schemas/user.py`)**:
   - Implemented Pydantic models for request validation (`UserCreate`) and sanitized output (`UserRead`) that strictly prevents leaking password hashes over the API.
4. **Automated Unit Testing (`backend/tests/test_user_model.py`)**:
   - Wrote unit tests verifying bcrypt hashing, user creation in the database, role relationships, and schema validation.
   - All 9 unit tests passing (100% success rate).

#### Key Architectural Decisions:
- **Zero-Exposure Policy**: Kept `hashed_password` completely excluded from all client-facing Pydantic DTOs (`UserRead`).
- **Normalized Roles**: Standardized system roles into an independent relational table rather than hardcoded string enums to support future custom institutional permissions.

#### Deliverables & Milestones:
- Operational `User` and `Role` database models with bcrypt hashing utilities.
- 9 passing automated unit tests.

#### Next Session (Session 7):
- JWT Security Utilities: Implement JWT Access Token creation with expiration timestamps, token decoding, and signature verification.

---

### Session 7: JWT (JSON Web Token) Security Framework
- **Date**: November 25, 2026
- **Status**: Completed

#### Objectives & Work Completed:
1. **Cryptographic Token Generator (`backend/app/core/security.py`)**:
   - Implemented `create_access_token()` stamping user ID (`sub`), role scope (`role`), issued-at (`iat`), and expiration (`exp`) signed via HS256 algorithm.
   - Implemented `decode_access_token()` providing cryptographic signature validation against application `SECRET_KEY`.
2. **Authentication DTO Schemas (`backend/app/schemas/token.py`)**:
   - Modeled `Token` (Bearer token response model for React/Flutter clients) and `TokenPayload` for internal token inspection.
3. **Automated Unit Testing (`backend/tests/test_jwt.py`)**:
   - Wrote comprehensive test cases covering valid token issuance, decoding integrity, forged/tampered signature rejection, and expired token detection.
   - All 12 unit tests passing (100% success rate).

#### Key Architectural Decisions:
- **Stateless Authentication**: Using self-contained JWT tokens eliminates the need for expensive database lookups on every single authenticated HTTP request.
- **Embedded Role Scopes**: Embedding user role (`ADMIN`, `TEACHER`, etc.) inside the cryptographically signed JWT payload allows instant permission checks without extra database queries.

#### Deliverables & Milestones:
- Operational JWT access token creation and decoding framework.
- 12 passing unit tests across database, models, and authentication security.

#### Next Session (Session 8):
- User Login API Endpoint: Implement `POST /api/v1/auth/login` endpoint accepting credentials, validating password with bcrypt, and issuing JWT tokens.

---

### Session 8: Authentication Endpoint (`/api/v1/auth/login`)
- **Date**: November 26, 2026
- **Status**: Completed

#### Objectives & Work Completed:
1. **OAuth2 Password Login Endpoint (`backend/app/api/v1/endpoints/auth.py`)**:
   - Implemented `POST /api/v1/auth/login` accepting OAuth2 standard credentials (`username` as email and `password`).
   - Validated email existence and bcrypt password hash verification.
   - Enforced account status check preventing inactive users from authenticating.
   - Returned signed JWT access token formatted as a standard Bearer token.
2. **API Routing Gateway Integration (`backend/app/api/v1/api.py`)**:
   - Registered `auth.router` under `/api/v1/auth` with OpenAPI tag `"Authentication"`.
3. **Automated Unit Testing (`backend/tests/test_auth_login.py`)**:
   - Tested 4 authentication scenarios: successful login with token verification, incorrect password rejection, non-existent user handling, and inactive account blocking.
   - All 16 unit tests passing (100% success rate).

#### Key Architectural Decisions:
- **Standardized OAuth2 Password Flow**: Utilizing `OAuth2PasswordRequestForm` ensures seamless compatibility with Swagger UI's interactive "Authorize" lock and client HTTP libraries.
- **Ambiguous Error Messages**: Used uniform `"Incorrect email or password"` error message for both non-existent users and wrong passwords to protect against user enumeration attacks.

#### Deliverables & Milestones:
- Operational `/api/v1/auth/login` API endpoint.
- 16 passing automated unit tests across database, models, JWT, and authentication.

#### Next Session (Session 9):
- Role-Based Access Control (RBAC) & Route Protection: Implement `get_current_user` and role-checker dependencies (`require_role(["ADMIN"])`) to secure endpoints.

---

### Session 9: Role-Based Access Control (RBAC) & Route Protection
- **Date**: November 26, 2026
- **Status**: Completed

#### Objectives & Work Completed:
1. **Authentication & Identity Dependency (`backend/app/api/deps.py`)**:
   - Implemented `get_current_user` dependency extracting and cryptographically verifying Bearer JWT tokens from HTTP Authorization headers.
   - Enforced database user existence check and account active state verification.
2. **Role-Based Access Control Factory (`require_role`)**:
   - Implemented higher-order dependency `require_role(allowed_roles)` providing strict authorization gates.
   - Returns HTTP 403 Forbidden if a user attempts to access resources outside their permitted role scopes.
3. **Protected API Endpoints (`backend/app/api/v1/endpoints/auth.py`)**:
   - Implemented `GET /api/v1/auth/me` returning sanitized profile info for the currently logged-in user.
   - Implemented `GET /api/v1/auth/admin-only` demonstrating role restriction.
4. **Automated Unit Testing (`backend/tests/test_rbac.py`)**:
   - Tested 4 security scenarios: authenticated profile retrieval (200), unauthenticated rejection (401), admin access granting (200), and unauthorized role blockage (403 Forbidden).
   - All 20 unit tests passing (100% success rate).

#### Key Architectural Decisions:
- **FastAPI Dependency Injection**: Using reusable dependencies (`Depends(get_current_user)`) ensures route protection is declarative, clean, and impossible to bypass.
- **Principle of Least Privilege**: Users are granted access only to routes matching their explicit role enum, protecting sensitive management and financial data from students/parents.

#### Deliverables & Milestones:
- Operational security dependencies (`get_current_user`, `require_role`) and protected routes.
- 20 passing unit tests across database, models, JWT, login, and RBAC.

#### Next Session (Session 10 - Week 2 Milestone):
- Database Seeding & Week 2 Completion: Create automated database seed script (`seed_data.py`) populating initial Admin, Teacher, and Student accounts, and finalize Week 2 testing.
