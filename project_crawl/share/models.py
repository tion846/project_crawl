# https://docs.sqlalchemy.org/en/20/
# https://www.cnblogs.com/lsdb/p/9835894.html

# https://www.jianshu.com/p/c8952453b99a

from typing import Any, List
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship
from time import localtime, strftime
from datetime import datetime


class Base(DeclarativeBase):
    pass


# 定义映射类User，其继承上一步创建的Base
class Product(Base):
    __tablename__ = "Product"
    __table_args__ = {'sqlite_autoincrement': True}
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(64), nullable=False)
    Link = Column(String(256), nullable=False)
    Spec_Link = Column(String(256), nullable=False)
    Sale_Price = Column(String(8), nullable=False)
    Spec_Json = Column(String)
    Cdt = Column(DateTime, nullable=False)

    def __init__(self, name, link, spec_link, sale_price, **kw: Any):
        self.Name = name
        self.Link = link
        self.Spec_Link = spec_link
        self.Sale_Price = sale_price
        self.Cdt = datetime.now()
        super().__init__(**kw)

    # __repr__方法用于输出该类的对象被print()时输出的字符串，如果不想写可以不写
    def __repr__(self):
        id = self.Id if (self.Id) else 0
        return "<Product(Id='%d', Name='%s', Link='%s', Spec_Link='%s', Sale_Price='%s')>" % (
            id, self.Name, self.Link, self.Spec_Link, self.Sale_Price
        )


# class User(Base):
#     __tablename__ = "user_account"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))
#     fullname: Mapped[Optional[str]]
#     addresses: Mapped[List["Address"]] = relationship(
#         back_populates="user", cascade="all, delete-orphan"
#     )

#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


# class Address(Base):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped["User"] = relationship(back_populates="addresses")

#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
