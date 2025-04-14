import argparse

from conf.db import SessionLocal
from entity.models import Student, Grade, Group, Subject, Teacher

parser = argparse.ArgumentParser(description="Work with database")
parser.add_argument("--action", "-a")
parser.add_argument("--model", "-m")
parser.add_argument("--id")
parser.add_argument("--name", "-n")
parser.add_argument("--phone", "-p")
parser.add_argument("--email", "-e")
parser.add_argument("--grade", "-g")
parser.add_argument("--date", "-d")
parser.add_argument("--group_id", "-gi")
parser.add_argument("--teacher_id", "-ti")
args = parser.parse_args()


def select_action():
    session = SessionLocal()
    if not args.action:
        print("--action (-a) is compulsory argument")
        return

    if not args.model:
        print("--model (-m) is compulsory argument")
        return

    if args.model == "Teacher":
        if args.action == "create":
            if not args.name or not args.email:
                return "name and email are compulsory argument to create Teacher object"
            else:
                teacher = Teacher(name=args.name, email=args.email)
                session.add(teacher)
                session.commit()
        elif args.action == "list":
            teachers = session.query(Teacher).all()
            for item in teachers:
                print(item.name)
        elif args.action == "update":
            if not args.id or (not args.name and not args.email):
                print(
                    "--id and one of: --name (n), --email (-e), --phone (-p) are compulsory"
                )
            teacher = session.get(Teacher, args.id)
            if args.name:
                teacher.name = args.name
            if args.email:
                teacher.email == args.email
            if args.phone:
                teacher.phone = args.phone
            session.commit()
        elif args.action == "delete":
            if not args.id:
                print("--id is compulsory")
            teacher = session.get(Teacher, args.id)
            session.delete(teacher)
            session.commit()

    if args.model == "Student":
        if args.action == "create":
            if not args.name or not args.email or not args.group_id:
                return "name, group_id and email are compulsory argument to create Student object"
            else:
                student = Student(
                    name=args.name, email=args.email, group_id=args.group_id
                )
                session.add(student)
                session.commit()
        elif args.action == "list":
            students = session.query(Student).all()
            for item in students:
                print(item.name)
        elif args.action == "update":
            if not args.id or (
                not args.name
                and not args.email
                and not args.phone
                and not args.group_id
            ):
                print(
                    "--id and one of: --name (n), --email (-e), --phone (-p), --group_id (-gi) are compulsory"
                )
            student = session.get(Student, args.id)
            if args.name:
                student.name = args.name
            if args.email:
                student.email == args.email
            if args.phone:
                student.phone = args.phone
            if args.group_id:
                student.group_id = args.group_id
            session.commit()
        elif args.action == "delete":
            if not args.id:
                print("--id is compulsory")
            student = session.get(Student, args.id)
            session.delete(student)
            session.commit()

    if args.model == "Group":
        if args.action == "create":
            if not args.name:
                return "name is compulsory argument to create Group object"
            else:
                group = Group(name=args.name)
                session.add(group)
                session.commit()
        elif args.action == "list":
            groups = session.query(Group).all()
            for item in groups:
                print(item.name)
        elif args.action == "update":
            if not args.id or not args.name:
                print("--id and --name (n) are compulsory")
                return
            group = session.get(Group, args.id)
            group.name = args.name
            session.commit()
        elif args.action == "delete":
            if not args.id:
                print("--id is compulsory")
            group = session.get(Group, args.id)
            session.delete(group)
            session.commit()

    if args.model == "Subject":
        if args.action == "create":
            if not args.name:
                return "name is compulsory argument to create Group object"
            else:
                subject = (
                    Subject(name=args.name, teacher_id=args.teacher_id)
                    if args.teacher_id
                    else Subject(name=args.name)
                )
                session.add(subject)
                session.commit()
        elif args.action == "list":
            subjects = session.query(Subject).all()
            for item in subjects:
                print(item.name)
        elif args.action == "update":
            if not args.id or not args.name:
                print("--id and --name (n) are compulsory")
                return
            subject = session.get(Subject, args.id)
            subject.name = args.name
            session.commit()
        elif args.action == "delete":
            if not args.id:
                print("--id is compulsory")
            subject = session.get(Subject, args.id)
            session.delete(subject)
            session.commit()

    if args.model == "Grade":
        if args.action == "create":
            if not args.name:
                return "name is compulsory argument to create Group object"
            else:
                subject = (
                    Subject(name=args.name, teacher_id=args.teacher_id)
                    if args.teacher_id
                    else Subject(name=args.name)
                )
                session.add(subject)
                session.commit()
        elif args.action == "list":
            grades = session.query(Grade).all()
            for item in grades:
                print(
                    item.grade, "Student:", item.student_id, "Subject", item.subject_id
                )
        elif args.action == "update":
            if not args.id or not args.grade:
                print("--id and --name (n) are compulsory")
                return
            grade = session.get(Grade, args.id)
            grade.grade = args.grade
            session.commit()
        elif args.action == "delete":
            if not args.id:
                print("--id is compulsory")
            grade = session.get(Grade, args.id)
            session.delete(grade)
            session.commit()


select_action()
