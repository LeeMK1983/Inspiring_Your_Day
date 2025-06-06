import json
import os

# Load template dictionary from JSON
with open(os.path.join(os.path.dirname(__file__), "insight_templates.json"), encoding="utf-8") as f:
    TEMPLATE_DICT = json.load(f)

def generate_insight(mood, task, goal):
    # Try exact match
    exact_key = f"{mood}__{task}__{goal}"
    if exact_key in TEMPLATE_DICT:
        return TEMPLATE_DICT[exact_key]
    
    # Try wildcard fallbacks in order of specificity
    fallback_keys = [
        f"{mood}__{task}__*",
        f"{mood}__*__{goal}",
        f"*__{task}__{goal}",
        f"{mood}__*__*",
        f"*__{task}__*",
        f"*__*__{goal}",
    ]

    for key in fallback_keys:
        if key in TEMPLATE_DICT:
            return TEMPLATE_DICT[key]

    # Final fallback
    return (
        f"Even while feeling {mood}, focusing on {task} helps you become a {goal}. "
        f"You’re walking your path with intention."
    )
