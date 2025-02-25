from datetime import datetime


def string_to_datetime(date_str: str, date_format: str) -> datetime:
    """
    🕒 Converte uma string para um objeto datetime com o formato especificado.

    Args:
        date_str (str): String representando a data/hora.
        date_format (str): Formato da string (ex.: "%Y-%m-%d %H:%M:%S").

    Returns:
        datetime: Objeto datetime correspondente à string fornecida.

    Raises:
        ValueError: Se a string não corresponder ao formato especificado.
    """
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError as e:
        raise ValueError(f"❌ Erro na conversão: {str(e)}")


def datetime_to_string(date_obj: datetime, date_format: str) -> str:
    """
    📝 Converte um objeto datetime para uma string com o formato especificado.

    Args:
        date_obj (datetime): Objeto datetime a ser convertido.
        date_format (str): Formato de saída da string (ex.: "%d/%m/%Y %H:%M").

    Returns:
        str: String formatada conforme especificado.

    Raises:
        TypeError: Se o objeto fornecido não for um datetime válido.
    """
    if not isinstance(date_obj, datetime):
        raise TypeError("❌ O parâmetro 'date_obj' deve ser um objeto datetime.")
    return date_obj.strftime(date_format)


def validate_date_string(date_str: str, date_format: str) -> bool:
    """
    ✅ Valida se uma string de data/hora corresponde ao formato especificado.

    Args:
        date_str (str): String da data a ser validada.
        date_format (str): Formato esperado da string.

    Returns:
        bool: True se válido, False caso contrário.
    """
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


# 🌟 Exemplos rápidos de uso:
if __name__ == "__main__":
    # Converte string para datetime
    dt = string_to_datetime("2025-02-24 14:30:00", "%Y-%m-%d %H:%M:%S")
    print("🕒 String para datetime:", dt)

    # Converte datetime para string
    dt_str = datetime_to_string(dt, "%d/%m/%Y %H:%M")
    print("📝 Datetime para string:", dt_str)

    # Valida string de data
    is_valid = validate_date_string("24/02/2025", "%d/%m/%Y")
    print("✅ String de data válida:", is_valid)