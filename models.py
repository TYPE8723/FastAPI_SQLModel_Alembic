from sqlmodel import SQLModel,Field,PrimaryKeyConstraint,ForeignKeyConstraint,Relationship
from typing import Optional
#ref - > https://testdriven.io/blog/fastapi-sqlmodel/
class SongBase(SQLModel):
    name:str
    artist:str

class Song(SongBase,table =True):
    id:int = Field(default = None,primary_key=True)
    musicsales:Optional["MusicSales"] = Relationship(back_populates="songs")

class SongCreate(SongBase):
    pass

class SongUpdate(SQLModel):
    name: Optional[str]
    artist: Optional[str]

class MusicSales(SQLModel,table = True):
    __tablename__ = "music_sales"
    __table_args__ = (
        PrimaryKeyConstraint("id",name="music_id_pkey"),
        ForeignKeyConstraint(['song_id'],['song.id'],name="song_id_fk")
    )
    id:int = Field(default = None,primary_key=True)
    max_week_sales:Optional[int] = Field(default=0)
    sales_count:int = Field(nullable=False)
    song_id:int = Field(nullable=False)#Field(default=None, foreign_key="team.id")
    songs:Optional["Song"] = Relationship(back_populates="musicsales")


class MusicSalesCreateBase(SQLModel):
    max_week_sales:Optional[int] = None
    sales_count:int
    song_id:int

class MusicSalesUpdate(SQLModel):
    max_week_sales:Optional[int] = None
    sales_count:Optional[int]= None