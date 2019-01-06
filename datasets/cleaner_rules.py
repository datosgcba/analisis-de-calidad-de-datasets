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


cleaner_rules = {'obras-registradas': [
    rename_column([
        # Columnas que no se modifican:
        ("lat", "lat"),
        ("long", "long"),
        ("direccion", "direccion"),
        ("codigo_postal", "codigo_postal"),  # TODO: revisar los nombres de las columnas de los codigos postales
        ("codigo_postal_argentino", "codigo_postal_argentino"),
        ("tipo_obra", "tipo_obra"),
        ("destino", "destino"),
        ("barrio", "barrio"),
        ("comuna", "comuna"),
        ("zonificaci", "zonificacion"),  # TODO: revisar ?

        # Columnas que si se modifican
        ("fecha_esta", "estado_fecha"),
        ("n_expedien", "expediente_numero"),
        ("f_expedien", "expediente_fecha"),
        ("calle", "direccion_calle"),
        ("altura", "direccion_altura"),
        ("smp", "seccion_manzana_parcela"),
        ("m2", "superficie_m2")
    ])
], 'sueldos-funcionarios': [

]}
