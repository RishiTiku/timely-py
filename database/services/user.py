from ..models import Student, User, Faculty
from typing import List, Optional, Type, Union
from database.utils import find_all, P
from ..utils import create_one, create_many

async def create_student(student_data: dict):
    return await create_one(Student, student_data)

async def create_students(students_list_data: List[dict]):
    await create_many(Student, students_list_data)

async def create_faculty(faculty_data: dict):
    return await create_one(Student, faculty_data)

async def create_faculties(faculty_list_data: List[dict]):
    await create_many(Faculty, faculty_list_data)


async def find_all_users(projection_model: Optional[Type[P]] = None, write_to_file: bool = False) -> Optional[List[Union[User, P]]]:
    return await find_all(User, projection_model, write_to_file)

async def add_batch_to_user(user_batch_map: dict):
    pass
