
# Phase 1. Keyword Scoring
"""
This function converts free-form user input into the closes matching keyword from a predefined list(e.g., mood, task, goal)
    Start simple with string overlap and make it extensible later
"""
import numpy as np
from fuzzywuzzy import fuzz

# Define Keyword Lists _ mood, task, and goal keywords
# Create keyword groups with aliases/synonyms _ Category - Main Keyword - Synonyms(aliases)
mood_keywords = { 
    "calm": ["calm", "relaxed", "peaceful", "serene", "chill", "at ease", "grounded", "clear"],
    "anxious": ["anxious", "nervous", "worried", "tense", "uneasy", "overwhelmed", "stressed", "panicked"],
    "motivated": ["motivated", "driven", "energized", "pumped", "ready", "focused", "ambitious"],
    "tired": ["tired", "exhausted", "drained", "sleepy", "fatigued", "burned out", "worn out", "lethargic"],
    "hopeful": ["hopeful", "optimistic", "positive", "confident", "expecting good things", "looking forward"],
    "angry": ["angry", "frustrated", "irritated", "annoyed", "mad", "furious"],
    "sad": ["sad", "down", "blue", "depressed", "disheartened", "gloomy"]
}

task_keywords = {
    "focus": ["focus", "concentrate", "deep work", "block distractions", "single tasking", "mental clarity"],
    "meeting": ["meeting", "presentation", "interview", "discussion", "team call", "zoom", "client talk"],
    "exercise": ["exercise", "workout", "run", "gym", "train", "fitness", "stretch", "walk"],
    "study": ["study", "learn", "read", "memorize", "revise", "research", "homework", "practice"],
    "creative": ["creative", "design", "draw", "write", "compose", "paint", "brainstorm", "build"],
    "routine": ["routine", "clean", "cook", "errands", "shopping", "organize", "laundry", "admin"]
}

goal_keywords = {
    "leader": ["leader", "manager", "guide", "decision maker", "mentor", "role model"],
    "creator": ["creator", "artist", "builder", "designer", "innovator", "writer", "inventor"],
    "peaceful": ["peaceful", "balanced", "mindful", "calm life", "spiritual", "zen", "content"],
    "resilient": ["resilient", "strong", "persistent", "tough", "enduring", "gritty", "fighter"],
    "successful": ["successful", "rich", "wealthy", "recognized", "respected", "high achiever", "powerful"],
    "kind": ["kind", "compassionate", "generous", "helpful", "humble", "selfless"]
}

FALLBACKS = {
        "mood":"calm",
        "task":"focus",
        "goal":"resilient"
    }

def score_input(user_text, keyword_list):
    user_words = user_text.lower().split()
    best_match = None
    highest_score = 0

    for keyword in keyword_list:
        keyword_words = keyword.lower().split()
        score = sum(1 for word in keyword_words if word in user_words)
        if score > highest_score:
            highest_score = score
            best_match = keyword
    return best_match

def map_input_to_keyword(user_text, keyword_dict):
    user_words = set(user_text.lower().split())
    best_keyword = None
    best_score = 0

    for keyword, synonyms in keyword_dict.items():
        # The set() function creates a set, which is an unoredered, unindexed collection of unique elements(remove duplicates)
        synonym_set = set(syn.lower() for syn in synonyms)
        score = len(user_words.intersection(synonym_set))
        if score > best_score:
            best_score = score
            best_keyword = keyword
    return best_keyword if best_score >0 else None

def fuzzy_match_input(user_text, keyword_dict):
    user_text = user_text.lower()
    best_keyword = None
    highest_score = 0

    for keyword, synonyms in keyword_dict.items():
        for synonym in synonyms:
            score = fuzz.partial_ratio(user_text, synonym.lower())
            if score > highest_score:
                highest_score = score
                best_keyword = keyword
    return best_keyword if highest_score >=60 else None

def get_best_keyword(user_input, keyword_dict, category):
    # Step 1: Simple keyword match
    result = map_input_to_keyword(user_input, keyword_dict)
    if result:
        return result
    
    # Step 2: Fuzzy match
    result = fuzzy_match_input(user_input, keyword_dict)
    if result:
        return result
    
    return FALLBACKS.get(category, "unknown")


def taking_user_input():
    mood = input("How are you feeling toady?")
    task = input("What is your main task")
    goal = input("What kind of person do you aspire to become?")

    return mood, task, goal


if __name__ == "__main__":
    
    mood_input, task_input, goal_input = taking_user_input()
    
    mapped_mood = get_best_keyword(mood_input, mood_keywords, "mood")
    mapped_task = get_best_keyword(task_input, task_keywords, "task")
    mapped_goal = get_best_keyword(goal_input, goal_keywords, "goal")

    print("Mood:", mood_input, "\n", "Mapped Mood:", mapped_mood)
    print("Task:", task_input, "\n", "Mapped Task:", mapped_task)
    print("Goal:", goal_input, "\n", "Mapped Goal:", mapped_goal)