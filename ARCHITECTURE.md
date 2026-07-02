# LRA Architecture

Life Recovery Assistant (LRA) follows a simple and scalable architecture designed to support the core workflow:

Capture → Plan → Disruption → Recovery → Continue

The system is designed with a clear separation between data models, business logic, and user interfaces.

---

## System Overview

The system transforms raw user tasks into a structured daily plan and helps users recover when their plan breaks.

High-level flow:

User  
↓  
Task Capture  
↓  
Planning Engine  
↓  
Daily Plan  
↓  
Disruption Event  
↓  
Recovery Engine  
↓  
Updated Daily Plan

---

## Architectural Principles

The architecture is guided by several principles.

**Separation of Concerns**

- Models manage data
- Services contain business logic
- Views/API handle interaction
- Templates render the UI

**Rule-Based MVP**

The MVP avoids AI systems.  
All decisions are deterministic and rule-based.

**Fast Interaction**

Task creation must take less than 5 seconds.

**Recovery-Oriented Design**

The system is optimized for handling disruptions and rebuilding plans.

---

## System Layers

### 1. Data Layer (Models)

Responsible for storing application state.

Core models:

User  
Task  
DailyPlan  
PlannedTask  
Disruption  
RecoverySession

Relationships:

User → many Tasks  
User → many DailyPlans  
DailyPlan → many PlannedTasks  
PlannedTask → references Task  
Disruption → linked to DailyPlan  
RecoverySession → linked to Disruption

---

### 2. Business Logic Layer (Services)

All core logic lives in the services layer.

Directory:

tasks/services/

Main services:

planner.py  
recovery.py

Views and APIs should never contain business rules.

---

### 3. Interface Layer

Responsible for user interaction.

Two interfaces exist:

**Web UI (MVP)**  
Django Templates

**API Layer**  
Django REST Framework

The API enables future mobile clients.

---

## Core Engines

### Planning Engine

Location:

tasks/services/planner.py

Purpose:

Transform raw tasks into a structured daily plan.

Responsibilities:

- Select pending tasks
- Sort tasks by priority
- Estimate available time
- Assign tasks to today's plan
- Generate PlannedTask objects

Example planning logic:

1. Retrieve all pending tasks
2. Sort by priority
3. Allocate time sequentially
4. Create DailyPlan
5. Create PlannedTask records

---

### Recovery Engine

Location:

tasks/services/recovery.py

Purpose:

Rebuild the daily plan after a disruption.

Responsibilities:

- record disruption
- evaluate remaining time
- keep unfinished tasks
- move excess tasks to future

Recovery strategy:

1. Identify incomplete tasks
2. Estimate remaining time in the day
3. Keep tasks that fit
4. Move overflow tasks to tomorrow
5. Create a RecoverySession record

---

## Data Flow

Typical workflow:

1. User creates tasks
2. Tasks are stored as raw tasks
3. Planning engine builds a DailyPlan
4. User works on tasks
5. A disruption occurs
6. User logs disruption
7. Recovery engine rebuilds the plan
8. User continues working

---

## Project Structure

Example Django project structure:

LRA_Project/

config/  
Django settings and project configuration

tasks/  
Core application

tasks/models.py  
Database models

tasks/services/  
Business logic

tasks/services/planner.py  
Daily planning engine

tasks/services/recovery.py  
Recovery engine

tasks/views.py  
Web views

tasks/api/  
API endpoints

templates/  
UI templates

static/  
Static assets

---

## Database (MVP)

The MVP uses SQLite for simplicity.

Production environments will migrate to PostgreSQL.

Migration path:

SQLite → PostgreSQL

No schema changes required.

---

## Future Architecture Extensions

The architecture allows several future upgrades.

**AI Planning Engine**

Replace rule-based planner with AI-assisted planning.

**AI Recovery Assistant**

Suggest better recovery strategies.

**Mobile Application**

React Native client using the REST API.

**Calendar Integration**

Google Calendar / Apple Calendar sync.

**Analytics Layer**

Behavior insights and productivity patterns.

---

## Design Goals

The architecture prioritizes:

- simplicity
- fast development
- reliability
- clear separation of logic
- future scalability

The MVP architecture intentionally avoids unnecessary complexity while keeping the system ready for future growth.
