# LRA – Life Recovery Assistant

## Goal
Build a mobile-first productivity system that helps users recover when their day gets disrupted.

Core concept:
Disruption → Recovery → Continue

---

## Tech Stack

Backend:
- Django
- Django REST Framework (later)

Database:
- SQLite (MVP)
- PostgreSQL (production)

Frontend MVP:
- Django Templates / Simple HTML

Future:
- React Native Mobile App

---

## Current Data Models

User (Django default)

Task
- title
- description
- priority
- estimated_minutes
- status
- created_at

DailyPlan
- user
- date

PlannedTask
- daily_plan
- task
- order
- planned_minutes
- status

Disruption
- user
- daily_plan
- lost_minutes
- reason

RecoverySession
- disruption
- tasks_kept
- tasks_moved
- recovery_score

---

## Current Progress

✅ Django project created  
✅ tasks app created  
✅ Database models implemented  
✅ Migrations applied  
✅ Admin panel working  

Next Step:
Build the **Daily Planning Engine**
