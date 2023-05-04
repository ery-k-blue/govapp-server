from sqlalchemy import create_engine

engine = create_engine("mysql://root:password@localhost/mysql?charset=utf8")