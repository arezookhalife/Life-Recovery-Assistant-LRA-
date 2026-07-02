# PROJECT LOG

Life Recovery Assistant (LRA)

This file tracks major decisions, scope changes, and technical milestones during the development of LRA.

---

## Entry Format

Each entry contains:

- Date
- Area
- Decision
- Reason
- Impact
- Status

---

## 2026-07-02

### Area
Product Definition

### Decision
Defined LRA as a Daily Planning and Recovery Assistant instead of a traditional todo application.

### Reason
The main value of the product is helping users recover their day after disruptions.

### Impact
Architecture and domain model were adjusted to support recovery workflows.

### Status
Approved

---

## 2026-07-02

### Area
Core Product Flow

### Decision
Defined the core user journey:

Capture → Today → Disruption → Recovery → Continue

### Reason
This represents the real moment of value for users.

### Impact
All MVP features must support this workflow.

### Status
Approved

---

## 2026-07-02

### Area
MVP Scope

### Decision
Limited the MVP to the minimal recovery workflow.

### Reason
Smaller scope allows faster development and validation.

### Impact
Many complex features moved to later phases.

### Status
Approved

---

## 2026-07-02

### Area
AI Strategy

### Decision
AI features are excluded from the MVP.

### Reason
AI increases complexity and slows early development.

### Impact
Planning and recovery systems will be rule-based.

### Status
Approved

---

## 2026-07-02

### Area
Domain Model

### Decision
Defined core entities:

- Task
- DailyPlan
- PlannedTask
- Disruption
- RecoverySession

### Reason
These entities support the full recovery workflow.

### Impact
Database design is based on these models.

### Status
Approved

---

## 2026-07-02

### Area
Architecture

### Decision
Adopted service-based architecture.

### Reason
Business logic should be separated from views and serializers.

### Impact
Created services layer inside the tasks app.

### Status
Approved

---

## 2026-07-02

### Area
Planning Engine

### Decision
Introduce a rule-based planning engine.

### Reason
The system must automatically generate daily plans.

### Impact
Implementation will be in planner.py.

### Status
In Progress

---

## 2026-07-02

### Area
Recovery Engine

### Decision
Design a recovery engine to rebuild plans after disruptions.

### Reason
Recovery is the core value of LRA.

### Impact
Implementation will be in recovery.py.

### Status
Planned

---

## 2026-07-02

### Area
Database

### Decision
Use SQLite for MVP.

### Reason
Simpler setup and faster development.

### Impact
PostgreSQL will be used in production.

### Status
Approved
