# Rules from https://datosgcba.github.io/guia-datos/guia-abiertos/

# Booleanos -> valores permitidos: ["true", "false", ""]

# TIEMPO -> ISO 8601 YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]
# Zona horaria default: UTC-03:00
# Fecha -> YYYY-MM-DD
# Hora -> HH:MM:SS[.mmmmmm][+HH:MM]
# Fecha y Hora -> YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]
# Duracion -> YYYY-MM-DDTHH:MM:SS[.mmmmmm]

# Rangos horarios : TODO

# Coordenadas
# Estandar EPSG: 4326 - WGS 84
# Campos deben llamarse "lat" y "long"
# Estandar WKT para datos geograficos que no sean coordenadas / puntos

# Estandar de contrataciones abieras
# Estandar GTFS para datos de movilidad
# Estandar WKT para datos geograficos


def remove_colum(column_name):
    return {"remover_columnas": [
        {"field": column_name},
    ]}


def rename_column(column_tuples):
    columns = []
    for original_name, new_name in column_tuples:
        columns.append({
            "field": original_name,
            "new_field": new_name
        })
    return {"renombrar_columnas": columns}


def parse_datetime(column_name, original_format):
    # Target format: YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]
    return {"fecha_completa": [
        {"field": column_name, "time_format": original_format}
    ]}


def parse_date(column_name, original_format):
    # Target format: YYYY-MM-DD
    # Also possible target format: YYYY-MM (when there is no day information)
    return {"fecha_simple": [
        {"field": column_name, "time_format": original_format}
    ]}


def parse_fragmented_datetime(original_columns, target_colum):
    return {"fecha_separada": [
        {"fields": original_columns, "new_field_name": target_colum}
    ]}
