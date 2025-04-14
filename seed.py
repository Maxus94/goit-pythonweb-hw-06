import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.orm import Session

from conf.db import SessionLocal
from entity.models import Student, Grade, Group, Subject, Teacher

fake = Faker("uk_UA")
Faker.seed(42)


def seed_database():
    session = SessionLocal()
    try:
        groups = create_group(session)
        print("groups - ok")
        teachers = create_teacher(session)
        print("teachers - ok")
        subjects = create_subject(session, teachers)
        print("subjects - ok")
        students = create_student(session, groups)
        print("students - ok")
        grades = create_grades(session, students, subjects)
        print("grades - ok")
        session.commit()
        print("Database seeded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()


def create_group(session):
    group_name = ["3", "4", "MCS-1"]
    groups = []
    for name in group_name:
        group = Group(name=name)
        session.add(group)
        groups.append(group)
    session.flush()
    return groups


def create_teacher(session):
    teachers = []
    for i in range(3):
        teacher = Teacher(
            name=fake.name(), email=fake.email(), phone=fake.phone_number()
        )
        session.add(teacher)
        teachers.append(teacher)
    session.flush()
    return teachers


def create_subject(session, teachers: list):
    subject_names = [
        "JS",
        "React",
        "node.js",
        "Design",
        "Python",
    ]
    subjects = []
    for name in subject_names:
        subject = Subject(name=name, teacher=random.choice(teachers))
        session.add(subject)
        subjects.append(subject)
    session.flush()
    return subjects


def create_student(session, groups: list):
    students = []
    for i in range(30):
        student = Student(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            group=random.choice(groups),
        )
        session.add(student)
        students.append(student)
    session.flush()
    return students


def create_grades(session, students: list, subjects: list):
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now()
    for student in students:
        num_grades = random.randint(10, 20)
        for _ in range(num_grades):
            subject = random.choice(subjects)
            grade = Grade(
                student_id=student.id,
                subject_id=subject.id,
                grade=random.randint(60, 100),
                date_received=start_date
                + timedelta(days=random.randint(0, (end_date - start_date).days)),
            )
            session.add(grade)
    session.flush()


if __name__ == "__main__":
    seed_database()
