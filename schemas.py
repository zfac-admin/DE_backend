from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class PlanCreate(BaseModel):
    year: int
    month: int
    item_number: str
    item_name: str
    inventory: int
    model: str
    process: str
    price: float
    account_idx: int = 1

class PlanBase(BaseModel):
    plan_idx: int
    year: int
    month: int
    item_number: str
    item_name: str
    inventory: int
    model: str
    process: str
    price: float
    account_idx: int = 1

class PlanResponse(BaseModel):
    year: int
    month: int
    prod_plan: float
    business_plan: float
    prod_amount: float
    business_amount: float
    production_achievement_rate: float
    business_achievement_rate: float

class PlanResponse2(BaseModel):
    year: int
    month: int
    process: str
    previous_amount: float
    current_amount: float
    growth_rate: float

class PlanUpdate(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    item_number: Optional[str] = None
    item_name: Optional[str] = None
    inventory: Optional[int] = None
    model: Optional[str] = None
    process: Optional[str] = None
    price: Optional[float] = None
    
    class Config:
        orm_mode = True

class ProductionCreate(BaseModel):
    date: date
    line: Optional[str] = None
    operator: Optional[str] = None
    item_number: str
    item_name: str
    model: str
    target_quantity: int
    produced_quantity: int
    production_efficiency: int
    process: str
    operating_time: Optional[time] = None
    non_operating_time: Optional[time] = None
    shift: str
    line_efficiency: int
    specification: str
    account_idx: int = 1

class ProductionBase(BaseModel):
    production_idx: int
    date: date
    line: Optional[str] = None
    operator: Optional[str] = None
    item_number: str
    item_name: str
    model: str
    target_quantity: int
    produced_quantity: int
    production_efficiency: int
    process: str
    operating_time: Optional[time] = None
    non_operating_time: Optional[time] = None
    shift: str
    line_efficiency: int
    specification: str
    account_idx: int = 1

class ProductionResponse(BaseModel):
    year: int
    month: int
    production_efficiency: int
    line_efficiency: int

class ProductionUpdate(BaseModel):
    date: Optional[date] 
    line: Optional[str] = None
    operator: Optional[str] = None
    item_number: Optional[str] = None
    item_name: Optional[str] = None
    model: Optional[str] = None
    target_quantity: Optional[int] = None
    produced_quantity: Optional[int] = None
    production_efficiency: Optional[int] = None
    process: Optional[str] = None
    operating_time: Optional[time] = None
    non_operating_time: Optional[time] = None
    shift: Optional[str] = None
    line_efficiency: Optional[int] = None
    specification: Optional[str] = None

    class Config:
        orm_mode = True

class InventoryManagementCreate(BaseModel):
    date: date
    item_number: str
    item_name: str
    price: float
    basic_quantity: int
    basic_amount: float
    in_quantity: int
    in_amount: float
    defective_in_quantity: int
    defective_in_amount: float
    out_quantity: int
    out_amount: float
    adjustment_quantity: int
    current_quantity: int
    current_amount: float
    lot_current_quantity: int
    difference_quantity: int
    account_idx: int = 1

class InventoryManagementBase(BaseModel):
    inventory_idx: int
    date: date
    item_number: str
    item_name: str
    price: float
    basic_quantity: int
    basic_amount: float
    in_quantity: int
    in_amount: float
    defective_in_quantity: int
    defective_in_amount: float
    out_quantity: int
    out_amount: float
    adjustment_quantity: int
    current_quantity: int
    current_amount: float
    lot_current_quantity: int
    difference_quantity: int
    account_idx: int = 1

class InventoryManagementUpdate(BaseModel):
    date: Optional[date]
    item_number: Optional[str]
    item_name: Optional[str]
    price: Optional[float]
    basic_quantity: Optional[int]
    basic_amount: Optional[float]
    in_quantity: Optional[int]
    in_amount: Optional[float]
    defective_in_quantity: Optional[int]
    defective_in_amount: Optional[float]
    out_quantity: Optional[int]
    out_amount: Optional[float]
    adjustment_quantity: Optional[int]
    current_quantity: Optional[int]
    current_amount: Optional[float]
    lot_current_quantity: Optional[int]
    difference_quantity: Optional[int]

    class Config:
        orm_mode = True

class MaterialCreate(BaseModel):
    date: date
    client: str
    item_number: str
    item_name: str
    item_category: str
    model: str
    process: str
    quantity: int
    account_idx: int = 1

class MaterialBase(BaseModel):
    material_idx: int
    date: date
    client: str
    item_number: str
    item_name: str
    item_category: str
    model: str
    process: str
    quantity: int
    account_idx: int = 1

class MaterialResponse(BaseModel):
    year: int
    month: int
    client: str
    previous_amount: float
    current_amount: float
    growth_rate: Optional[float] = None

class MaterialResponse2(BaseModel):
    year: int
    month: int
    business_plan: float
    business_amount: float
    business_achievement_rate: float

class MaterialUpdate(BaseModel):
    date: Optional[date]
    client: Optional[str] = None
    item_number: Optional[str] = None
    item_name: Optional[str] = None
    item_category: Optional[str] = None
    model: Optional[str] = None
    process: Optional[str] = None
    quantity: Optional[int] = None
    
    class Config:
        orm_mode = True

class MaterialInvenCreate(BaseModel):
    date: date
    item_number: str
    item_name: str
    price: float
    item_category: str
    process: str
    client: str
    model: str
    overall_status_quantity: int
    overall_status_amount: float
    account_idx: int = 1

class MaterialInvenBase(BaseModel):
    materialinven_idx:int
    date: date
    item_number: str
    item_name: str
    price: float
    item_category: str
    process: str
    client: str
    model: str
    overall_status_quantity: int
    overall_status_amount: float
    account_idx: int = 1

class MaterialInOutManagementCreate(BaseModel):
    date: date
    statement_number: str
    client: str
    delivery_quantity: int 
    defective_quantity: int 
    settlement_quantity: int 
    supply_amount: float 
    vat: float
    total_amount: float 
    purchase_category: str
    account_idx: int = 1

class MaterialInOutManagementBase(BaseModel):
    materialinout_idx: int
    date: date
    statement_number: str
    client: str
    delivery_quantity: int 
    defective_quantity: int 
    settlement_quantity: int 
    supply_amount: float 
    vat: float
    total_amount: float 
    purchase_category: str
    account_idx: int = 1

class MaterialInOutManagementUpdate(BaseModel):
    date: Optional[date]
    statement_number: Optional[str] = None
    client: Optional[str] = None
    delivery_quantity: Optional[int] = None
    defective_quantity: Optional[int] = None
    settlement_quantity: Optional[int] = None
    supply_amount: Optional[float] = None
    vat: Optional[float] = None
    total_amount: Optional[float] = None
    purchase_category: Optional[str] = None

    class Config:
        orm_mode = True

class MaterialInvenManagementCreate(BaseModel):
    date: date
    item_number: str
    item_name: str
    price: float
    basic_quantity: int
    basic_amount: float
    in_quantity: int
    in_amount: float
    defective_in_quantity: int
    defective_in_amount: float
    out_quantity: int
    out_amount: float
    adjustment_quantity: int
    current_quantity: int
    current_amount: float
    lot_current_quantity: int
    difference_quantity: int
    account_idx: int = 1

class MaterialInvenManagementBase(BaseModel):
    materialinvenmanage_idx: int
    date: date
    item_number: str
    item_name: str
    price: float
    basic_quantity: int
    basic_amount: float
    in_quantity: int
    in_amount: float
    defective_in_quantity: int
    defective_in_amount: float
    out_quantity: int
    out_amount: float
    adjustment_quantity: int
    current_quantity: int
    current_amount: float
    lot_current_quantity: int
    difference_quantity: int
    account_idx: int = 1

class MaterialInvenManagementUpdate(BaseModel):
    date: Optional[date]
    item_number: Optional[str]
    item_name: Optional[str]
    price: Optional[float]
    basic_quantity: Optional[int]
    basic_amount: Optional[float]
    in_quantity: Optional[int]
    in_amount: Optional[float]
    defective_in_quantity: Optional[int]
    defective_in_amount: Optional[float]
    out_quantity: Optional[int]
    out_amount: Optional[float]
    adjustment_quantity: Optional[int]
    current_quantity: Optional[int]
    current_amount: Optional[float]
    lot_current_quantity: Optional[int]
    difference_quantity: Optional[int]

    class Config:
        orm_mode = True

class MassProductionInput(BaseModel):
    daily_out: int
    capa: int
    delivery_date: str
    stock_finished: int
    stock_wip: int
    stock_part1: int
    order_vol: int
    lead_time_part1: int
    method: str
    forecast_months: int