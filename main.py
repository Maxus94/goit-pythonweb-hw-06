from datetime import datetime

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
parser.add_argument("--group_id", "-gi")
parser.add_argument("--teacher_id", "-ti")
parser.add_argument("--student_id", "-si")
parser.add_argument("--subject_id", "-sj")
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
                print("name and email are compulsory argument to create Teacher object")
            else:
                try:
                    teacher = Teacher(name=args.name, email=args.email)
                    session.add(teacher)
                    session.commit()
                    print(f"Teacher {args.name} was created")
                except Exception as e:
                    print(e)
                finally:
                    session.close()
        elif args.action == "list":
            try:
                teachers = session.query(Teacher).all()
                for item in teachers:
                    print(item.name)
            except Exception as e:
                print(e)
            finally:
                session.close()
        elif args.action == "update":
            if not args.id or (not args.name and not args.email and not args.phone):
                print(
                    "--id and one of: --name (n), --email (-e), --phone (-p) are compulsory"
                )
                return
            try:
                teacher = session.get(Teacher, args.id)
                if teacher is None:
                    raise Exception(f"Teacher with ID {args.id} does not exist")
                if args.name:
                    teacher.name = args.name
                if args.email:
                    teacher.email == args.email
                if args.phone:
                    teacher.phone = args.phone
                session.commit()
                print(f"Teacher with ID {args.id} {teacher.name} was updated")
            except Exception as e:
                print(e)
            finally:
                session.close()
        elif args.action == "delete":
            if not args.id:
                print("--id is compulsory")
                return
            try:
                teacher = session.get(Teacher, args.id)
                if teacher is None:
                    raise Exception(f"Teacher with ID {args.id} does not exist")
                t_name = teacher.name
                session.delete(teacher)
                session.commit()
                print(f"Teacher with ID {args.id} {t_name} was deleted")
            except Exception as e:
                print(e)
            finally:
                session.close()

    if args.model == "Student":
        if args.action == "create":
            if not args.name or not args.email or not args.group_id:
                print(
                    "name, group_id and email are compulsory argument to create Student object"
                )
            else:
                try:
                    student = Student(
                        name=args.name,
                        email=args.email,
                        group_id=int(args.group_id),
                        phone=args.phone,
                    )
                    session.add(student)
                    session.commit()
                    print(f"Student {args.name} was created")
                except Exception as e:
                    print(e)
                finally:
                    session.close()
        elif args.action == "list":
            try:
                students = session.query(Student).all()
                for item in students:
                    print(item.name)
            except Exception as e:
                print(e)
            finally:
                session.close()
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
                return
            try:
                student = session.get(Student, args.id)
                if student is None:
                    raise Exception(f"There is no student with ID {args.id}")
                if args.name:
                    student.name = args.name
                if args.email:
                    student.email = args.email
                if args.phone:
                    student.phone = args.phone
                if args.group_id:
                    student.group_id = args.group_id
                session.commit()
                print(f"Student with ID {student.id} {student.name} was updated")
            except Exception as e:
                print(e)
            finally:
                session.close()
        elif args.action == "delete":
            if not args.id:
                print("--id is compulsory")
                return
            try:
                student = session.get(Student, args.id)
                if student is None:
                    raise Exception(f"There is no student with ID {args.id}")
                st_name = student.name
                session.delete(student)
                session.commit()
                print(f"Student with ID {args.id} {st_name} was deleted")
            except Exception as e:
                print(e)
            finally:
                session.close()

    if args.model == "Group":
        if args.action == "create":
            if not args.name:
                print("name is compulsory argument to create Group object")
            else:
                try:
                    group = Group(name=args.name)
                    session.add(group)
                    session.commit()
                    print(f"Group {group.name} was created")
                except Exception as e:
                    print(e)
                finally:
                    session.close()

        elif args.action == "list":
            try:
                groups = session.query(Group).all()
                for item in groups:
                    print(item.name)
            except Exception as e:
                print(e)

        elif args.action == "update":
            if not args.id or not args.name:
                print("--id and --name (n) are compulsory")
                return
            try:
                group = session.get(Group, args.id)
                if group is None:
                    raise Exception(f"There is no group with ID {args.id}")
                group.name = args.name
                session.commit()
                print(f"Group with ID {args.id} was updated")
            except Exception as e:
                print(e)
            finally:
                session.close()

        elif args.action == "delete":
            if not args.id:
                print("--id is compulsory")
                return
            try:
                group = session.get(Group, args.id)
                if group is None:
                    raise Exception(f"There is no group with ID {args.id}")
                gr_name = group.name
                session.delete(group)
                session.commit()
                print(f"Group with ID {args.id} {gr_name} was deleted")
            except Exception as e:
                print(e)
            finally:
                session.close()

    if args.model == "Subject":
        if args.action == "create":
            if not args.name or not args.teacher_id:
                print(
                    "name and teacher_id are compulsory arguments to create Group object"
                )
            else:
                try:
                    subject = (
                        Subject(name=args.name, teacher_id=int(args.teacher_id))
                        if args.teacher_id
                        else Subject(name=args.name)
                    )
                    session.add(subject)
                    session.commit()
                    print(f"Subject {subject.name} was created")
                except Exception as e:
                    print(e)
                finally:
                    session.close()

        elif args.action == "list":
            try:
                subjects = session.query(Subject).all()
                for item in subjects:
                    print(item.name)
            except Exception as e:
                print(e)
            finally:
                session.close()

        elif args.action == "update":
            if not args.id or not args.name:
                print(
                    "--id and one of --name (n) and --teacher_id (-ti) are compulsory"
                )
                return
            try:
                subject = session.get(Subject, args.id)
                if subject is None:
                    raise Exception(f"Subject with ID {args.id} does not exist")
                if subject.name:
                    subject.name = args.name
                if subject.teacher_id:
                    subject.teacher_id = args.teacher_id
                session.commit()
                print(f"Subject with ID {args.id} {subject.name} was updated")
            except Exception as e:
                print(e)
            finally:
                session.close

        elif args.action == "delete":
            if not args.id:
                print("--id is compulsory")
                return
            try:
                subject = session.get(Subject, args.id)
                if subject is None:
                    raise Exception(f"Subject with ID {args.id} does not exist")
                sj_name = subject.name
                session.delete(subject)
                session.commit()
                print(f"Subject with ID {args.id} {sj_name} was deleted")
            except Exception as e:
                print(e)
            finally:
                session.close()

    if args.model == "Grade":
        if args.action == "create":
            if not args.grade or not args.student_id:
                print(
                    "grade, student_is, subject_id are compulsory arguments to create Grade object"
                )
            else:
                try:
                    grade = Grade(
                        grade=int(args.grade),
                        student_id=args.student_id,
                        subject_id=args.subject_id,
                        date_received=datetime.now(),
                    )
                    session.add(grade)
                    session.commit()
                    print(
                        f"Grade {grade.grade} for student with ID {grade.student_id} subject ID {grade.subject_id} was added"
                    )
                except Exception as e:
                    print(e)
                finally:
                    session.close()

        elif args.action == "list":
            try:
                grades = session.query(Grade).all()
                for item in grades:
                    print(
                        item.grade,
                        "Student:",
                        item.student_id,
                        "Subject",
                        item.subject_id,
                    )
            except Exception as e:
                print(e)
            finally:
                session.close()

        elif args.action == "update":
            if not args.id or (
                not args.grade and not args.subject_id and not args.student_id
            ):
                print(
                    "--id and one of --grade (g), --student_id (-si), subject_id (-sj) are compulsory"
                )
                return
            try:
                grade = session.get(Grade, args.id)
                if grade is None:
                    raise Exception(f"There is no grade with ID {args.id}")
                if args.grade:
                    if int(args.grade) > 100 or int(args.grade) < 1:
                        raise Exception("Grade must be between 1 and 100")
                    grade.grade = args.grade
                if args.student_id:
                    grade.student_id = args.student_id
                if args.subject_id:
                    grade.subject_id = args.subject_id
                session.commit()
                print(f"Grade with ID {args.id} was updated")
            except Exception as e:
                print(e)
            finally:
                session.close()

        elif args.action == "delete":
            if not args.id:
                print("--id is compulsory")
                return
            try:
                grade = session.get(Grade, args.id)
                if grade is None:
                    raise Exception(f"Grade with ID {args.id} does not exist")
                session.delete(grade)
                session.commit()
                print(f"Grade with ID {args.id} was deleted")
            except Exception as e:
                print(e)
            finally:
                session.close()


select_action()
