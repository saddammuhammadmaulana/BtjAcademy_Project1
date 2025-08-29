from fastapi import APIRouter

from api.scheduler.service import Schedule

scheduler_router = APIRouter()
tag = ["Scheduler"]

@scheduler_router.post('/add_data', tags=tag)
def add_data(data: int):
    schedule = Schedule(data=data).add_data()
    return schedule