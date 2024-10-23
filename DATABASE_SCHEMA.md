# Database Schema

This document outlines the database schema for the Expense Tracker web application.

## Overview

The database consists of three primary models:

1. **User Model**
2. **Expense Model**
3. **Category Model**

The relationships between these models are designed to:

- Allow each user to manage their own expenses and categories.
- Ensure data integrity and support efficient querying.

## Models

### User Model

Represents the users of the application.

#### Fields

- `id`: Integer, Primary Key
- `username`: String(150), Unique, Not Null
- `email`: String(150), Unique, Not Null, Indexed
- `password_hash`: String(128), Not Null
- `created_at`: DateTime, Not Null, Defaults to current time
- `expenses`: Relationship to Expense Model (One-to-Many)
- `categories`: Relationship to Category Model (One-to-Many)
