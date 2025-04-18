from sqlalchemy import select, func, desc, Float
from sqlalchemy.orm import Session

from conf.db import SessionLocal
from entity.models import Student, Grade, Subject, Teacher, Group


def select_1(session):
    query = (
        select(
            Student, func.round(func.avg(Grade.grade), 2).cast(Float).label("avg_grade")
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(query).all()


def select_2(session, subject):
    query_id = select(Subject.id).where(Subject.name == subject).scalar_subquery()
    query = (
        select(
            Student, func.round(func.avg(Grade.grade), 2).cast(Float).label("avg_grade")
        )
        .join(Grade)
        .where(Grade.subject_id == query_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )

    return session.execute(query).all()


def select_3(session, subject):
    subject_id = select(Subject.id).where(Subject.name == subject).scalar_subquery()
    query = (
        select(func.round(func.avg(Grade.grade), 2).cast(Float), Student.group_id)
        .join(Student)
        .where(Student.group_id == Group.id, Grade.subject_id == subject_id)
        .group_by(Student.group_id)
        .order_by((Student.group_id))
    )
    return session.execute(query).all()


def select_4(session):
    query = select(func.round(func.avg(Grade.grade), 2).cast(Float))
    return session.execute(query).scalar()


def select_5(session, teacher):
    teacher_id = select(Teacher.id).where(Teacher.name == teacher).scalar_subquery()
    query = select(Subject.name).where(Subject.teacher_id == teacher_id)
    return session.execute(query).all()


def select_6(session, group):
    group_id = select(Group.id).where(Group.name == group).scalar_subquery()
    query = select(Student.name).where(Student.group_id == group_id)
    return session.execute(query).all()


def select_7(session, subject, group):
    subject_id = select(Subject.id).where(Subject.name == subject).scalar_subquery()
    group_id = select(Group.id).where(Group.name == group).scalar_subquery()
    query = (
        select(Student.name, Grade.grade)
        .join(Grade)
        .where(Grade.subject_id == subject_id, Student.group_id == group_id)
    )
    return session.execute(query).all()


def select_8(session, teacher):
    teacher_id = select(Teacher.id).where(Teacher.name == teacher).scalar_subquery()
    query = (
        select(func.round(func.avg(Grade.grade), 2).cast(Float))
        .join(Subject)
        .where(Subject.teacher_id == teacher_id)
    )
    return session.execute(query).all()


def select_9(session, student):
    student_id = select(Student.id).where(Student.name == student).scalar_subquery()
    query = (
        select(Subject.name)
        .join(Grade)
        .where(Grade.student_id == student_id)
        .group_by(Subject.id)
    )
    return session.execute(query).all()


def select_10(session, student, teacher):
    student_id = select(Student.id).where(Student.name == student).scalar_subquery()
    teacher_id = select(Teacher.id).where(Teacher.name == teacher).scalar_subquery()
    query = (
        select(Subject.name)
        .join(Grade)
        .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .group_by(Subject.name)
    )
    return session.execute(query).all()


def select_x1(session, student, teacher):
    teacher_id = select(Teacher.id).where(Teacher.name == teacher).scalar_subquery()
    student_id = select(Student.id).where(Student.name == student).scalar_subquery()
    query = (
        select(func.round(func.avg(Grade.grade), 2).cast(Float))
        .join(Subject)
        .where(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
    )
    return session.execute(query).scalar()


def select_x2(session, subject, group):
    subject_id = select(Subject.id).where(Subject.name == subject).scalar_subquery()
    group_id = select(Group.id).where(Group.name == group).scalar_subquery()
    last_grades = (
        select(func.max(Grade.date_received).label("last_date"))
        .join(Student)
        .where(Grade.subject_id == subject_id, Student.group_id == group_id)
        .scalar_subquery()
    )

    query = (
        select(Student.name, Grade.grade)
        .join(Grade, Student.id == Grade.student_id)
        .where(
            Grade.subject_id == subject_id,
            Student.group_id == group_id,
            Grade.date_received == last_grades,
        )
    )

    return session.execute(query).all()


if __name__ == "__main__":
    session = SessionLocal()
    subject = "Python"
    teacher = "Адам Литвин"
    student = "Юхим Голик"
    group = "MCS-1"

    result_1 = select_1(session)
    print("5 студентів з найбільшим середнім балом з усіх предметів")
    for item in result_1:
        print(f"{item[0]} average grade - {item[1]}")
    print()

    result_2 = select_2(session, subject)
    print(
        f"Студент з найбільшим середнім баломом з предмету {subject} - {result_2[0][0]}, average grade {result_2[0][1]}"
    )
    print()

    result_3 = select_3(session, subject)
    print(f"Середній бал з предмету {subject} за групами:")
    for item in result_3:
        print(f" Середній бал в групі з ID {item[1]} - {item[0]}")
    print()

    result_4 = select_4(session)
    print(f"Середній бал на потоці - {result_4}")
    print()

    result_5 = select_5(session, teacher)
    print(f"Курси, які читає викладач {teacher} - {result_5}")
    print()

    result_6 = select_6(session, group)
    print(f"Студенти групи {group}: {result_6}")
    print()

    result_7 = select_7(session, subject, group)
    print(f"Оцінки студентів групи {group} з {subject}")
    for item in result_7:
        print(f"{item[0]} - {item[1]}")
    print()

    result_8 = select_8(session, teacher)
    print(f"Середній бал, який ставить {teacher} зі своїх предметів - {result_8[0][0]}")
    print()

    result_9 = select_9(session, student)
    print(f"Курси, які відвідує {student}: {result_9}")
    print()

    result_10 = select_10(session, student, teacher)
    print(f"Курси, які студенту {student} читає викладач {teacher}: {result_10}")
    print()

    result_x1 = select_x1(session, student, teacher)
    print(
        f"Середній бал студента {student}, виставлений викладачем {teacher} - {result_x1}"
    )
    print()

    result_x2 = select_x2(session, subject, group)
    print(
        f"Оцінки студентів групи {group} з предмета {subject} на останньому занятті: {result_x2}"
    )
