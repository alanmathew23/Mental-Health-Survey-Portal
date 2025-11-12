CREATE DATABASE MentalWellness;
USE MentalWellness;

-- Student Table
CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Department VARCHAR(50) NOT NULL,
    YearOfStudy INT CHECK (YearOfStudy BETWEEN 1 AND 4)
);

-- Counselor Table
CREATE TABLE Counselor (
    CounselorID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
	Password VARCHAR(100) NOT NULL,
    Specialization VARCHAR(100)
);

-- Session Table with StartTime and EndTime added
CREATE TABLE Session (
    SessionID INT PRIMARY KEY auto_increment,
    StudentID INT,
    CounselorID INT,
    SessionDate DATE NOT NULL,
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,	
    Notes TEXT,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (CounselorID) REFERENCES Counselor(CounselorID)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CHECK (StartTime < EndTime)  -- Ensure start < end
);

-- MentalHealthResource Table
CREATE TABLE MentalHealthResource (
    ResourceID INT PRIMARY KEY,
    Title VARCHAR(200) NOT NULL,
    ResourceType VARCHAR(50) CHECK (ResourceType IN ('Article','Video','Podcast','Guide')),
    URL VARCHAR(255) UNIQUE
);

-- StudentResourceAccess Table
CREATE TABLE StudentResourceAccess (
    AccessID INT PRIMARY KEY,
    StudentID INT NULL,
    ResourceID INT NOT NULL,
    AccessDate DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ResourceID) REFERENCES MentalHealthResource(ResourceID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- WellnessSurvey Table
CREATE TABLE WellnessSurvey (
    SurveyID INT PRIMARY KEY,
    StudentID INT,
    SubmissionDate DATE NOT NULL,
    StressLevel INT CHECK (StressLevel BETWEEN 1 AND 10),
    SleepHours INT CHECK (SleepHours BETWEEN 0 AND 24),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- MentalHealthLog Table
CREATE TABLE MentalHealthLog (
    LogID INT PRIMARY KEY,
    StudentID INT,
    LogDate DATE NOT NULL,
    Mood VARCHAR(50) NOT NULL,
    Notes TEXT,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Insert Students
INSERT INTO Student VALUES 
(1, 'Aarav Sharma', 'aarav.sharma@pesu.edu','password','CSE', 2),
(2, 'Diya Rao', 'diya.rao@pesu.edu','password', 'ECE', 3),
(3, 'Rahul Menon', 'rahul.menon@pesu.edu','password', 'ME', 1),
(4, 'Sneha Patil', 'sneha.patil@pesu.edu','password', 'CSE', 4),
(5, 'Karan Nair', 'karan.nair@pesu.edu','password', 'EEE', 2),
(6, 'Demo_Studentr', 'demo@pesu.edu','Demo','password',1);

-- Insert Counselors
INSERT INTO Counselor VALUES
(1, 'Dr. Meera Iyer', 'meera.iyer@pesu.edu','password', 'Stress Management'),
(2, 'Dr. Arjun Rao', 'arjun.rao@pesu.edu','password', 'Anxiety'),
(3, 'Dr. Kavya Sharma', 'kavya.sharma@pesu.edu','password', 'Relationships'),
(4, 'Dr. Vivek Kulkarni', 'vivek.kulkarni@pesu.edu','password', 'Sleep Disorders'),
(5, 'Dr. Priya Menon', 'priya.menon@pesu.edu','password', 'Career Guidance'),
(6, 'Demo_Counselor', 'demo@pesu.edu','password','Demo');

-- Insert Sessions WITH time slots (non-overlapping for both students and counselors)
INSERT INTO Session VALUES
(1, 1, 1, '2025-08-01', '09:00:00', '10:00:00', 'Discussed exam stress'),
(2, 2, 2, '2025-08-05', '10:00:00', '11:00:00', 'Coping strategies for anxiety'),
(3, 3, 3, '2025-08-10', '11:00:00', '12:00:00', 'Managing peer pressure'),
(4, 4, 4, '2025-08-15', '12:00:00', '13:00:00', 'Improving sleep cycle'),
(5, 5, 5, '2025-08-20', '13:00:00', '14:00:00', 'Career planning discussion');
ALTER TABLE Session MODIFY SessionID INT AUTO_INCREMENT;

-- Insert Resources
INSERT INTO MentalHealthResource VALUES
(1, 'Mindfulness Basics', 'Article', 'https://wellness.org/mindfulness'),
(2, 'Yoga for Stress Relief', 'Video', 'https://wellness.org/yoga-stress'),
(3, 'Dealing with Exam Pressure', 'Guide', 'https://wellness.org/exam-guide'),
(4, 'Sleep Hygiene Podcast', 'Podcast', 'https://wellness.org/sleep-podcast'),
(5, 'Time Management Tips', 'Article', 'https://wellness.org/time-management');

-- Insert StudentResourceAccess
INSERT INTO StudentResourceAccess VALUES
(1, 1, 1, '2025-08-01'),
(2, 1, 2, '2025-08-02'),
(3, 2, 3, '2025-08-05'),
(4, 3, 4, '2025-08-10'),
(5, 4, 5, '2025-08-15');

-- Insert Wellness Surveys
INSERT INTO WellnessSurvey VALUES
(1, 1, '2025-08-01', 7, 6),
(2, 2, '2025-08-05', 6, 7),
(3, 3, '2025-08-10', 8, 5),
(4, 4, '2025-08-15', 5, 8),
(5, 5, '2025-08-20', 9, 4);

-- Insert Mental Health Logs
INSERT INTO MentalHealthLog VALUES
(1, 1, '2025-08-01', 'Stressed', 'Exams are overwhelming'),
(2, 2, '2025-08-05', 'Anxious', 'Upcoming project deadline'),
(3, 3, '2025-08-10', 'Confused', 'Peer group issues'),
(4, 4, '2025-08-15', 'Tired', 'Not sleeping well'),
(5, 5, '2025-08-20', 'Optimistic', 'Planning for future');

-- TRIGGERS --
-- TRIGGER 1 --
DELIMITER $$

CREATE TRIGGER after_resource_access_log
AFTER INSERT ON StudentResourceAccess
FOR EACH ROW
BEGIN
    DECLARE nextLogID INT;

    -- Compute next LogID safely (avoid referencing the same table in subquery directly)
    SELECT COALESCE(MAX(LogID), 0) + 1 INTO nextLogID 
    FROM (SELECT LogID FROM MentalHealthLog) AS temp;

    -- Insert log entry for student resource access
    IF NEW.StudentID IS NOT NULL THEN
        INSERT INTO MentalHealthLog (LogID, StudentID, LogDate, Mood, Notes)
        VALUES (
            nextLogID,
            NEW.StudentID,
            NEW.AccessDate,
            'Reflective',
            CONCAT('Accessed mental health resource ID: ', NEW.ResourceID)
        );
    END IF;
END$$

DELIMITER ;
-- TEST FOR TRIGGER --
INSERT INTO StudentResourceAccess (AccessID, StudentID, ResourceID, AccessDate)
VALUES (6, 2, 2, '2025-08-25');

SELECT * FROM MentalHealthLog;

-- TRIGGER 2 to prevent counselor AND student overlapping sessions

DROP TRIGGER IF EXISTS prevent_double_booking;
DELIMITER $$

CREATE TRIGGER prevent_double_booking
BEFORE INSERT ON Session
FOR EACH ROW
BEGIN
    DECLARE overlap_counselor INT;
    DECLARE overlap_student INT;

    -- Check counselor overlap
    SELECT COUNT(*) INTO overlap_counselor
    FROM Session
    WHERE CounselorID = NEW.CounselorID
      AND SessionDate = NEW.SessionDate
      AND (
        (NEW.StartTime < EndTime AND NEW.EndTime > StartTime)
      );

    -- Check student overlap
    SELECT COUNT(*) INTO overlap_student
    FROM Session
    WHERE StudentID = NEW.StudentID
      AND SessionDate = NEW.SessionDate
      AND (
        (NEW.StartTime < EndTime AND NEW.EndTime > StartTime)
      );

    IF overlap_counselor > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Counselor already has a session booked during this time slot.';
    END IF;

    IF overlap_student > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Student already has a session booked during this time slot.';
    END IF;

END$$

DELIMITER ;

-- TEST TRIGGER --

-- Valid insert - no overlap for student or counselor
INSERT INTO Session (SessionID, StudentID, CounselorID, SessionDate, StartTime, EndTime, Notes)
VALUES (6, 1, 2, '2025-09-01', '09:00:00', '10:00:00', 'Follow-up counseling session');

-- Overlapping insert - student overlap (should error)
INSERT INTO Session (SessionID, StudentID, CounselorID, SessionDate, StartTime, EndTime, Notes)
VALUES (7, 1, 3, '2025-09-01', '09:30:00', '10:30:00', 'Attempt overlapping booking for student');

-- Overlapping insert - counselor overlap (should error)
INSERT INTO Session (SessionID, StudentID, CounselorID, SessionDate, StartTime, EndTime, Notes)
VALUES (8, 2, 2, '2025-09-01', '09:30:00', '10:30:00', 'Attempt overlapping booking for counselor');

-- FUNCTIONS
-- function1 --
DELIMITER $$

CREATE FUNCTION GetStudentStressLevel(p_StudentID INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE latestStress INT;

    SELECT StressLevel
    INTO latestStress
    FROM WellnessSurvey
    WHERE StudentID = p_StudentID
    ORDER BY SubmissionDate DESC
    LIMIT 1;

    RETURN latestStress;
END$$

DELIMITER ;
-- test 1--
SELECT GetStudentStressLevel(1) AS LatestStressLevel;


 -- function 2--
DELIMITER $$

CREATE FUNCTION CountSessionsForCounselorOnDate(p_CounselorID INT, p_Date DATE)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE sessionCount INT;

    SELECT COUNT(*)
    INTO sessionCount
    FROM Session
    WHERE CounselorID = p_CounselorID
      AND SessionDate = p_Date;

    RETURN sessionCount;
END$$

DELIMITER ;
-- test 2--
SELECT CountSessionsForCounselorOnDate(2, '2025-08-05') AS SessionsOnDate


-- PROCEDURE --
-- procedure 1--
DELIMITER $$

CREATE PROCEDURE AddNewSession (
    IN p_SessionID INT,
    IN p_StudentID INT,
    IN p_CounselorID INT,
    IN p_SessionDate DATE,
    IN p_StartTime TIME,
    IN p_EndTime TIME,
    IN p_Notes TEXT,
    OUT p_Message VARCHAR(255)
)
BEGIN
    DECLARE overlapCount INT;

    -- Count overlapping sessions for counselor on the same date and time slot
    SELECT COUNT(*) INTO overlapCount
    FROM Session
    WHERE CounselorID = p_CounselorID
      AND SessionDate = p_SessionDate
      AND (
        (StartTime < p_EndTime AND EndTime > p_StartTime)  -- Overlapping time check
      );

    IF overlapCount > 0 THEN
        SET p_Message = 'Error: Counselor is already booked during this time slot.';
    ELSE
        INSERT INTO Session (SessionID, StudentID, CounselorID, SessionDate, StartTime, EndTime, Notes)
        VALUES (p_SessionID, p_StudentID, p_CounselorID, p_SessionDate, p_StartTime, p_EndTime, p_Notes);
        SET p_Message = 'Success: Session scheduled.';
    END IF;
END$$

DELIMITER ;
-- test for proc 1
SET @msg = 'success';
CALL AddNewSession(
    101,                -- p_SessionID
    5,                  -- p_StudentID
    3,                  -- p_CounselorID
    '2025-10-25',       -- p_SessionDate
    '10:00:00',         -- p_StartTime
    '11:00:00',         -- p_EndTime
    'Initial counseling session.', -- p_Notes
    @msg                -- p_Message (OUT)
);
SELECT @msg AS Result;




-- procedure 2--
DELIMITER $$

CREATE PROCEDURE UpdateMentalHealthLogMood (
    IN p_LogID INT,
    IN p_NewMood VARCHAR(50),
    IN p_NewNotes TEXT,
    OUT p_Message VARCHAR(255)
)
BEGIN
    IF EXISTS (SELECT 1 FROM MentalHealthLog WHERE LogID = p_LogID) THEN
        UPDATE MentalHealthLog
        SET Mood = p_NewMood,
            Notes = p_NewNotes
        WHERE LogID = p_LogID;
        
        SET p_Message = 'Success: Mental health log updated.';
    ELSE
        SET p_Message = 'Error: LogID not found.';
    END IF;
END$$

DELIMITER ;

-- call to procedures--


-- 2. UpdateMentalHealthLogMood example
CALL UpdateMentalHealthLogMood(3, 'Calm', 'Feeling better after meditation', @msg);
SELECT @msg;


-- FIXES FOR MENTALWELLNESS DATABASE

-- ========================================
-- FIX 1: Add AUTO_INCREMENT to Primary Keys (for future tables)
-- ========================================
-- Note: Can't alter existing tables with data without recreating them
-- For new deployments, modify the CREATE TABLE statements to include AUTO_INCREMENT

-- Example for future reference:
-- CREATE TABLE Student (
--     StudentID INT PRIMARY KEY AUTO_INCREMENT,
--     ...
-- );

-- ========================================
-- FIX 2: Make StudentID NOT NULL in StudentResourceAccess
-- ========================================
ALTER TABLE StudentResourceAccess
MODIFY COLUMN StudentID INT NOT NULL;

-- ========================================
-- FIX 3: Fix Trigger to use AUTO_INCREMENT approach
-- ========================================
DROP TRIGGER IF EXISTS after_resource_access_log;

DELIMITER $$

CREATE TRIGGER after_resource_access_log
AFTER INSERT ON StudentResourceAccess
FOR EACH ROW
BEGIN
    DECLARE nextLogID INT;

    -- Use a more concurrency-safe approach
    -- Get max LogID and add 1 in a single atomic operation
    SELECT IFNULL(MAX(LogID), 0) + 1 INTO nextLogID FROM MentalHealthLog;

    -- Insert log entry for student resource access
    IF NEW.StudentID IS NOT NULL THEN
        INSERT INTO MentalHealthLog (LogID, StudentID, LogDate, Mood, Notes)
        VALUES (
            nextLogID,
            NEW.StudentID,
            NEW.AccessDate,
            'Reflective',
            CONCAT('Accessed mental health resource ID: ', NEW.ResourceID)
        );
    END IF;
END$$

DELIMITER ;

-- ========================================
-- FIX 4: Add BEFORE UPDATE trigger for Session overlap prevention
-- ========================================
DROP TRIGGER IF EXISTS prevent_double_booking_update;

DELIMITER $$

CREATE TRIGGER prevent_double_booking_update
BEFORE UPDATE ON Session
FOR EACH ROW
BEGIN
    DECLARE overlap_counselor INT;
    DECLARE overlap_student INT;

    -- Check counselor overlap (exclude current session being updated)
    SELECT COUNT(*) INTO overlap_counselor
    FROM Session
    WHERE CounselorID = NEW.CounselorID
      AND SessionDate = NEW.SessionDate
      AND SessionID != NEW.SessionID  -- Exclude current session
      AND (
        (NEW.StartTime < EndTime AND NEW.EndTime > StartTime)
      );

    -- Check student overlap (exclude current session being updated)
    SELECT COUNT(*) INTO overlap_student
    FROM Session
    WHERE StudentID = NEW.StudentID
      AND SessionDate = NEW.SessionDate
      AND SessionID != NEW.SessionID  -- Exclude current session
      AND (
        (NEW.StartTime < EndTime AND NEW.EndTime > StartTime)
      );

    IF overlap_counselor > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Counselor already has a session booked during this time slot.';
    END IF;

    IF overlap_student > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Student already has a session booked during this time slot.';
    END IF;

END$$

DELIMITER ;

-- ========================================
-- FIX 5: Update AddNewSession procedure to check student overlaps
-- ========================================
DROP PROCEDURE IF EXISTS AddNewSession;

DELIMITER $$

CREATE PROCEDURE AddNewSession (
    IN p_SessionID INT,
    IN p_StudentID INT,
    IN p_CounselorID INT,
    IN p_SessionDate DATE,
    IN p_StartTime TIME,
    IN p_EndTime TIME,
    IN p_Notes TEXT,
    OUT p_Message VARCHAR(255)
)
BEGIN
    DECLARE overlapCounselor INT;
    DECLARE overlapStudent INT;

    -- Check overlapping sessions for counselor
    SELECT COUNT(*) INTO overlapCounselor
    FROM Session
    WHERE CounselorID = p_CounselorID
      AND SessionDate = p_SessionDate
      AND (
        (StartTime < p_EndTime AND EndTime > p_StartTime)
      );

    -- Check overlapping sessions for student
    SELECT COUNT(*) INTO overlapStudent
    FROM Session
    WHERE StudentID = p_StudentID
      AND SessionDate = p_SessionDate
      AND (
        (StartTime < p_EndTime AND EndTime > p_StartTime)
      );

    IF overlapCounselor > 0 THEN
        SET p_Message = 'Error: Counselor is already booked during this time slot.';
    ELSEIF overlapStudent > 0 THEN
        SET p_Message = 'Error: Student is already booked during this time slot.';
    ELSE
        INSERT INTO Session (SessionID, StudentID, CounselorID, SessionDate, StartTime, EndTime, Notes)
        VALUES (p_SessionID, p_StudentID, p_CounselorID, p_SessionDate, p_StartTime, p_EndTime, p_Notes);
        SET p_Message = 'Success: Session scheduled.';
    END IF;
END$$

DELIMITER ;

-- ========================================
-- FIX 6: Add indexes on foreign keys for better performance
-- ========================================
CREATE INDEX idx_session_student ON Session(StudentID);
CREATE INDEX idx_session_counselor ON Session(CounselorID);
CREATE INDEX idx_session_date ON Session(SessionDate);
CREATE INDEX idx_resource_access_student ON StudentResourceAccess(StudentID);
CREATE INDEX idx_resource_access_resource ON StudentResourceAccess(ResourceID);
CREATE INDEX idx_wellness_survey_student ON WellnessSurvey(StudentID);
CREATE INDEX idx_mental_health_log_student ON MentalHealthLog(StudentID);

-- ========================================
-- TESTING THE FIXES
-- ========================================

-- Test the updated trigger
INSERT INTO StudentResourceAccess (AccessID, StudentID, ResourceID, AccessDate)
VALUES (7, 3, 1, '2025-11-08');

SELECT * FROM MentalHealthLog WHERE StudentID = 3 ORDER BY LogDate DESC LIMIT 1;

-- Test the updated procedure with student overlap check
SET @msg = '';
CALL AddNewSession(
    102,
    1,  -- Student 1 who already has session 6 on 2025-09-01 from 09:00-10:00
    4,
    '2025-09-01',
    '09:30:00',  -- This should overlap with existing session
    '10:30:00',
    'Should fail due to student overlap',
    @msg
);
SELECT @msg AS Result;  -- Should return error message about student being booked

-- Test valid session booking
SET @msg = '';
CALL AddNewSession(
    103,
    2,
    4,
    '2025-11-10',
    '14:00:00',
    '15:00:00',
    'Valid session with no overlaps',
    @msg
);
SELECT @msg AS Result;  -- Should return success message

-- Test UPDATE trigger (try to update session to overlap)
-- First, check existing session 6
SELECT * FROM Session WHERE SessionID = 6;

-- Try to update it to overlap with itself on a different time (should work)
UPDATE Session 
SET StartTime = '11:00:00', EndTime = '12:00:00'
WHERE SessionID = 6;

-- Try to update it to overlap with another session (should fail)
-- Assuming there's another session for counselor 2 or student 1
UPDATE Session 
SET StartTime = '09:30:00', EndTime = '10:30:00'
WHERE SessionID = 6;  -- This should trigger an error if there's an overlap

SELECT 'All fixes applied successfully!' AS Status;
