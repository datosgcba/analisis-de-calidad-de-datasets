from helpers import *

obras = {
    'input_path': "obras-registradas/obras-registradas.csv",
    "output_path": "obras-registradas/clean/obras-registradas.csv",
    "cleaner_rules": [
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
    ]
}

sueldos2012 = {
    'input_path': 'sueldo-funcionarios/sueldos-funcionarios-2012.csv',
    'output_path': 'sueldo-funcionarios/clean/sueldos-funcionarios-2012.csv',
    'cleaner_rules': [],
    'parse_options': {
        'sep': ';'
    }
}

target_datasets = [
    obras,
    sueldos2012
]
