class RecipeService:

    @staticmethod
    def get_all_recipes():
        return [
            {
                "id": 1,
                "title": "Pollo con arroz para cachorro",
                "species": "Perro"
            },
            {
                "id": 2,
                "title": "Atún suave para gato adulto",
                "species": "Gato"
            }
        ]