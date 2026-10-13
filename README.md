#Sistema de gestion de minimarkets 'bodega' 
Se identifico un problema en el Peru, el cual es la falta de digitalización
de los minimarkets. A razon de eso se creo este sistema.

La aplicacion de escritoria fue desarrollado en codigo Python y con una alamcenamiento de SQL server para la
administracion de stock y orden de los productos como informacion importante para la gestion del minimarket

Features:
- Gestion de productos ( 60% )
- Control de proveedores y historial de productos ( 10%)
- Registro de entrada y salida de mercaderia (10%)
- Modulo estadistico y reporte de ventas ( 05%)

Date:
- Legunaje : python -> POO
- Almacenamiento : SQL serverd ( proximamente mongoDB -> Base de datos NO relacional)
- Librerias utilizadas : Tkinter,pyodbc, math

requirements:
- Python 3.10
- SQL Server y SQL Server Management Studio (SSMS).
- Driver ODBC para SQL Server (ODBC Driver 17/18 for SQL Server).

instructions for intall the system .
git clone https://github.com/andyhuapaya1-bot/INVENTARIO-SQL-PY-.git
pip install -r requirements.txt
python main.py
