import re

class Validador:
    @staticmethod
    def es_texto_no_vacio(texto, nombre_campo="Campo"):
        if not texto or not str(texto).strip():
            return False, f"El campo '{nombre_campo}' no puede estar vacío."
        return True, str(texto).strip()

    @staticmethod
    def es_entero_positivo(valor, nombre_campo="Número", permitir_cero=True):
        try:
            val = int(valor)
            if permitir_cero and val < 0:
                return False, f"'{nombre_campo}' debe ser mayor o igual a 0."
            if not permitir_cero and val <= 0:
                return False, f"'{nombre_campo}' debe ser mayor a 0."
            return True, val
        except (ValueError, TypeError):
            return False, f"'{nombre_campo}' debe ser un número entero válido."

    @staticmethod
    def es_decimal_positivo(valor, nombre_campo="Monto", permitir_cero=False):
        """
        Sirve para precios (productos), totales (ventas), precios unitarios (detalles)[cite: 1, 2, 3].
        """
        try:
            val = float(valor)
            if permitir_cero and val < 0:
                return False, f"'{nombre_campo}' debe ser un importe mayor o igual a 0."
            if not permitir_cero and val <= 0:
                return False, f"'{nombre_campo}' debe ser un importe mayor a 0.00."
            return True, round(val, 2)
        except (ValueError, TypeError):
            return False, f"'{nombre_campo}' debe ser un valor monetario o decimal válido."

    @staticmethod
    def es_codigo_barras_ean13(codigo):
        """Valida exactamente 13 dígitos numéricos según la restricción SQL[cite: 2, 3]."""
        codigo_limpio = str(codigo).strip()
        if not re.fullmatch(r"^\d{13}$", codigo_limpio):
            return False, "El código de barras debe contener exactamente 13 dígitos numéricos."
        return True, codigo_limpio

    @staticmethod
    def es_codigo_formato(codigo, longitud_max=9, nombre_campo="Código"):
        """Valida códigos alfanuméricos cortos (productos, movimientos, ventas)[cite: 2, 3]."""
        codigo_limpio = str(codigo).strip()
        if not codigo_limpio:
            return True, None  # Si es opcional en la BD
        if len(codigo_limpio) > longitud_max:
            return False, f"'{nombre_campo}' no puede exceder los {longitud_max} caracteres."
        return True, codigo_limpio

    @staticmethod
    def es_email_valido(email):
        """Valida estructura estándar de correo para proveedores[cite: 2, 3]."""
        email_limpio = str(email).strip()
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.fullmatch(patron, email_limpio):
            return False, "El formato del correo electrónico no es válido."
        return True, email_limpio

    @staticmethod
    def es_telefono_valido(telefono, longitud_max=14):
        """Valida que el teléfono contenga solo números o caracteres permitidos (+, -)[cite: 2, 3]."""
        tel = str(telefono).strip()
        if not tel:
            return True, None  # Es campo opcional en SQL[cite: 2, 3]
        if len(tel) > longitud_max or not re.fullmatch(r"^[\d\+\s\-]{6,14}$", tel):
            return False, f"El teléfono debe tener entre 6 y {longitud_max} dígitos válidos."
        return True, tel