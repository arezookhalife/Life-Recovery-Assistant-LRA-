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
## 2026-07-12

### Area
Product Vision & Strategy

### Decision
Evolved the product from a "Recovery Tool" to a "Behavioral-Aware Planning Assistant" by integrating Psychological Principles and Healthy Gamification into the core MVP.

### Reason
To increase user engagement and provide deeper value by addressing the root causes of procrastination and perfectionism.

### Impact
The product roadmap now includes behavioral metadata (tiny steps, energy levels) and gamification elements as core features rather than just future ideas.

### Status
Approved

---

## 2026-07-12

### Area
AI Strategy

### Decision
Reaffirmed that AI is excluded from the MVP, focusing instead on Rule-Based (Deterministic) Logic for planning and recovery.

### Reason
To ensure predictability, reduce complexity, and establish a solid baseline of rules before adding an intelligent layer.

### Impact
Planning and recovery systems will be implemented using explicit business rules. AI will be reserved for "Phase 3: AI Coaching Layer."

### Status
Approved

---

## 2026-07-12

### Area
Technical Implementation (Planner Engine)

### Decision
Stabilized the Daily Plan generation API and aligned unit tests with current greedy selection behavior.

### Reason
To ensure a reliable and testable baseline before implementing more complex task prioritization.

### Impact
The `test_generate_daily_plan_selects_tasks_within_daily_capacity` test now passes, and the API is stable.

### Status
Completed

---

## 2026-07-12

### Area
Technical Implementation (Serializer)

### Decision
Implemented `total_estimated_minutes` as a dynamic `SerializerMethodField` in `DailyPlanSerializer`.

### Reason
To avoid `FieldError` and unnecessary database schema changes for a calculated field.

### Impact
API now correctly returns the total duration of planned tasks.

### Status
Completed

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
