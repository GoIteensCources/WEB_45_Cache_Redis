from fastapi import Body, Depends, FastAPI, Request, status, Path,  APIRouter
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.notes import Note
from settings import get_db
import json


router = APIRouter()

@router.get("/get/cache")
async def get_redis_cache(request: Request):
    all_keys = await request.app.state.redis.keys("*")  
    data = await request.app.state.redis.get("all_notes")  
    print(data)
    return all_keys, data


@router.get("/notes")
async def all_notes(request: Request , db: AsyncSession = Depends(get_db)):

    redis_data = await request.app.state.redis.get("all_notes")  # type: ignore
    if redis_data:
        return {"notes from redis": redis_data}

    all_notes = await db.scalars(select(Note))
    data_all_notes = all_notes.all()
    count = await db.scalar(select(func.count()).select_from(Note))

    list_notes = [note.__dict__ for note in data_all_notes]
    for note in list_notes:
        note.pop("_sa_instance_state", None)

    print(list_notes)
    await request.app.state.redis.set("all_notes", json.dumps({"notes":list_notes, "count": count}))  # type: ignore
    
    return {"notes": data_all_notes, "counts notes": count}


@router.post("/notes")
async def create_note(
    request: Request ,
    db: AsyncSession = Depends(get_db),
    name: str = Body(...),
    description: str | None = Body(None, nullable=True),
):
    note = Note(name=name, description=description)
    db.add(note)
    await db.commit()
    await db.refresh(note)

    # Очищення кешу після створення нової нотатки
    await request.app.state.redis.delete("all_notes")  

    return note


@router.get("/notes/{note_id}")
async def get_note_by_id(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await db.get(Note, note_id)
    return note


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(request: Request, note_id: int, db: AsyncSession = Depends(get_db)):
    note = await db.get(Note, note_id)
    await db.delete(note)
    await db.commit()

    # Очищення кешу після створення нової нотатки
    await request.app.state.redis.delete("all_notes") 


@router.put("/notes/{note_id}")
async def update_notes(request: Request, db: AsyncSession = Depends(get_db), note_id: int = Path()):
    note = await db.get(Note, note_id)
    if note:
        note.done = True if note.done is False else False
        await db.commit()
        await db.refresh(note)

        # Очищення кешу після створення нової нотатки
        await request.app.state.redis.delete("all_notes") 
    return note
