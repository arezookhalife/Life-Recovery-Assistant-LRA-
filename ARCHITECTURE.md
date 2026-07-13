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
Task Capture (with behavioral metadata)
↓  
Planning Engine (Behavior-aware) 
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

**Behavior-Aware Design**

The architecture directly supports psychological interventions:
- breakdown detection
- tiny first steps
- cognitive load reduction

**Ethical Gamification**

Motivation mechanics (XP, Streaks) are built into the backend logic without punitive rules.

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

*Note: The Task model includes behavioral fields such as scheduled_date, first_tiny_step, good_enough_definition, and postpone_count.*

---

### 2. Business Logic Layer (Services)

All core logic lives in the services layer.

Directory:

tasks/services/

Main services:

planner.py (Planning engine)  
recovery.py (Recovery engine)
gamification.py (XP and progress logic)

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
- Filter by user's daily capacity (e.g., 180-240 mins)
- Prioritize fixed-date tasks (`scheduled_date`)
- Assign tasks to today's plan
- Generate PlannedTask objects

Example planning logic:

1. Retrieve pending tasks
2. Separate fixed-date tasks from flexible tasks
3. Sort by priority
4. Allocate within daily capacity limit
5. Create DailyPlan and PlannedTask records

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

### Gamification & Behavioral Engine (New)

Location:

tasks/services/gamification.py

Purpose:

Manage ethical user rewards and psychological support.

Responsibilities:

- Calculate XP on task completion
- Reward "Recovery actions" to encourage resilience
- Track non-punitive consistency streaks
- Trigger breakdown suggestions for high postpone counts

---

## Data Flow

Typical workflow:

1. User creates tasks (with optional tiny steps)
2. Tasks are stored as raw tasks
3. Planning engine builds a DailyPlan (including fixed-date tasks)
4. User works on tasks and earns XP
5. A disruption occurs
6. User logs disruption
7. Recovery engine rebuilds the plan
8. User continues working with a fresh plan

---

## Project Structure

Example Django project structure:

LRA_Project/

config/  
Django settings and project configuration

tasks/  
Core application

tasks/models.py  
Database models (with behavioral metadata)

tasks/services/  
Business logic

tasks/services/planner.py  
Daily planning engine

tasks/services/recovery.py  
Recovery engine

tasks/services/gamification.py  
Gamification service

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

**AI Coaching Layer**

Replace rule-based nudges with AI-assisted coaching and energy-level suggestions.

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
- **psychological and emotional safety**
- future scalability

The MVP architecture intentionally avoids unnecessary complexity while keeping the system ready for future growth.
