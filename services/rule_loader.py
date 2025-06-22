import json
from typing import List, Dict


def load_rules() -> List[Dict]:
    with open("app/config/bonus_rules.json", "r") as rules_file:
        rules = json.load(rules_file)
        return list(rules.values())
