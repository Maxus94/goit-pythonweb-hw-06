from datetime import datetime

from sqlalchemy import ForeignKey, func, DateTime, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    students: Mapped[list["Student"]] = relationship(back_populates="group")


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)

    subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="SET NULL"), nullable=False
    )

    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("groups.id", ondelete="SET NULL"), nullable=False
    )
    group: Mapped["Group"] = relationship(back_populates="students")
    grades: Mapped[list["Grade"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"{self.name}"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    date_received: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    student: Mapped["Student"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship(back_populates="grades")

    def __repr__(self):
        return f"{str(self.grade)}"
