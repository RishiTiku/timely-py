import random, asyncio, uuid
from datetime import time
from typing import List, Optional
from faker import Faker
from bson import ObjectId

# Import your Beanie models
from database.models import Student, Faculty, Batch, Event  # Adjust import if needed
from database.config import connect_db

faker = Faker()

# Constants
TOTAL_STUDENTS = 100_000
TOTAL_FACULTY = 50_000
TOTAL_EVENTS = 100_000
BATCH_COUNT = 2_000
STUDENT_CHUNK = 500
FACULTY_CHUNK = 100
EVENT_CHUNK = 500
CHUNK_SIZE = 200

# Time range generator
def random_time_range():
    start_hour = random.randint(8, 16)
    end_hour = random.randint(start_hour + 1, min(start_hour + 3, 20))
    return time(start_hour), time(end_hour)

def format_time(t: time) -> str:
    return t.strftime("%H:%M")

def generate_code(prefix: str) -> str:
    return f"{prefix.upper()}-{uuid.uuid4().hex}"

# Generate batches
def generate_batches() -> List[Batch]:
    return [
        Batch(
            id=ObjectId(),
            name=f"{faker.word().capitalize()} Batch",
            code=generate_code("BATCH"),
            description=faker.sentence(),
            participants=[],
            events=[],
            live_events=[]
        ) for _ in range(BATCH_COUNT)
    ]

# Generate students
def generate_students(count: int) -> List[Student]:
    return [
        Student(
            id=ObjectId(),
            name=faker.name(),
            email=faker.unique.email(),
            password="12345678",
            uid=generate_code("UID"),
            semester=random.randint(1, 8),
            division=random.choice(["A", "B", "C", "D", "E", "F"]),
            passout=random.randint(2025, 2028),
            in_batches=[]
        ) for _ in range(count)
    ]

# Generate faculties
def generate_faculty(count: int) -> List[Faculty]:
    return [
        Faculty(
            id=ObjectId(),
            name=faker.name(),
            email=faker.unique.email(),
            password="12345678",
            code=generate_code("FAC"),
            default_room=None,
            in_batches=[],
            faculty_events=[]
        ) for _ in range(count)
    ]

# Async insert
async def insert_in_chunks(model, data, chunk_size=CHUNK_SIZE):
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        print(f"Inserting {model.__name__}: {i + 1} to {i + len(chunk)}")
        await model.insert_many(chunk)

# Main driver
async def bulk_inserts():
    await connect_db()
    print("Creating batches...")
    batches = generate_batches()
    batch_map = {b.id: b for b in batches}

    print("Creating students...")
    students = generate_students(TOTAL_STUDENTS)
    for s in students:
        assigned_batches = random.sample(batches, k=random.randint(1, 10))
        s.in_batches = [b.id for b in assigned_batches]
        for b in assigned_batches:
            batch_map[b.id].participants.append(s.id)

    print("Creating faculty...")
    faculties = generate_faculty(TOTAL_FACULTY)
    for f in faculties:
        assigned_batches = random.sample(batches, k=random.randint(1, 10))
        f.in_batches = [b.id for b in assigned_batches]
        for b in assigned_batches:
            batch_map[b.id].participants.append(f.id)

    print("Creating events...")
    events = []
    for _ in range(TOTAL_EVENTS):
        selected_batches = random.sample(batches, k=random.randint(1, 3))
        selected_faculty = random.sample(faculties, k=random.randint(1, 2))
        start, end = random_time_range()

        event = Event(
            id=ObjectId(),
            start_time=format_time(start),
            end_time=format_time(end),
            online_links=[faker.url()],
            description=faker.sentence(),
            batches=[b.id for b in selected_batches],
            faculties=[f.id for f in selected_faculty],
            subjects=[],
            rooms=[]
        )
        events.append(event)

        for b in selected_batches:
            batch_map[b.id].events.append(event.id)
        for f in selected_faculty:
            f.faculty_events.append(event.id)

    print("Bulk inserting everything...")
    await insert_in_chunks(Batch, list(batch_map.values()))
    await insert_in_chunks(Student, students)
    await insert_in_chunks(Faculty, faculties)
    await insert_in_chunks(Event, events)

    print("Done inserting everything.")
