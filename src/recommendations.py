# src/recommendations.py

RECOMMENDATIONS = {
    "academics": [
        "What departments are available in ANITS?",
        "Who is the HOD of CSE department?",
        "What courses are offered at ANITS?"
    ],

    "facilities": [
        "Where is the library located?",
        "What are the library timings?",
        "Is there a hostel facility?"
    ],

    "placements": [
        "What companies visit ANITS?",
        "What is the highest placement package?",
        "Who is the placement officer?"
    ],

    "clubs": [
        "What clubs are available in ANITS?",
        "How can I join a club?",
        "When is the annual fest?"
    ],

    "contacts": [
        "What is the principal email?",
        "How can I contact the placement cell?",
        "What is the college phone number?"
    ],

    "locations": [
        "Where is the placement cell?",
        "Where is the canteen?",
        "Where is the boys hostel?"
    ],

    "general": [
        "Tell me about ANITS",
        "How to apply for admission?",
        "What facilities are available?"
    ]
}


def get_recommendations(category):
    return RECOMMENDATIONS.get(category, RECOMMENDATIONS["general"])