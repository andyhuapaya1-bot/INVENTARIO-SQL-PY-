import pyodbc

DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': r'DESKTOP-FIAHUU8\SQLEXPRESS',
    'database': 'Inventarios_SQLyPython',
    'trusted_connection': 'yes'
}

def get_db_connection():
    """Retorna una conexión activa a SQL Server o None si falla."""
    try:
        conn_str = (
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
            f"TrustServerCertificate=yes;"
        )
        return pyodbc.connect(conn_str)
    except Exception as e:
        print(f"\n[ERROR DE CONEXIÓN SQL]: {e}\n")
        return None

if __name__ == "__main__":
    # Prueba rápida de conexión
    conn = get_db_connection()
    if conn:
        print("¡Conexión exitosa a SQL Server!")
        conn.close()
    else:
        print("Falló la conexión. Revisa el nombre del servidor o servicio SQL.")