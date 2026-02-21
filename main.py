
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, datetime
from database import get_db
from typing import List
import forecasting
import math

app = FastAPI()
@app.get("/")
def root():
    return None

#plan 엔드포인트
@app.post("/plans/", response_model=schemas.PlanCreate)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    return crud.create_plan(db, plan)

@app.get("/plans/all/", response_model=List[schemas.PlanBase])
def get_all_plans(db: Session = Depends(get_db)):
    return crud.get_all_plans(db)

@app.get("/plans/rate/{year}", response_model=List[schemas.PlanResponse])
def get_plans_rate(year: int, db: Session = Depends(get_db)):
    return crud.get_plans_rate_for_year(db, year)

@app.put("/plans/{plan_id}", response_model=schemas.PlanUpdate)
def update_plan(plan_id: int, plan_update: schemas.PlanUpdate, db: Session = Depends(get_db)):
    updated_plan = crud.update_plan(db, plan_id, plan_update)
    if not updated_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return updated_plan

@app.delete("/plans/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    deleted_plan = crud.delete_plan(db, plan_id)
    if not deleted_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"detail": "Plan deleted"}

@app.get("/plans/rates/{year},{month}", response_model=List[schemas.PlanResponse2])
def get_plan_rate_month(year: int, month: int, db: Session = Depends(get_db)):
    plans = crud.get_plan_rate_for_month(db, year, month)
    return plans

#production 엔드포인트
@app.post("/productions/", response_model=schemas.ProductionCreate)
def create_production(production: schemas.ProductionCreate, db: Session = Depends(get_db)):
    return crud.create_production(db, production)

@app.get("/productions/all/", response_model=List[schemas.ProductionBase])
def get_all_productions(db: Session = Depends(get_db)):
    return crud.get_all_productions(db)

@app.get("/productions/efficiency/{year}", response_model=List[schemas.ProductionResponse])
def get_production_efficiency(year: int, db: Session = Depends(get_db)):
    return crud.get_production_efficiency_for_year(db, year)

@app.get("/productions/{year}", response_model=List[schemas.ProductionBase])
def get_production(year: int, db: Session = Depends(get_db)):
    production = crud.get_production_year(db, year)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production

@app.get("/productions/day/{date}", response_model=List[schemas.ProductionBase])
def get_day_production_data(date: datetime.date,  db: Session = Depends(get_db)):
    production = crud.get_day_production(db, date)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production

@app.get("/productions/days/", response_model=List[schemas.ProductionBase])
def get_days_production_data(start_date: datetime.date, end_date: datetime.date, operator: str=None, item_number: str=None, item_name: str=None, db: Session = Depends(get_db)):
    production = crud.get_days_production(db, start_date, end_date, operator, item_number, item_name)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production

@app.get("/productions/id/{production_id}", response_model=schemas.ProductionBase)
def get_production(production_id: int, db: Session = Depends(get_db)):
    production = crud.get_production(db, production_id)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production.__dict__

@app.put("/productions/{production_id}", response_model=schemas.ProductionUpdate)
def update_production(production_id: int, productions_update: schemas.ProductionUpdate, db: Session = Depends(get_db)):
    updated_productions = crud.update_production(db, production_id, productions_update)
    if not updated_productions:
        raise HTTPException(status_code=404, detail="Production not found")
    return updated_productions

@app.delete("/productions/{production_id}")
def delete_production(production_id: int, db: Session = Depends(get_db)):
    deleted_production = crud.delete_production(db, production_id)
    if not deleted_production:
        raise HTTPException(status_code=404, detail="Production not found")
    return {"detail": "Production deleted"}

#inventory 엔드포인트
@app.post("/inventories/", response_model=schemas.InventoryManagementCreate)
def create_inventory_management(inventory: schemas.InventoryManagementCreate, db: Session = Depends(get_db)):
    return crud.create_inventory_management(db=db, inventory=inventory)

@app.get("/inventories/all/", response_model=List[schemas.InventoryManagementBase])
def get_all_inventories(db: Session = Depends(get_db)):
    return crud.get_all_inventories(db=db)

@app.get("/inventories/{inventory_id}", response_model=schemas.InventoryManagementBase)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = crud.get_inventory(db=db, inventory_id=inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory.__dict__

@app.get("/inventories/month/", response_model=List[schemas.InventoryManagementBase])
def get_inventory_month(year: int, month: int, db: Session = Depends(get_db)):
    inventory = crud.get_month_inventory(db, year, month)
    return inventory

@app.put("/inventories/{inventory_id}", response_model=schemas.InventoryManagementUpdate)
def update_inventory(inventory_id: int, inventory_update: schemas.InventoryManagementUpdate, db: Session = Depends(get_db)):
    updated_inventory = crud.update_inventory(db, inventory_id, inventory_update)
    if not updated_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return updated_inventory

@app.delete("/inventories/{inventory_id}")
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    deleted_inventory = crud.delete_inventory(db, inventory_id)
    if not deleted_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return {"detail": "Inventory deleted"}

#material 엔드포인트
@app.post("/materials/", response_model=schemas.MaterialCreate)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    return crud.create_materials(db=db, material=material)

@app.get("/materials/all/", response_model=List[schemas.MaterialBase])
def get_all_materials(db: Session = Depends(get_db)):
    return crud.get_all_materials(db=db)

@app.get("/material/rate/{year}", response_model=List[schemas.MaterialResponse2])
def get_material_rate(year: int, db: Session = Depends(get_db)):
    return crud.get_material_rate_for_year(db, year)

@app.get("/materials/rates/{year},{month}", response_model=List[schemas.MaterialResponse])
def get_material_rate(year: int, month: int, db: Session = Depends(get_db)):
    materials = crud.get_material_rate_for_month(db, year, month)
    return materials

@app.put("/materials/{material_id}", response_model=schemas.MaterialUpdate)
def update_material(material_id: int, material_update: schemas.MaterialUpdate, db: Session = Depends(get_db)):
    updated_material = crud.update_material(db, material_id, material_update)
    if not updated_material:
        raise HTTPException(status_code=404, detail="Material not found")
    return updated_material

@app.delete("/materials/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    deleted_material = crud.delete_material(db, material_id)
    if not deleted_material:
        raise HTTPException(status_code=404, detail="Material not found")
    return {"detail": "Material deleted"}

@app.get("/material_LOT/all/", response_model=List[schemas.MaterialInvenBase])
def get_all_materials_LOT(db: Session = Depends(get_db)):
    return crud.get_all_material_LOT(db=db)

#material_in_out 엔드포인트
@app.post("/materials_in_out/", response_model=schemas.MaterialInOutManagementCreate)
def create_in_out(material: schemas.MaterialInOutManagementCreate, db: Session = Depends(get_db)):
    return crud.create_in_out(db=db, material=material)

@app.get("/materials_in_out/all/", response_model=List[schemas.MaterialInOutManagementBase])
def get_all_in_out(db: Session = Depends(get_db)):
    return crud.get_all_materials_in_out(db=db)

@app.put("/materials_in_out/{material_id}", response_model=schemas.MaterialInOutManagementUpdate)
def update_in_out(material_id: int, material_update: schemas.MaterialInOutManagementUpdate, db: Session = Depends(get_db)):
    updated_in_out = crud.update_material_in_out(db, material_id, material_update)
    if not updated_in_out:
        raise HTTPException(status_code=404, detail="Material not found")
    return updated_in_out

@app.delete("/materials_in_out/{material_id}")
def delete_in_out(material_id: int, db: Session = Depends(get_db)):
    deleted_in_out = crud.delete_material_in_out(db, material_id)
    if not deleted_in_out:
        raise HTTPException(status_code=404, detail="Material not found")
    return {"detail": "Material deleted"}

#material_inven_management 엔드포인트
@app.post("/material_invens/", response_model=schemas.MaterialInvenManagementCreate)
def create_material_inventory(inventory: schemas.MaterialInvenManagementCreate, db: Session = Depends(get_db)):
    return crud.create_material_invens(db=db, inventory=inventory)

@app.get("/material_invens/all/", response_model=List[schemas.MaterialInvenManagementBase])
def get_all_material_inventories(db: Session = Depends(get_db)):
    return crud.get_all_material_invens(db=db)

@app.get("/material_invens/{inventory_id}", response_model=schemas.MaterialInvenManagementBase)
def get_material_inventories(inventory_id: int, db: Session = Depends(get_db)):
    inventory = crud.get_material_invens(db=db, inventory_id=inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory.__dict__

@app.get("/material_invens/month/", response_model=List[schemas.MaterialInvenManagementBase])
def get_month_material_inventories(year: int, month: int, db: Session = Depends(get_db)):
    inventory = crud.get_month_material_invens(db, year, month)
    return inventory

@app.put("/material_invens/{inventory_id}", response_model=schemas.MaterialInvenManagementUpdate)
def update_material_invens(inventory_id: int, inventory_update: schemas.MaterialInvenManagementUpdate, db: Session = Depends(get_db)):
    updated_inventory = crud.update_material_invens(db, inventory_id, inventory_update)
    if not updated_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return updated_inventory

@app.delete("/material_invens/{inventory_id}")
def delete_material_invens(inventory_id: int, db: Session = Depends(get_db)):
    deleted_inventory = crud.delete_material_invens(db, inventory_id)
    if not deleted_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return {"detail": "Inventory deleted"}

# prediction 엔드포인트
@app.post("/predictions/mass_production")
def predict_mass_production(data: schemas.MassProductionInput, db: Session = Depends(get_db)):
    raw_order_volume = crud.get_history_for_order_volume(db)
    raw_safety_stock = crud.get_history_for_safety_stock(db)

    dates = sorted(list(raw_order_volume.keys()))[-12:] if raw_order_volume else []
    
    if not dates:
        dates = ["2026-01", "2026-02"]
        historical_order_volume = {d: data.order_vol for d in dates}
        historical_safety_stock = {d: data.stock_finished for d in dates}
    else:
        historical_order_volume = {d: raw_order_volume[d] for d in dates}
        historical_safety_stock = {d: raw_safety_stock.get(d, 0) for d in dates}

    historical_lead_time = {d: data.lead_time_part1 for d in dates}

    pred_order = forecasting.calculate_forecast(historical_order_volume, data.method, data.forecast_months)
    pred_lead = forecasting.calculate_forecast(historical_lead_time, data.method, data.forecast_months)

    order_values = list(historical_order_volume.values())
    if len(order_values) > 1:
        avg_order = sum(order_values) / len(order_values)
        variance = sum((x - avg_order) ** 2 for x in order_values) / (len(order_values) - 1)
        std_dev = math.sqrt(variance)
    else:
        std_dev = 0

    Z_SCORE = 1.65
    pred_safety = {}
    for date in pred_order.keys():
        lt = max(1, pred_lead.get(date, 1))
        pred_safety[date] = int(Z_SCORE * std_dev * math.sqrt(lt))

    return {
        "order_volume": {"history": historical_order_volume, "prediction": pred_order},
        "lead_time": {"history": historical_lead_time, "prediction": pred_lead},
        "safety_stock": {"history": historical_safety_stock, "prediction": pred_safety}
    }