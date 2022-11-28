from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://admin:YSIEAVvV@mysql-97755-0.cloudclusters.net:19995"
engine = create_engine(DATABASE_URL+'/Cursos')
engineSub = create_engine(DATABASE_URL+'/Alumnos')
meta = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionSubLocal = sessionmaker(autocommit=False, autoflush=False, bind=engineSub)
Base = declarative_base()