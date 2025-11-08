PESU DBMS Mini Project
# MentalWellness Database System

A comprehensive SQL-based project designed to model and manage a university mental wellness system. It tracks students, counselors, sessions, wellness surveys, mental health logs, and resource access—supporting consistency and automation through triggers, functions, and stored procedures.

***

## Overview

The **MentalWellness** database aims to maintain student mental health records, counselor sessions, resource interactions, wellness surveys, and logs in a structured, normalized format. It automates key actions like logging student resource usage and preventing double booking of counseling sessions.

***

## Requirements for GUI
```
pip install tkcalendar
```

## How to run
```
python mental_wellness_gui.py
```

## Database Schema

### 1. Student
Stores basic student information.

| Column | Type | Description |
|--------|------|-------------|
| StudentID | INT (PK) | Unique student identifier |
| Name | VARCHAR(100) | Student's full name |
| Email | VARCHAR(100) | Unique email ID |
| Department | VARCHAR(50) | Department or branch |
| YearOfStudy | INT | Between 1 and 4 |

### 2. Counselor
Tracks counselor details and specialization.

| Column | Type | Description |
|--------|------|-------------|
| CounselorID | INT (PK) | Unique counselor identifier |
| Name | VARCHAR(100) | Counselor's name |
| Email | VARCHAR(100) | Unique email ID |
| Specialization | VARCHAR(100) | Area of expertise |

### 3. Session
Represents booked counseling sessions.

| Column | Type | Description |
|--------|------|-------------|
| SessionID | INT (PK) | Unique session ID |
| StudentID | INT (FK→Student) | Linked student |
| CounselorID | INT (FK→Counselor) | Assigned counselor |
| SessionDate | DATE | Date of session |
| StartTime | TIME | Start time |
| EndTime | TIME | End time |
| Notes | TEXT | Session details |

**Constraints:**
- StartTime < EndTime  
- Cascading deletes for students  
- Prevents session overlap for both student and counselor via triggers and procedures

### 4. MentalHealthResource
Catalog of wellness materials.

| Column | Type | Description |
|--------|------|-------------|
| ResourceID | INT (PK) | Unique ID |
| Title | VARCHAR(200) | Resource title |
| ResourceType | ENUM(Article, Video, Podcast, Guide) | Type of resource |
| URL | VARCHAR(255) | Resource link |

### 5. StudentResourceAccess
Logs student interactions with resources.

| Column | Type | Description |
|--------|------|-------------|
| AccessID | INT (PK) | Unique access ID |
| StudentID | INT (FK→Student) | Linked student |
| ResourceID | INT (FK→Resource) | Accessed resource |
| AccessDate | DATE | Date of access |

### 6. WellnessSurvey
Voluntary student wellness self-assessment.

| Column | Type | Description |
|--------|------|-------------|
| SurveyID | INT (PK) | Unique survey ID |
| StudentID | INT (FK→Student) | Linked student |
| SubmissionDate | DATE | Date submitted |
| StressLevel | INT | Scale 1–10 |
| SleepHours | INT | Scale 0–24 |

### 7. MentalHealthLog
Chronological student mood logs.

| Column | Type | Description |
|--------|------|-------------|
| LogID | INT (PK) | Unique log ID |
| StudentID | INT (FK→Student) | Linked student |
| LogDate | DATE | Log date |
| Mood | VARCHAR(50) | Descriptive mood |
| Notes | TEXT | Log remarks |

***

## Triggers

### 1. `after_resource_access_log`
**Type:** AFTER INSERT on `StudentResourceAccess`  
**Function:** Automatically logs a “Reflective” mood entry whenever a student accesses a resource.

### 2. `prevent_double_booking`
**Type:** BEFORE INSERT on `Session`  
**Function:** Prevents overlapping booking for counselors or students.

### 3. `prevent_double_booking_update`
**Type:** BEFORE UPDATE on `Session`  
**Function:** Prevents modification of session details that would cause time overlap conflicts.

***

## Functions

### 1. `GetStudentStressLevel(p_StudentID)`
Returns the student’s most recent stress level from `WellnessSurvey`.

### 2. `CountSessionsForCounselorOnDate(p_CounselorID, p_Date)`
Returns the number of sessions assigned to a particular counselor on a given date.

***

## Stored Procedures

### 1. `AddNewSession(...)`
Schedules a new counseling session with double booking checks for both counselor and student.

**Checks performed:**
- Counselor overlap  
- Student overlap  

**Returns:**
- “Success: Session scheduled.”  
- “Error: Counselor/Student is already booked during this time slot.”

### 2. `UpdateMentalHealthLogMood(...)`
Updates a mental health log’s mood and notes, validating `LogID` existence.

***

## Performance Optimizations

Indexes were added for efficient join and lookup performance:
- `Session(StudentID)`
- `Session(CounselorID)`
- `Session(SessionDate)`
- `StudentResourceAccess(StudentID)`
- `StudentResourceAccess(ResourceID)`
- `WellnessSurvey(StudentID)`
- `MentalHealthLog(StudentID)`

***

## Testing Summary

Test coverage includes:
- Trigger execution for automatic log entries  
- Overlap prevention triggers on insert and update  
- Stored procedure logic for session booking  
- Stress level retrieval and counselor session count functions  

Example verification:
```sql
CALL AddNewSession(
    103, 2, 4, '2025-11-10', '14:00:00', '15:00:00',
    'Valid session with no overlaps', @msg
);
SELECT @msg;
```

***

## Future Improvements

- Add **AUTO_INCREMENT** to primary keys for scalability.  
- Integrate with front-end dashboards for real-time student wellness insights.  
- Include access auditing logs and counselor availability calendars.

***

## Author

Developed by **Aakanksha Nandi (PES2UG23CS008), Alan Mathew (PES2UG23CS049)**  
Course Project – *DBMS*  
Institution: PES University  
Year: 2025  

***