# ====================================================
# FILE PURPOSE
# ====================================================
# Translates technical narrative metrics and weakness classifications
# into human-readable, writer-friendly feedback. Supports multiple languages.

FEEDBACK_CONTENT = {
    "english": {
        "high_repetition": {
            "title": "Repetitive Phrasing",
            "explanation": "This section relies heavily on the same words or sentence structures.",
            "suggestion": "Try varying your vocabulary or combining sentences to create a smoother flow."
        },
        "emotionally_flat": {
            "title": "Emotionally Flat",
            "explanation": "The tone here feels a bit neutral or detached.",
            "suggestion": "Consider weaving in the character's internal feelings or sensory details to help readers connect."
        },
        "poor_pacing": {
            "title": "Monotonous Pacing",
            "explanation": "The sentences in this section are very similar in length, which can make the reading experience feel flat.",
            "suggestion": "Try breaking up longer sentences or adding a short, punchy sentence to create rhythm."
        },
        "dense_exposition": {
            "title": "Heavy Description",
            "explanation": "This block is heavily descriptive without any breaks.",
            "suggestion": "Adding a short line of dialogue or breaking this into smaller paragraphs can help readers stay engaged."
        },
        "general_weakness": {
            "title": "Attention Drift",
            "explanation": "This section might cause the reader's attention to drift.",
            "suggestion": "Look for ways to tighten the prose, clarify the action, or raise the stakes."
        },
        "strong_section": {
            "title": "Strong Section",
            "explanation": "This part reads well.",
            "suggestion": "No major changes needed."
        }
    },
    "hindi": {
        "high_repetition": {
            "title": "दोहराव वाली शब्दावली",
            "explanation": "यह हिस्सा एक ही जैसे शब्दों या वाक्य संरचनाओं पर बहुत अधिक निर्भर है।",
            "suggestion": "प्रवाह को बेहतर बनाने के लिए अपनी शब्दावली में बदलाव करें या वाक्यों को जोड़ने का प्रयास करें।"
        },
        "emotionally_flat": {
            "title": "भावहीन वर्णन",
            "explanation": "यहाँ स्वर थोड़ा तटस्थ या अलग सा महसूस होता है।",
            "suggestion": "पाठकों को जोड़ने के लिए पात्र की आंतरिक भावनाओं या संवेदी विवरणों को शामिल करने पर विचार करें।"
        },
        "poor_pacing": {
            "title": "नीरस गति",
            "explanation": "इस खंड के वाक्यों की लंबाई बहुत समान है, जिससे पढ़ने का अनुभव सपाट हो सकता है।",
            "suggestion": "लय बनाने के लिए लंबे वाक्यों को तोड़ें या छोटे, प्रभावशाली वाक्य जोड़ें।"
        },
        "dense_exposition": {
            "title": "भारी विवरण",
            "explanation": "यह ब्लॉक बिना किसी ब्रेक के बहुत अधिक वर्णनात्मक है।",
            "suggestion": "संवाद की एक छोटी पंक्ति जोड़ने या इसे छोटे पैराग्राफ में तोड़ने से पाठकों को जोड़े रखने में मदद मिल सकती है।"
        },
        "general_weakness": {
            "title": "ध्यान भटकना",
            "explanation": "यह हिस्सा पाठक का ध्यान भटका सकता है।",
            "suggestion": "गद्य को कसने, क्रिया को स्पष्ट करने या कहानी में रोमांच बढ़ाने के तरीके खोजें।"
        },
        "strong_section": {
            "title": "मजबूत हिस्सा",
            "explanation": "यह हिस्सा अच्छी तरह से लिखा गया है।",
            "suggestion": "किसी बड़े बदलाव की आवश्यकता नहीं है।"
        }
    },
    "marathi": {
        "high_repetition": {
            "title": "पुनरावृत्ती होणारी वाक्यरचना",
            "explanation": "हा भाग सारख्याच शब्दांवर किंवा वाक्यरचनेवर खूप अवलंबून आहे.",
            "suggestion": "ओघ सुधारण्यासाठी शब्दसंग्रहात बदल करा किंवा वाक्ये एकत्र करण्याचा प्रयत्न करा."
        },
        "emotionally_flat": {
            "title": "भावनाहीन वर्णन",
            "explanation": "येथील स्वर थोडा तटस्थ किंवा अलिप्त वाटतो.",
            "suggestion": "वाचकांना जोडण्यासाठी पात्राच्या अंतर्गत भावना किंवा संवेदी तपशील समाविष्ट करण्याचा विचार करा."
        },
        "poor_pacing": {
            "title": "एकसुरी वेग",
            "explanation": "या भागातील वाक्यांची लांबी खूप सारखीच आहे, ज्यामुळे वाचनाचा अनुभव सपाट होऊ शकतो.",
            "suggestion": "लय निर्माण करण्यासाठी लांब वाक्ये तोडा किंवा लहान, प्रभावी वाक्ये जोडा."
        },
        "dense_exposition": {
            "title": "अति वर्णन",
            "explanation": "हा भाग कोणत्याही ब्रेकशिवाय खूप वर्णनात्मक आहे.",
            "suggestion": "संवादाची एखादी छोटी ओळ जोडणे किंवा याचे लहान परिच्छेद केल्यास वाचकांना खिळवून ठेवण्यास मदत होईल."
        },
        "general_weakness": {
            "title": "लक्ष विचलित होणे",
            "explanation": "हा भाग वाचकाचे लक्ष विचलित करू शकतो.",
            "suggestion": "गद्य अधिक सुटसुटीत करा, कृती स्पष्ट करा किंवा कथेतील उत्सुकता वाढवण्याचे मार्ग शोधा."
        },
        "strong_section": {
            "title": "उत्तम भाग",
            "explanation": "हा भाग वाचायला चांगला वाटतो.",
            "suggestion": "मोठ्या बदलांची गरज नाही."
        }
    }
}

def get_feedback_for_issue(issue: str, metrics: dict) -> dict:
    """
    Returns a writer-friendly explanation of the issue and a suggestion in the detected language.
    """
    lang = metrics.get("language", "english")
    if lang not in FEEDBACK_CONTENT:
        lang = "english"
        
    lang_feedback = FEEDBACK_CONTENT[lang]
    
    return lang_feedback.get(issue, lang_feedback["strong_section"])
