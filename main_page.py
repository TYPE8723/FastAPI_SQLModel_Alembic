from fastapi import FastAPI,Depends,HTTPException
from sqlmodel import select
from fastapi_main import app
from db import init_db,get_session
from models import Song,SongCreate,SongUpdate,MusicSales,MusicSalesCreateBase,MusicSalesUpdate# the tables to be migrated should be imported here
main_app = FastAPI(debug=True)

#moutning fastapi_main
main_app.mount('/tutorials',app)

# #APIRouting
# main_app.include_router(app, prefix="/tutorials", tags=['tryouts'])#comment out annotate line for APIRouter to work

@main_app.get("/test")
async def hello():
    return {"data":"Hello word"}

# @main_app.on_event("startup")#should be only used if alembic is not used
# def on_startup():
#     init_db()

@main_app.post('/createsong')
async def add_song(song:SongCreate,session = Depends(get_session)):
    song = Song(name = song.name,artist=song.artist)
    session.add(song)
    session.commit()
    session.refresh(song)
    return song

@main_app.patch('/updatesong/{id}')
async def update_song(id:int,song:SongUpdate,session = Depends(get_session)):
    #song = Song(song)
    #fetching data of given id
    # db_song = session.execute(select(Song).where(Song.id==id)).scalar_one_or_none()#<class 'models.Song'>
    db_song = session.get(Song,id)#<class 'models.Song'>
    if not db_song:
        raise HTTPException(status_code=404, detail="Hero not found")
    print(type(db_song))
    update_data = song.dict(exclude_unset=True)
    # print(update_data.items())
    for key,value in update_data.items():
        setattr(db_song,key,value)
    session.add(db_song)
    session.commit()
    session.refresh(db_song)
    return song


@main_app.delete('/delete/{id}')
async def update_song(id:int,session=Depends(get_session)):
    db_song = session.execute(select(Song).where(Song.id==id)).scalar_one_or_none()
    session.delete(db_song)
    session.commit()

@main_app.post('/create_sales')
async def add_sales(sale:MusicSalesCreateBase,session=Depends(get_session)):
    create_sale = MusicSales(**sale.dict())
    session.add(create_sale)
    session.commit()
    session.refresh(create_sale)
    return create_sale

@main_app.patch('/update_sales/{id}')
async def update_sales(id:int,sales:MusicSalesUpdate,session=Depends(get_session)):
    db_sales = session.execute(select(MusicSales).where(MusicSales.id==id)).scalar_one_or_none()
    update_data = sales.dict(exclude_unset=True)
    for key,value in update_data.items():
        setattr(db_sales,key,value)
    session.add(db_sales)
    session.commit()
    session.refresh(db_sales)
    return db_sales