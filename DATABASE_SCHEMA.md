# Database Schema

## User Model

- **id**: Integer, Primary Key
- **username**: String(150), Unique, Not Null
- **email**: String(150), Unique, Not Null
- **password_hash**: String(128), Not Null
- **expenses**: Relationship to Expense Model (One-to-Many)

## Expense Model

- **id**: Integer, Primary Key
- **user_id**: Integer, Foreign Key (`User.id`), Not Null
- **amount**: Float, Not Null
- **category**: String(50), Not Null
- **date**: Date, Not Null
- **description**: String(200), Optional

## Category Model (Optional)

- **id**: Integer, Primary Key
- **name**: String(50), Not Null
- **user_id**: Integer, Foreign Key (`User.id`), Not Null
- **expenses**: Relationship to Expense Model (One-to-Many)