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
    return session.execute(query).all()


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
    return session.execute(query).all()


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
    result_7 = select_x1(session, "Юхим Голик", "Адам Литвин")
    print(result_7)
