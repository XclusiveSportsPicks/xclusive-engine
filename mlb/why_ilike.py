# mlb/why_i_like.py

def generate_reason(matchup, confidence, odds, sharp_delta):
    return f"{matchup}: Confidence {confidence}/10 with a {sharp_delta}% sharp differential and odds at {odds}."
