def predict_confidence(matchup):
    # Replace with real model inference once available
    mock_scores = {
        "Yankees vs Red Sox": 8.2,
        "Dodgers vs Padres": 7.7,
        "Braves vs Mets": 8.9,
    }
    return mock_scores.get(matchup, 6.0)
