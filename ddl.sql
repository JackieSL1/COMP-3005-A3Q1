create table if not exists students (
	student_id serial primary key,
	first_name varchar(50) not null,
	last_name varchar(50) not null,
	email varchar(50) not null unique,
	enrollment_date date
);