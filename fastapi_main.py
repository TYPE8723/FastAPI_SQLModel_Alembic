from typing import Union,Annotated
from enum import Enum
from fastapi import FastAPI,Query,Path,Header,Cookie,APIRouter
from pydantic import BaseModel

app = FastAPI()
# app = APIRouter()

#class to create an enum option for validation
class animalEnum(Enum):
    dog ="GERMAN SHEPERD"
    cat = "PERSIAN CAT"
    hen = "BROILER HEN"

@app.get('/')
def read_root():
    return{"hello world"}

@app.get('/items/{item_id}/{item_name}')#path parameters
def read_item(item_id:int,item_name:str,q:Union[str,None]=None):
    return { "item_id":item_id,"q":q}

@app.get('/animals/{item}')#path parameters
def getanimal(item:animalEnum):
    if item is animalEnum.dog:
        return {'data':animalEnum.dog.name}
    if item is animalEnum.cat:
        return {'data':animalEnum.cat.name}
    if item is animalEnum.hen:
        return {'data':animalEnum.hen.name}
    
#query parameters
#When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
@app.get('/mamal/')
def mamal_id(name:str,id:int):
    return {'data':name+str(id)}

#optional query parameters
@app.get('/query/params')
def animals(name:str,family:str|None=None):
    return{
        'name':name,
        'family':family,
    }

#pydantic validation
class Item(BaseModel):
    item_name:str
    description:str|None = None
    item_id:int

@app.put('/items/detais/')
def item_det(item:Item):#pydantic validation
    dict_convert = item.dict()#pydantic validation returns a class object which is accessed by the varible as a dict
    return {'data':dict_convert}

#additional validation
@app.get('/itemsA/')
async def read_items(q: str|None = Query(default='alensebas',max_length=50)):#read_items(q: Annotated[str|None,Query(max_length=50)]=None)
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update(({'q':q}))
    return results

@app.get('/itemsB/')
#Using Annotated is recommended instead of the default value in function parameters, it is better for multiple reasons. 🤓
async def read_itemb(q:Annotated[str|None,Query(max_length=20,min_length=3)]="ALEN"):#regex="^fixedquery$"# remove none to make it required
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update(({'q':q}))
    return results

@app.get('/itemC/')
#And you can also define a default list of values if none are provided:
async def read_itemc(q:Annotated[list[str],Query()]=['foo','bar']):
    return{"q":q}


@app.get("/itemsD/")
async def read_items(
    q: Annotated[
        Union[str, None],
        Query(
            alias="item-query",#this is used to change the name of the variable in the arguments
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            regex="^fixedquery$",
            deprecated=True,#comment this to make the label "deprecated" endpoint disappear in endpoint
        ),
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#exclude the endpoint from docs ->https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi


# gt: greater than
# ge: greater than or equal
# lt: less than
# le: less than or equal
@app.get("/itemE/{item_id}")
async def read_itemsE(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.get("/itemsf/")
async def read_itemsf(user_agent: Annotated[Union[str, None], Header()] = None):
    return {"User-Agent": user_agent}

@app.get("/itemsg/")
async def read_itemsg(ads_id: Annotated[Union[str, None], Cookie()] = None):
    return {"ads_id": ads_id}