from sqlalchemy.orm import Session
from models import Plan, Production, InventoryManagement, Material, MaterialPlan, MaterialInven, MaterialInOutManagement, MaterialInvenManagement, ProductionPlanSummary
import schemas
from sqlalchemy import extract, func, desc
from typing import List
from datetime import datetime, timedelta
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

#기간 계산 함수
def get_month_range(year: int, month: int):
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    return start_date, end_date

#plan CRUD
#plan Create
def create_plan(db: Session, plan: schemas.PlanCreate):
    db_plan = Plan(
        year=plan.year,
        month=plan.month,
        item_number=plan.item_number,
        item_name=plan.item_name,
        inventory=plan.inventory,
        model=plan.model,
        process=plan.process,
        price=plan.price,
        account_idx = plan.account_idx
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan.__dict__

#plan전체
def get_all_plans(db: Session):
    plan_get=db.query(Plan).all()
    return [plan.__dict__ for plan in plan_get]

#연도별 plan rate 데이터
def get_plans_rate_for_year(db: Session, year: int) -> List[schemas.PlanResponse]:
    summaries = db.query(ProductionPlanSummary).filter(ProductionPlanSummary.year == year).all()
    summary_dict = {s.month: s for s in summaries}
    plans_for_year = []

    for month in range(1, 13):
        s = summary_dict.get(month)
        if s:
            monthly_plan = schemas.PlanResponse(
                year=s.year,
                month=s.month,
                prod_plan=s.prod_plan,
                business_plan=s.business_plan,
                prod_amount=s.prod_amount,
                business_amount=s.business_amount,
                production_achievement_rate=s.prod_achievement_rate,
                business_achievement_rate=s.business_achievement_rate
            )
        else:
            monthly_plan = schemas.PlanResponse(
                year=year,
                month=month,
                prod_plan=0,
                business_plan=0,
                prod_amount=0,
                business_amount=0,
                production_achievement_rate=0,
                business_achievement_rate=0
            )
        plans_for_year.append(monthly_plan)

    return plans_for_year

#월별 plan 상승률
def get_plan_rate_for_month(db: Session, year: int, month: int):
    previous_month = (month - 1) or 12
    current_data = db.query(func.sum(Plan.inventory*InventoryManagement.price).label("current_amount"), Plan.process)\
        .select_from(InventoryManagement)\
        .join(Plan, Plan.item_name == InventoryManagement.item_name)\
        .filter(Plan.year == year, Plan.month == month)\
        .group_by(Plan.process).all()
    previous_data = db.query(func.sum(Plan.inventory*InventoryManagement.price).label("previous_amount"), Plan.process)\
        .select_from(InventoryManagement)\
        .join(Plan, Plan.item_name == InventoryManagement.item_name)\
        .filter(Plan.year == year, Plan.month == previous_month)\
        .group_by(Plan.process).all()
    previous_map = {data.process: data.previous_amount for data in previous_data}
    results = []

    for current in current_data:
        previous_amount = previous_map.get(current.process, 0)
        growth_rate = ((current.current_amount - previous_amount) / previous_amount * 100) if previous_amount else 0

        result = schemas.PlanResponse2(
            year=year,
            month=month,
            process=current.process,
            previous_amount=previous_amount,
            current_amount=current.current_amount,
            growth_rate=growth_rate
        )
        results.append(result)
    return results

#plan Update
def update_plan(db: Session, plan_id: int, plan_update: schemas.PlanUpdate):
    plan = db.query(Plan).filter(Plan.plan_idx == plan_id).first()
    
    if not plan:
        return None  
    
    for var, value in vars(plan_update).items():
        setattr(plan, var, value)  
        
    db.commit()
    db.refresh(plan)  
    return plan

#plan Delete
def delete_plan(db: Session, plan_id: int):
    plan = db.query(Plan).filter(Plan.plan_idx == plan_id).first()
    
    if not plan:
        return None
    
    db.delete(plan)
    db.commit()
    return plan

#production CRUD
#production Create
def create_production(db: Session, production: schemas.ProductionCreate):
    db_production = Production(
        date=production.date,
        line=production.line,
        operator=production.operator,
        item_number=production.item_number,
        item_name=production.item_name,
        model=production.model,
        target_quantity=production.target_quantity,
        produced_quantity=production.produced_quantity,
        production_efficiency=production.production_efficiency,
        process=production.process,
        operating_time=production.operating_time,
        non_operating_time=production.non_operating_time,
        shift=production.shift,
        line_efficiency=production.line_efficiency,
        specification=production.specification,
        account_idx=production.account_idx
    )
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production.__dict__

def get_production(db: Session, production_id: int):
    production_get = db.query(Production).filter(Production.production_idx == production_id).first()
    return  production_get

def get_production_year(db: Session, year: int):
    production_get = db.query(Production).filter(extract('year', Production.date) == year).all()
    return  [production.__dict__ for production in production_get]

def get_production_efficiency_for_year(db: Session, year: int) -> List[schemas.ProductionResponse]:
    plans_for_year = []

    for month in range(1, 13):
        start_date, end_date = get_month_range(year, month)
        production_efficiency = db.query(func.avg(Production.production_efficiency))\
            .filter(Production.date.between(start_date.date(), end_date.date()))\
            .scalar() or 0
        line_efficiency = db.query(func.avg(Production.line_efficiency))\
            .filter(Production.date.between(start_date.date(), end_date.date()))\
            .scalar() or 0
        
        monthly_plan = schemas.ProductionResponse(
            year=year,
            month=month,
            production_efficiency=int(production_efficiency),
            line_efficiency=int(line_efficiency)
        )
        plans_for_year.append(monthly_plan)
    return plans_for_year

#production전체
def get_all_productions(db: Session):
    production_get = db.query(Production).all()
    return [production.__dict__ for production in production_get]

def get_days_production(db: Session, start_date: datetime.date, end_date: datetime.date, operator: str , item_number: str , item_name: str):
    querys = db.query(Production).filter(Production.date.between(start_date, end_date))
    
    if operator:
        querys = querys.filter(Production.operator == operator)
    if item_number:
        querys = querys.filter(Production.item_number == item_number)
    if item_name:
        querys = querys.filter(Production.item_name == item_name)
    
    production_get = querys.order_by(desc(Production.production_idx)).all()
    return [production.__dict__ for production in production_get]

#특정날짜 production반환
def get_day_production(db: Session, date: datetime.date):
    production_get = db.query(Production).filter(Production.date == date).order_by(desc(Production.production_idx)).all()
    return [production.__dict__ for production in production_get]

#production Upadate
def update_production(db: Session, production_id: int, production_update: schemas.ProductionUpdate):
    production = db.query(Production).filter(Production.production_idx == production_id).first()
    
    if not production:
        return None  
    
    for var, value in vars(production_update).items():
        setattr(production, var, value)  
        
    db.commit()
    db.refresh(production)  
    return production

#production Delete
def delete_production(db: Session, production_id: int):
    production = db.query(Production).filter(Production.production_idx == production_id).first()
    
    if not production:
        return None
    
    db.delete(production)
    db.commit()
    return production

#inventory_management CRUD
#inventory_management Create
def create_inventory_management(db: Session, inventory: schemas.InventoryManagementCreate):
    db_inventory = InventoryManagement(
        date=inventory.date,
        item_number=inventory.item_number,
        item_name=inventory.item_name,
        price=inventory.price,
        basic_quantity=inventory.basic_quantity,
        basic_amount=inventory.basic_amount,
        in_quantity=inventory.in_quantity,
        in_amount=inventory.in_amount,
        defective_in_quantity=inventory.defective_in_quantity,
        defective_in_amount=inventory.defective_in_amount,
        out_quantity=inventory.out_quantity,
        out_amount=inventory.out_amount,
        adjustment_quantity=inventory.adjustment_quantity,
        current_quantity=inventory.current_quantity,
        current_amount=inventory.current_amount,
        lot_current_quantity=inventory.lot_current_quantity,
        difference_quantity=inventory.difference_quantity,
        account_idx=inventory.account_idx
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory.__dict__

def get_inventory(db: Session, inventory_id: int):
    inventory_get = db.query(InventoryManagement).filter(InventoryManagement.inventory_idx == inventory_id).first()
    return  inventory_get
    
#inventory전체
def get_all_inventories(db: Session):
    inventory_get = db.query(InventoryManagement).all()
    return [inventory.__dict__ for inventory in inventory_get]

def get_month_inventory(db: Session, year: int, month: int):
    inventory_get = db.query(InventoryManagement).filter(extract('year', InventoryManagement.date) == year, extract('month', InventoryManagement.date) == month).order_by(desc(InventoryManagement.inventory_idx)).all()
    return [inventory.__dict__ for inventory in inventory_get]

#inventory_management Update
def update_inventory(db: Session, inventory_id: int, inventory_update: schemas.InventoryManagementUpdate):
    inventory = db.query(InventoryManagement).filter(InventoryManagement.inventory_idx == inventory_id).first()
    
    if not inventory:
        return None  
    
    for var, value in vars(inventory_update).items():
        setattr(inventory, var, value)  
        
    db.commit()
    db.refresh(inventory)  
    return inventory

#inventory_management Delete
def delete_inventory(db: Session, inventory_id: int):
    inventory = db.query(InventoryManagement).filter(InventoryManagement.inventory_idx == inventory_id).first()
    
    if not inventory:
        return None
    
    db.delete(inventory)
    db.commit()
    return inventory

#material CRUD
#material Create
def create_materials(db: Session, material: schemas.MaterialCreate):
    db_material = Material(
        date=material.date,
        client=material.client,
        item_number=material.item_number,
        item_name=material.item_name,
        item_category=material.item_category,
        model=material.model,
        process=material.process,
        quantity=material.quantity,
        account_idx=material.account_idx
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material.__dict__

#material 전체
def get_all_materials(db: Session):
    material_get = db.query(Material).all()
    return [material.__dict__ for material in material_get]

#material Update
def update_material(db: Session, material_id: int, material_update: schemas.MaterialUpdate):
    material = db.query(Material).filter(Material.material_idx == material_id).first()
    
    if not material:
        return None  
    
    for var, value in vars(material_update).items():
        setattr(material, var, value)  
        
    db.commit()
    db.refresh(material)  
    return material

#material Delete
def delete_material(db: Session, material_id: int):
    material = db.query(Material).filter(Material.material_idx == material_id).first()
    
    if not material:
        return None
    
    db.delete(material)
    db.commit()
    return material

def get_material_rate_for_year(db: Session, year: int) -> List[schemas.MaterialResponse2]:
    plans = db.query(MaterialPlan).filter(MaterialPlan.year == year).order_by(MaterialPlan.month).all()    
    materials_for_year = []
    for plan in plans:
        monthly_plan = schemas.MaterialResponse2(
            year=plan.year,
            month=plan.month,
            business_plan=plan.business_plan,
            business_amount=plan.business_amount,
            business_achievement_rate=plan.business_achievement_rate
        )
        materials_for_year.append(monthly_plan)
        
    return materials_for_year

#월별 material 상승률
def get_material_rate_for_month(db: Session, year: int, month: int):
    current_start_date = datetime(year, month, 1)
    next_month = month % 12 + 1
    current_end_date = datetime(year, next_month, 1) - timedelta(days=1)
    previous_month = (month - 1) or 12
    previous_year = year - 1 if month == 1 else year
    previous_start_date = datetime(previous_year, previous_month, 1)
    previous_end_date = datetime(year, month, 1) - timedelta(days=1)
    current_data = db.query(func.sum(Material.quantity*MaterialInvenManagement.price).label("current_amount"), Material.client)\
        .select_from(MaterialInvenManagement)\
        .join(Material, Material.item_name == MaterialInvenManagement.item_name)\
        .filter(Material.date >= current_start_date, Material.date <= current_end_date)\
        .group_by(Material.client).all()
    previous_data = db.query(func.sum(Material.quantity*MaterialInvenManagement.price).label("previous_amount"), Material.client)\
        .select_from(MaterialInvenManagement)\
        .join(Material, Material.item_name == MaterialInvenManagement.item_name)\
        .filter(Material.date >= previous_start_date, Material.date <= previous_end_date)\
        .group_by(Material.client).all()
    previous_map = {data.client: data.previous_amount for data in previous_data}
    results = []

    for current in current_data:
        previous_amount = previous_map.get(current.client, 0)
        growth_rate = ((current.current_amount - previous_amount) / previous_amount * 100) if previous_amount else 0

        result = schemas.MaterialResponse(
            year=year,
            month=month,
            client=current.client,
            previous_amount=previous_amount,
            current_amount=current.current_amount,
            growth_rate=growth_rate
        )
        results.append(result)
    return results

#material_lot 전체
def get_all_material_LOT(db: Session):
    material_get = db.query(MaterialInven).all()
    return [material.__dict__ for material in material_get]

#material_in_out_management CRUD
#material_in_out_management Create
def create_in_out(db: Session, material: schemas.MaterialInOutManagementCreate):
    db_material = MaterialInOutManagement(
        date=material.date,
        statement_number=material.statement_number,
        client=material.client,
        delivery_quantity=material.delivery_quantity,
        defective_quantity=material.defective_quantity,
        settlement_quantity=material.settlement_quantity,
        supply_amount=material.supply_amount,
        vat=material.vat,
        total_amount=material.total_amount,
        purchase_category=material.purchase_category,
        account_idx=material.account_idx
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material.__dict__

#material_in_out 전체
def get_all_materials_in_out(db: Session):
    material_get = db.query(MaterialInOutManagement).all()
    return [material.__dict__ for material in material_get]

#material_in_out_management Update
def update_material_in_out(db: Session, material_id: int, material_update: schemas.MaterialInOutManagementUpdate):
    material = db.query(MaterialInOutManagement).filter(MaterialInOutManagement.materialinout_idx == material_id).first()
    
    if not material:
        return None  
    
    for var, value in vars(material_update).items():
        setattr(material, var, value)  
        
    db.commit()
    db.refresh(material)  
    return material

#material_in_out_management Delete
def delete_material_in_out(db: Session, material_id: int):
    material = db.query(MaterialInOutManagement).filter(MaterialInOutManagement.materialinout_idx == material_id).first()
    
    if not material:
        return None
    
    db.delete(material)
    db.commit()
    return material

#material_inven_management CRUD
def create_material_invens(db: Session, inventory: schemas.MaterialInvenManagementCreate):
    db_inventory = MaterialInvenManagement(
        date=inventory.date,
        item_number=inventory.item_number,
        item_name=inventory.item_name,
        price=inventory.price,
        basic_quantity=inventory.basic_quantity,
        basic_amount=inventory.basic_amount,
        in_quantity=inventory.in_quantity,
        in_amount=inventory.in_amount,
        defective_in_quantity=inventory.defective_in_quantity,
        defective_in_amount=inventory.defective_in_amount,
        out_quantity=inventory.out_quantity,
        out_amount=inventory.out_amount,
        adjustment_quantity=inventory.adjustment_quantity,
        current_quantity=inventory.current_quantity,
        current_amount=inventory.current_amount,
        lot_current_quantity=inventory.lot_current_quantity,
        difference_quantity=inventory.difference_quantity,
        account_idx=inventory.account_idx
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory.__dict__

def get_material_invens(db: Session, material_invens_id: int):
    material_invens_get = db.query(MaterialInvenManagement).filter(MaterialInvenManagement.materialinvenmanage_idx == material_invens_id).first()
    return  material_invens_get
    
#material_inven_management전체
def get_all_material_invens(db: Session):
    material_invens_get = db.query(MaterialInvenManagement).all()
    return [material_invens.__dict__ for material_invens in material_invens_get]

def get_month_material_invens(db: Session, year: int, month: int):
    material_invens_get = db.query(MaterialInvenManagement).filter(extract('year', MaterialInvenManagement.date) == year, extract('month', MaterialInvenManagement.date) == month).order_by(desc(MaterialInvenManagement.materialinvenmanage_idx)).all()
    return [material_invens.__dict__ for material_invens in material_invens_get]

#material_inven_management Update
def update_material_invens(db: Session, inventory_id: int, inventory_update: schemas.MaterialInvenManagementUpdate):
    inventory = db.query(MaterialInvenManagement).filter(MaterialInvenManagement.materialinvenmanage_idx == inventory_id).first()
    
    if not inventory:
        return None  
    
    for var, value in vars(inventory_update).items():
        setattr(inventory, var, value)  
        
    db.commit()
    db.refresh(inventory)  
    return inventory

#material_inven_management Delete
def delete_material_invens(db: Session, inventory_id: int):
    inventory = db.query(MaterialInvenManagement).filter(MaterialInvenManagement.materialinvenmanage_idx == inventory_id).first()
    
    if not inventory:
        return None
    
    db.delete(inventory)
    db.commit()
    return inventory

#  Production을 월별로 집계하여 딕셔너리로 반환
def get_history_for_order_volume(db: Session):
    data = db.query(Production).all()
    if not data:
        return {}
        
    df = pd.DataFrame([{
        'date': p.date,
        'quantity': p.produced_quantity
    } for p in data])
    
    df['date'] = pd.to_datetime(df['date'])
    df_monthly = df.resample('M', on='date').sum().reset_index()
    
    return {row['date'].strftime('%Y-%m'): int(row['quantity']) for _, row in df_monthly.iterrows()}

# InventoryManagement를 월별로 집계하여 딕셔너리로 반환
def get_history_for_safety_stock(db: Session):
    data = db.query(InventoryManagement).all()
    if not data:
        return {}
        
    df = pd.DataFrame([{
        'date': inv.date,
        'quantity': inv.current_quantity
    } for inv in data])
    
    df['date'] = pd.to_datetime(df['date'])
    df_monthly = df.resample('M', on='date').last().reset_index() 
    df_monthly['quantity'] = df_monthly['quantity'].ffill().fillna(0)

    return {row['date'].strftime('%Y-%m'): int(row['quantity']) for _, row in df_monthly.iterrows()}