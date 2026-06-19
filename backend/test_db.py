from app.core.database import engine

try:
    connection = engine.connect()
    print("Conexión exitosa con MySQL")
    connection.close()

except Exception as e:
    print("Error:", e)