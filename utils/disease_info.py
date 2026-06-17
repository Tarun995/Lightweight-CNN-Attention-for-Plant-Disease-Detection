# Label mappings for each crop
LABELS = {
    "potato": ['Early Blight', 'Late Blight', 'Healthy'],
    "tomato": ['Bacterial Spot', 'Early Blight', 'Late Blight', 'Leaf Mold',
               'Septoria Leaf Spot', 'Spider Mites', 'Target Spot',
               'Yellow Leaf Curl Virus', 'Mosaic Virus', 'Healthy'],
    "corn":   ['Healthy', 'Gray Leaf Spot', 'Common Rust', 'Northern Leaf Blight'],
}

# Actionable, lightweight guides for diseases
DISEASE_GUIDE = {
    "potato": {
        "Early Blight": {
            "Immediate": [
                "Remove heavily infected leaves.",
                "Avoid overhead watering; water at soil level.",
                "Improve spacing/airflow."
            ],
            "Further": [
                "Rotate crops (2–3 years).",
                "Use resistant varieties if available."
            ],
            "Causes": [
                "Fungus Alternaria; warm, humid conditions; leaf wetness."
            ],
        },
        "Late Blight": {
            "Immediate": [
                "Isolate/rogue infected plants.",
                "Avoid leaf wetness; increase airflow.",
            ],
            "Further": [
                "Destroy cull piles; rotate away from solanaceous crops.",
                "Monitor weather; apply protectants proactively."
            ],
            "Causes": [
                "Oomycete Phytophthora infestans; cool, wet weather."
            ],
        },
        "Healthy": {
            "Immediate": ["No action required."],
            "Further": ["Maintain good hygiene and balanced nutrition."],
            "Causes": ["—"],
        }
    },
    "tomato": {
        "Bacterial Spot": {
            "Immediate": ["Remove infected leaves.", "Avoid overhead irrigation."],
            "Further": ["Rotate crops; sanitize tools; use certified seed."],
            "Causes": ["Xanthomonas bacteria; splashing water spreads it."]
        },
        "Early Blight": {
            "Immediate": ["Remove lower infected leaves; mulch soil."],
            "Further": ["Rotate crops; avoid wet foliage; maintain K and Ca."],
            "Causes": ["Alternaria; warm temps + leaf wetness."]
        },
        "Late Blight": {
            "Immediate": ["Isolate plants; avoid foliage wetness."],
            "Further": ["Destroy volunteers; preventative protectants during cool/wet."],
            "Causes": ["P. infestans; cool, humid conditions."]
        },
        "Leaf Mold": {
            "Immediate": ["Increase ventilation; reduce humidity."],
            "Further": ["Prune for airflow; avoid overcrowding."],
            "Causes": ["Passalora fulva; high humidity in greenhouses."]
        },
        "Septoria Leaf Spot": {
            "Immediate": ["Remove infected leaves; mulch to block soil splash."],
            "Further": ["Rotate crops; avoid overhead watering."],
            "Causes": ["Septoria lycopersici; persistent leaf wetness."]
        },
        "Spider Mites": {
            "Immediate": ["Spray water underside leaves; isolate plants."],
            "Further": ["Introduce predators (Phytoseiulus); maintain humidity."],
            "Causes": ["Hot, dry conditions; dust stress."]
        },
        "Target Spot": {
            "Immediate": ["Remove infected leaves; improve airflow."],
            "Further": ["Rotate; avoid nighttime irrigation."],
            "Causes": ["Corynespora cassiicola; warm, humid conditions."]
        },
        "Yellow Leaf Curl Virus": {
            "Immediate": ["Control whiteflies; remove infected plants."],
            "Further": ["Use resistant varieties; reflective mulches."],
            "Causes": ["Begomovirus via whiteflies."]
        },
        "Mosaic Virus": {
            "Immediate": ["Remove infected plants; sanitize hands/tools."],
            "Further": ["Resistant varieties; avoid tobacco handling before work."],
            "Causes": ["TMV/ToMV; mechanical transmission."]
        },
        "Healthy": {
            "Immediate": ["No action required."],
            "Further": ["Keep balanced nutrients and good airflow."],
            "Causes": ["—"]
        }
    },
    "corn": {
        "Gray Leaf Spot": {
            "Immediate": ["Avoid irrigation on foliage; increase airflow."],
            "Further": ["Rotate; residue management; tolerant hybrids."],
            "Causes": ["Cercospora; warm, humid environments."]
        },
        "Common Rust": {
            "Immediate": ["Scout regularly; avoid dense planting."],
            "Further": ["Resistant hybrids; monitor for epidemic years."],
            "Causes": ["Puccinia sorghi; cool temps + moisture."]
        },
        "Northern Leaf Blight": {
            "Immediate": ["Remove severely infected leaves if few."],
            "Further": ["Resistant hybrids; rotate; manage residue."],
            "Causes": ["Exserohilum turcicum; moderate temps + humidity."]
        },
        "Healthy": {
            "Immediate": ["No action required."],
            "Further": ["Maintain fertility, spacing, irrigation discipline."],
            "Causes": ["—"]
        }
    }
}

# Useful links for fertilizers and pesticides
FERTILIZER_LINKS = {
    "potato": "https://www.indiamart.com/proddetail/potato-fertilizer-123.html",
    "tomato": "https://www.indiamart.com/proddetail/tomato-fertilizer-456.html",
    "corn":   "https://www.indiamart.com/proddetail/corn-maize-fertilizer-789.html"
}

PESTICIDE_LINKS = {
    "potato": "https://www.indiamart.com/search.mp?ss=potato%20fungicide",
    "tomato": "https://www.indiamart.com/search.mp?ss=tomato%20fungicide",
    "corn":   "https://www.indiamart.com/search.mp?ss=corn%20fungicide"
}
