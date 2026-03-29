-- ============================================================
-- MySQL Table Creation Script
-- CSC312 - Web Application Development
-- MIVA Open University, 2026
--
-- This script creates the database and the tbl_user table used
-- to store registered user credentials securely.
-- The password column stores hashed values only; plain text
-- passwords are never persisted (Viega & Messier, 2003).
-- ============================================================


-- Step 1: Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS csc312_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- Step 2: Select the database for use
USE csc312_db;


-- Step 3: Create the tbl_user table
-- Columns:
--   id         - Auto-incrementing primary key (unique per user)
--   username   - Unique string, max 50 characters, cannot be NULL
--   password   - Hashed password string (pbkdf2:sha256 output), max 255 chars
--   created_at - Timestamp automatically set when a record is inserted
CREATE TABLE IF NOT EXISTS tbl_user (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);


-- Step 4: Verify the table structure
-- Run this SELECT after creation to confirm columns and types
DESCRIBE tbl_user;


-- ============================================================
-- Sample verification query (optional):
-- After running the Flask app and registering a user, run
-- this to confirm the hashed password was stored correctly.
-- ============================================================
-- SELECT id, username, LEFT(password, 30) AS password_preview, created_at
-- FROM tbl_user;
