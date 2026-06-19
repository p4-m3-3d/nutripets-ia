from app.core.database import SessionLocal
from app.models.toxic_ingredient_model import ToxicIngredient

import re
import unicodedata

def normalize_text(text):

    ext = text.lower()

    return "".join(
    c for c in unicodedata.normalize(
        "NFD",
        text
    )
    if unicodedata.category(c) != "Mn"
)

DANGER_PRIORITY = {
"Crítico": 3,
"Alto": 2,
"Moderado": 1
}

URGENCY_MAP = {
"Crítico": "EMERGENCIA",
"Alto": "URGENTE",
"Moderado": "PRECAUCIÓN"
}

RECOMMENDED_ACTIONS = {
"EMERGENCIA":
"Acudir inmediatamente a un veterinario o centro de emergencias.",

"URGENTE":
    "Contactar a un veterinario lo antes posible y monitorear al animal.",

"PRECAUCIÓN":
    "Observar síntomas y consultar a un veterinario si empeoran."

}

class ToxicDetector:

    @staticmethod
    def detect(question: str):

        db = SessionLocal()

        try:

            ingredients = db.query(
                ToxicIngredient
            ).all()

            question_lower = normalize_text(
                question
            )

            # ==================================
            # BUSQUEDA POR NOMBRE
            # ==================================

            for ingredient in ingredients:

                ingredient_name = normalize_text(
                    ingredient.name
                )

                pattern = r"\b" + re.escape(
                    ingredient_name
                ) + r"\b"

                if re.search(
                    pattern,
                    question_lower
                ):

                    urgency = URGENCY_MAP.get(
                        ingredient.danger_level,
                        "DESCONOCIDA"
                    )

                    return {
                        "found": True,
                        "match_type": "ingredient",
                        "reason": f"Se detectó el ingrediente tóxico '{ingredient.name}' en la consulta.",
                        "ingredient": ingredient.name,
                        "danger_level": ingredient.danger_level,
                        "urgency": urgency,
                        "recommended_action": RECOMMENDED_ACTIONS.get(
                            urgency
                        ),
                        "symptoms": ingredient.symptoms,
                        "action_required": ingredient.action_required
                    }

                if ingredient.aliases:

                    aliases = ingredient.aliases.split(",")

                    for alias in aliases:

                        alias = normalize_text(
                            alias.strip()
                        )

                        pattern = r"\b" + re.escape(
                            alias
                        ) + r"\b"

                        if re.search(
                            pattern,
                            question_lower
                        ):

                            urgency = URGENCY_MAP.get(
                                ingredient.danger_level,
                                "DESCONOCIDA"
                            )

                            return {
                                "found": True,
                                "match_type": "alias",
                                "reason": f"Se detectó una referencia a '{ingredient.name}' mediante el alias '{alias}'.",
                                "ingredient": ingredient.name,
                                "danger_level": ingredient.danger_level,
                                "urgency": urgency,
                                "recommended_action": RECOMMENDED_ACTIONS.get(
                                    urgency
                                ),
                                "symptoms": ingredient.symptoms,
                                "action_required": ingredient.action_required
                            }

            # ==================================
            # BUSQUEDA POR SINTOMAS
            # ==================================

            matches = []

            for ingredient in ingredients:

                if not ingredient.symptoms:
                    continue

                symptoms = (
                    normalize_text(
                        ingredient.symptoms
                    )
                    .replace(".", "")
                    .split(",")
                )

                score = 0

                for symptom in symptoms:

                    symptom = symptom.strip()

                    if symptom and symptom in question_lower:
                        score += 1

                if score > 0:

                    urgency = URGENCY_MAP.get(
                        ingredient.danger_level,
                        "DESCONOCIDA"
                    )

                    matches.append({
                        "ingredient": ingredient.name,
                        "danger_level": ingredient.danger_level,
                        "urgency": urgency,
                        "recommended_action": RECOMMENDED_ACTIONS.get(
                            urgency
                        ),
                        "symptoms": ingredient.symptoms,
                        "action_required": ingredient.action_required,
                        "score": score
                    })

            if matches:

                filtered_matches = [
                    match for match in matches if match["score"] >= 2
                ]

                if not filtered_matches:
                    return {
                        "found": False
                    }

                filtered_matches.sort(
                    key=lambda x: (
                        x["score"],
                        DANGER_PRIORITY.get(
                            x["danger_level"],
                            0
                        )
                    ),
                    reverse=True
                )

                top_match = filtered_matches[0]

                return {
                    "found": True,
                    "match_type": "symptom",
                    "reason": (
                        f"Los síntomas reportados coinciden con "
                        f"una posible intoxicación por "
                        f"{top_match['ingredient']}."
                    ),
                    "highest_risk": top_match,
                    "possible_toxicities": filtered_matches[:5]
                }

            return {
                "found": False
            }

        finally:
            db.close()