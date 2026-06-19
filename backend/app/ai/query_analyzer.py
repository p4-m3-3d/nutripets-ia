class QueryAnalyzer:

    @staticmethod
    def detect_species(question: str):

        question = question.lower()

        if "gato" in question:
            return 2

        if "perro" in question:
            return 1

        return None

    @staticmethod
    def detect_life_stage(question: str):

        question = question.lower()

        if "cachorro" in question:
            return 1

        if "adulto" in question:
            return 2

        if "senior" in question:
            return 3

        return None