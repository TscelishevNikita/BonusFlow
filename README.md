# BonusFlow

## Установка
```bash
pip install -r requirements.txt
```

## Запуск
```bash
python main.py
```

## Настройка

Добавьте новую запись в config/bonus_rules.json

Определите:

1) name: уникальное имя правила

2) description: описание правила (опционально)

3) condition: условие применения (опционально)

4) type: тип бонуса (множитель или фиксированое значение)

5) priority: порядок применения

6) amount: значение множителя или фиксированного значения (зависит от типа бонуса)

## Использование

Открыть документацию http://127.0.0.1:8000/docs или использовать PostMan

Пример запроса:
```bash
{
  "transaction_amount": 150,
  "timestamp": "2025-06-22T18:36:04.457Z",
  "customer_status": "vip"
}
```

Пример ответа:
```bash
{
  "total_bonus": 42,
  "applied_rules": [
    {
      "rule": "base_rate",
      "bonus": 15
    },
    {
      "rule": "holiday_bonus",
      "bonus": 15
    },
    {
      "rule": "vip_boost",
      "bonus": 12
    }
  ]
}
```
