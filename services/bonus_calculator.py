from typing import List, Dict

from models.schemas import BonusRequest


class BonusCalculator:
    """
    Класс для расчета бонусов на основе заданных правил.
    Атрибуты:
        rules (List[Dict]): Список правил для расчета бонусов, отсортированный
        по приоритету.
    """
    def __init__(self, rules: List[Dict]):
        """
        Инициализирует объект BonusCalculator.
        Аргументы:
            rules (List[Dict]): Список правил для расчета бонусов.
        """
        self.rules = sorted(rules, key=lambda x: x["priority"])

    def calculate(self, bonus_data: BonusRequest) -> dict:
        """
        Рассчитывает бонусы на основе данных о транзакции и применяемых правил.
        Аргументы:
            bonus_data (BonusRequest): Данные о транзакции.
        Возвращает:
            dict: Словарь с общим бонусом и примененными правилами.
        """
        base_rate = self._get_base_rate()
        base_bonus = bonus_data.transaction_amount // base_rate if base_rate else 0
        total_bonus = base_bonus
        applied_rules = []

        for rule in self.rules:
            if self._check_condition(rule, bonus_data):
                bonus_before = total_bonus
                total_bonus = self._apply_rule(rule, total_bonus)
                applied_rules.append({
                    "rule": rule["name"],
                    "bonus": round(
                        total_bonus - bonus_before if rule['type'] != 'base_bonus'
                        else base_bonus,
                        2)
                })

        return {
            "total_bonus": total_bonus,
            "applied_rules": list(filter(lambda x: x["bonus"] > 0,
                                         applied_rules))
        }

    def _get_base_rate(self) -> float:
        """
        Возвращает базовую ставку для расчета бонусов.
        Возвращает:
            float: Базовая ставка.
        """
        for rule in self.rules:
            if rule["type"] == "base_bonus":
                return rule["amount"]

    def _check_condition(self, rule: Dict, bonus_data: BonusRequest) -> bool:
        """
        Проверяет, выполняется ли условие для применения правила.
        Аргументы:
            rule (Dict): Правило для проверки.
            bonus_data (BonusRequest): Данные о транзакции.
        Возвращает:
            bool: True, если условие выполняется или условий нет, иначе False.
        """
        if "condition" not in rule:
            return True
        condition = rule["condition"]
        if condition == "is_weekend_or_holiday":
            return bonus_data.timestamp.weekday() >= 5
        elif condition == "is_vip":
            return bonus_data.customer_status == "vip"
        return False

    def _apply_rule(self, rule: Dict, current_bonus: float) -> float:
        """
        Применяет правило к текущему бонусу.
        Аргументы:
            rule (Dict): Правило для применения.
            current_bonus (float): Текущий бонус.
        Возвращает:
            float: Обновленный бонус после применения правила.
        """
        if rule["type"] == "multiplier":
            return round(current_bonus * rule["amount"], 2)
        if rule["type"] == "fixed_bonus":
            return current_bonus + rule["amount"]
        return current_bonus
