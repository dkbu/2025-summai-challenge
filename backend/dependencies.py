# Create a global instance or use a proper dependency pattern

from models import DiagramStorage, UserCounter


diagram_storage = DiagramStorage()
user_counter = UserCounter()


async def get_diagram_storage():
    return diagram_storage


async def get_user_counter():
    return user_counter