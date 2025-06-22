from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from services.bonus_calculator import BonusCalculator
from models.schemas import BonusRequest, BonusResponse
from services.rule_loader import load_rules

router = APIRouter()


@router.post("/calculate-bonus", response_model=BonusResponse)
async def calculate_bonus(bonus_data: BonusRequest):
    try:
        rules = load_rules()
    except FileNotFoundError:
        print("Файл с правилами не найден.")
        raise HTTPException(status_code=500, detail="Ошибка загрузки правил")
    except Exception as e:
        print(f"Произошла ошибка при загрузке правил: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка загрузки правил")

    calculator = BonusCalculator(rules)
    result = calculator.calculate(bonus_data)
    return result
