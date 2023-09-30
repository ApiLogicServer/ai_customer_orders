# coding: utf-8
from sqlalchemy import CheckConstraint, Column, DECIMAL, Date, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  September 28, 2023 10:28:25
# Database: sqlite:////Users/val/dev/ApiLogicServer/ApiLogicServer-dev/servers/ai_customer_orders/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################

from safrs import SAFRSBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Customer(SAFRSBase, Base):
    __tablename__ = 'Customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'
    __table_args__ = (
        CheckConstraint('Balance <= CreditLimit'),
    )

    CustomerID = Column(Integer, primary_key=True)
    FirstName = Column(Text, nullable=False)
    LastName = Column(Text, nullable=False)
    Balance : DECIMAL = Column(DECIMAL)
    CreditLimit : DECIMAL = Column(DECIMAL)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderList : Mapped[List["Order"]] = relationship(back_populates="Customer")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Product(SAFRSBase, Base):
    __tablename__ = 'Products'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'
    __table_args__ = (
        CheckConstraint('UnitPrice >= 0'),
    )

    ProductID = Column(Integer, primary_key=True)
    ProductName = Column(Text, nullable=False)
    UnitPrice : DECIMAL = Column(DECIMAL)

    # parent relationships (access parent)

    # child relationships (access children)
    ItemList : Mapped[List["Item"]] = relationship(back_populates="Product")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Order(SAFRSBase, Base):
    __tablename__ = 'Orders'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    OrderID = Column(Integer, primary_key=True)
    CustomerID = Column(ForeignKey('Customers.CustomerID'))
    OrderDate = Column(Date)
    ShipDate = Column(Date)
    AmountTotal : DECIMAL = Column(DECIMAL)
    Notes = Column(Text)

    # parent relationships (access parent)
    Customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    ItemList : Mapped[List["Item"]] = relationship(back_populates="Order")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Item(SAFRSBase, Base):
    __tablename__ = 'Items'
    _s_collection_name = 'Item'  # type: ignore
    __bind_key__ = 'None'

    ItemID = Column(Integer, primary_key=True)
    OrderID = Column(ForeignKey('Orders.OrderID'))
    ProductID = Column(ForeignKey('Products.ProductID'))
    Quantity = Column(Integer)
    Amount : DECIMAL = Column(DECIMAL)
    UnitPrice : DECIMAL = Column(DECIMAL)

    # parent relationships (access parent)
    Order : Mapped["Order"] = relationship(back_populates=("ItemList"))
    Product : Mapped["Product"] = relationship(back_populates=("ItemList"))

    # child relationships (access children)

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_
