
# ALEMBIC SETUP

How to setup alembic on a Fastapi application
Install the given packages
* alembic
* fastapi
* psycopg2-binary
* SQLAlchemy(not neccessary)
* sqlmodel
* uvicorn

1. Initialize the database with alembic Initialize
```
alembic init migrations
```
migrations is the name of folder to keep migration files

2. Import neccessary packages in "migrations/script.py.mako"
```
import sqlmodel
```

3. Import neccessary packages in "migrations/env.py"
* Import SQLModel
```
from sqlmodel import SQLModel
```
* Import models used in that project
```
from models import *
```
* Set target_metadata
```
target_metadata = SQLModel.metadata
```
* Set DB URL  for alembic.ini in env.py or directly change the vaue of sqlalchemy.url in alembic.ini
```
config.set_main_option("sqlalchemy.url",'postgresql+psycopg2://postgres:12345@localhost:5432/FASQL')
```

