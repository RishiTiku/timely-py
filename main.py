import asyncio
from database.dummy import get_student_objects, get_batch_objects, get_faculty_objects
from database.services import (
    create_students, create_batches, find_all_users,
    find_all_batches, join_user_batch_subscribers, create_faculty, create_faculties,
    create_recurring_events, find_all_events, find_all_recurring_events)

from database.config import connect_db, disconnect_db
from database.models.projections import UserIdNameProjection, BatchIdCodeProjection
from database.dummy import user_batch_mapping, get_recurring_event_objects
from database.migration_scripts import migrate_add_subjects_field, migrate_user_fields, migrate_batch_fields
from database.models import Event, RecurringEvent
import database.models as models_module
import inspect
from beanie import Document

async def main():
    await connect_db()
    # await find_all_batches(BatchIdCodeProjection, write_to_file=True)
    # print(*get_student_objects(), sep="\n")
    # print(*get_faculty_objects(), sep="\n")
    # print(get_batch_objects())"migrate_user_fields",
    # await create_batches(get_batch_objects())
    # await migrate_batch_fields()
    # await create_students(get_student_objects())
    # await create_faculties(get_faculty_objects())
    # await find_all_users(UserIdNameProjection, write_to_file=True)
    # await create_batches(get_batch_objects())
    # await find_all_batches(BatchIdCodeProjection, write_to_file=True)
    # await join_user_batch_subscribers(user_batch_mapping)
    # await create_recurring_events(get_recurring_event_objects())
    # print(get_recurring_event_objects())
    # await migrate_add_subjects_field()
    # await migrate_user_fields()
    # await create_recurring_events(get_recurring_event_objects())
    await find_all_events(write_to_file=True)
    # val = await ABC.find({}).to_list()
    # print(val)
    await disconnect_db()


# Standard Python entry point
if __name__ == "__main__":
    asyncio.run(main())


""" 
TODO
- Join Events to Batches
- Query Users to Events
- Join Users to Events
- Query Users to Events (subscribed + faculty)
- hello 

""" 