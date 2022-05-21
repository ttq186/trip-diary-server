# from sqlalchemy.ext.declarative import declared_attr, as_declarative
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# @as_declarative()
# class Base:
#     @declared_attr
#     def __tablename__(cls) -> str:
#         """Generate __tablename__ in lowercase automatically."""
#         return cls.__name__.lower()
