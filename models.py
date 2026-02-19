from sqlalchemy import Column, Integer, String, Date, Time, Float
from database import Base

class Plan(Base):
    __tablename__ = "plans"

    plan_idx = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    month = Column(Integer)
    item_number = Column(String(100))
    item_name = Column(String(100))
    inventory = Column(Integer)
    model = Column(String(100))
    process = Column(String(100))
    price = Column(Float)
    account_idx = Column(Integer)

class Production(Base):
    __tablename__ = "productions"

    production_idx = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    line = Column(String)
    operator = Column(String(100))
    item_number = Column(String(100))
    item_name = Column(String(100))
    model = Column(String(100))
    target_quantity = Column(Integer)
    produced_quantity = Column(Integer)
    production_efficiency = Column(Integer)
    process = Column(String(100))
    operating_time = Column(Time)
    non_operating_time = Column(Time)
    shift = Column(String(100))
    line_efficiency = Column(Integer)
    specification = Column(String(100))
    account_idx = Column(Integer)

class InventoryManagement(Base):
    __tablename__ = "inventory_managements"

    inventory_idx = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    item_number = Column(String(100))
    item_name = Column(String(100))
    price = Column(Float)
    basic_quantity = Column(Integer)
    basic_amount = Column(Float)
    in_quantity = Column(Integer)
    in_amount = Column(Float)
    defective_in_quantity = Column(Integer)
    defective_in_amount = Column(Float)
    out_quantity = Column(Integer)
    out_amount = Column(Float)
    adjustment_quantity = Column(Integer)
    current_quantity = Column(Integer)
    current_amount = Column(Float)
    lot_current_quantity = Column(Integer)
    difference_quantity = Column(Integer)
    account_idx = Column(Integer)

class Material(Base):
    __tablename__ = "materials"

    material_idx = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    client = Column(String(100))
    item_number = Column(String(100))
    item_name = Column(String(100))
    item_category = Column(String(100))
    model = Column(String(100))
    process = Column(String(100))
    quantity = Column(Integer)
    account_idx = Column(Integer)

class MaterialPlan(Base):
    __tablename__ = "material_plans"

    plan_idx = Column(Integer, primary_key=True, index=True, autoincrement=True)
    year = Column(Integer)
    month = Column(Integer)
    business_plan = Column(Float)
    business_amount = Column(Float)
    business_achievement_rate = Column(Float)
    account_idx = Column(Integer, default=1)

class MaterialInven(Base):
    __tablename__ = "material_invens"

    materialinven_idx = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    item_number = Column(String(100))
    item_name = Column(String(100))
    item_category = Column(String(100))
    price = Column(Float)
    process = Column(String(100))
    client = Column(String(100))
    model = Column(String(100))
    overall_status_quantity = Column(Integer)
    overall_status_amount = Column(Float)
    account_idx = Column(Integer)

class MaterialInOutManagement(Base):
    __tablename__ = "material_in_out_managements"

    materialinout_idx = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    statement_number = Column(String(100))
    client = Column(String(100))
    delivery_quantity = Column(Integer) 
    defective_quantity = Column(Integer) 
    settlement_quantity = Column(Integer) 
    supply_amount = Column(Float) 
    vat = Column(Float)
    total_amount = Column(Float) 
    purchase_category = Column(String(100))
    account_idx = Column(Integer)

class MaterialInvenManagement(Base):
    __tablename__ = "material_invens_managements"

    materialinvenmanage_idx = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    item_number = Column(String(100))
    item_name = Column(String(100))
    price = Column(Float)
    basic_quantity = Column(Integer)
    basic_amount = Column(Float)
    in_quantity = Column(Integer)
    in_amount = Column(Float)
    defective_in_quantity = Column(Integer)
    defective_in_amount = Column(Float)
    out_quantity = Column(Integer)
    out_amount = Column(Float)
    adjustment_quantity = Column(Integer)
    current_quantity = Column(Integer)
    current_amount = Column(Float)
    lot_current_quantity = Column(Integer)
    difference_quantity = Column(Integer)
    account_idx = Column(Integer)