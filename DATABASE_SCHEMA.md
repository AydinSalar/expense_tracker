Database Schema

User Model

	•	id: Integer, Primary Key
	•	username: String(150), Unique, Not Null
	•	email: String(150), Unique, Not Null, Indexed
	•	password_hash: String(128), Not Null
	•	created_at: DateTime, Not Null, Default to current time
	•	expenses: Relationship to Expense Model (One-to-Many)
	•	categories: Relationship to Category Model (One-to-Many)

Expense Model

	•	id: Integer, Primary Key
	•	user_id: Integer, Foreign Key to User.id, Not Null
	•	category_id: Integer, Foreign Key to Category.id, Not Null
	•	amount: Numeric(10, 2), Not Null
	•	date: Date, Not Null
	•	description: String(200), Optional

Category Model

	•	id: Integer, Primary Key
	•	name: String(50), Not Null
	•	user_id: Integer, Foreign Key to User.id, Not Null
	•	expenses: Relationship to Expense Model (One-to-Many)
	•	Unique Constraint: On ('name', 'user_id') to prevent duplicate category names for the same user
