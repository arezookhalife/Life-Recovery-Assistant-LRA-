# Life Recovery Assistant (LRA)

Life Recovery Assistant (LRA) is a productivity recovery application designed to help busy people regain control of their day after unexpected disruptions.

Unlike traditional task managers, LRA focuses on what happens when a plan breaks.

The goal is simple: help users quickly recover and continue working on what truly matters.


---

## Problem

Most productivity tools assume a predictable schedule.

Real life is different.

Days are often disrupted by:

- unexpected meetings  
- family responsibilities  
- energy drops  
- urgent tasks  
- external interruptions  

When a disruption happens, people usually lose their plan and struggle to decide what to do next.

LRA is designed specifically for that moment.

---

## Core Idea

LRA is not just a todo list.

It is a **Daily Planning and Recovery Assistant** built on **Behavioral Design**.

Users capture tasks quickly, and the system helps them rebuild their plan when the day gets disrupted, using psychological principles to reduce friction and shame.

Core concept:

Disruption → Recovery → Continue

---

## MVP Flow

Capture → Today → Disruption → Recovery → Continue

1. Capture tasks quickly  
2. Generate a daily plan  
3. Work on tasks  
4. Log disruptions when the plan breaks  
5. Recover the plan  
6. Continue the day  

---

## MVP Features

The MVP includes only the core functionality needed to validate the product idea.

**Quick Capture**  
Users can create tasks in less than 5 seconds.

**Daily Planning**  
The system generates a daily plan based on pending tasks and user capacity.

**Today View**  
Users see the tasks planned for today.

**Task Completion**  
Tasks can be marked as completed.

**Disruption Logging**  
Users can log unexpected events that interrupt their day.

**Recovery Engine**  
The system rebuilds the daily plan after a disruption.

**Behavioral Support**  
Built-in support for tiny steps and managing task complexity.

**Healthy Gamification**  
Basic progress tracking and rewards to encourage consistency without pressure.

---

## Out of Scope (MVP)

The following features are intentionally excluded from the MVP.

- AI assistant / AI coach  
- Voice input  
- Calendar integration  
- Team collaboration  
- Projects or workspaces  
- Subtasks  
- Habit tracking  
- Offline mode  
- Drag-and-drop scheduling  
- Native mobile app  

These features may appear in future phases.

---

## Domain Model

The core entities of the system are:

- User  
- Task (with behavioral metadata) 
- DailyPlan  
- PlannedTask  
- Disruption  
- RecoverySession  


---

## Core Business Rules

- Task title is required  
- Each task belongs to one user  
- Each user has only one DailyPlan per day  
- Task status values:
  - Pending
  - Completed
- Recovery can only happen after a disruption  
- Recovery does not delete tasks  
- Recovery only moves or keeps pending tasks  
- Users can override system decisions  

---

## Architecture Overview

The project follows an API-first architecture with a service layer.

System flow:

User  
↓  
Raw Tasks  
↓  
Planning Engine (Behavior-aware)    
↓  
DailyPlan  
↓  
Disruption  
↓  
Recovery Engine  
↓  
Updated DailyPlan  

---

## Project Structure

config/  
Django project configuration

tasks/  
Core application (Tasks & Planning logic)

services/  
Business logic  
planner.py  
recovery.py

api/  
REST API

templates/  
Minimal web UI

static/  
Static files

---

## Technology Stack

Backend

- Django  
- Django REST Framework  

Database

- SQLite (MVP)  
- PostgreSQL (production)

Frontend (MVP)

- Django Templates

Future Mobile App

- React Native

---

## Design Principles

- Fast task capture  
- Simple user experience  
- Minimal cognitive load  
- Reliable recovery after disruption  
- **Behavioral design & healthy gamification**

---

## Project Goal

The goal of the MVP is to validate one key hypothesis:


Users need a fast, psychologically-supported way to recover their day after disruptions.

---

## Future Roadmap

Possible future features include:

- AI-based planning & coaching  
- Advanced behavioral nudges  
- Mobile application  
- Calendar integration  
- Analytics and insights  
- Deep gamification layers (XP, Streaks, Achievements)