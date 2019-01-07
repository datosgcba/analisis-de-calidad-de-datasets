# coding=utf-8
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

# TODO: combinar columnas de año y mes para los datasets de sueldos

sueldos2012 = {
    'input_path': 'sueldo-funcionarios/sueldos-funcionarios-2012.csv',
    'output_path': 'sueldo-funcionarios/clean/sueldos-funcionarios-2012.csv',
    'cleaner_rules': [
        rename_column([
            ("ANIO", "anio"),
            ("MES", "mes"),
            ("APELLIDO", "apellido"),
            ("NOMBRES", "nombre"),
            ("CARGO", "cargo"),
            ("ASIG_MENSUALES", "asignacion_mensual"),
            ("SALARIO_FAMILIAR", "salario_familiar"),
            ("DESCUENTOS_MENSUALES", "descuentos"),
            ("LIQUIDO", "liquido"),
        ])
    ],
    'parse_options': {
        'sep': ';'
    }
}

sueldos2013 = {
    'input_path': 'sueldo-funcionarios/sueldos-funcionarios-2013.csv',
    'output_path': 'sueldo-funcionarios/clean/sueldos-funcionarios-2013.csv',
    'cleaner_rules': [
        rename_column([
            ("anio", "anio"),
            ("mes", "mes"),
            ("apellido", "apellido"),
            ("nombre", "nombre"),
            ("cargo", "cargo"),
            ("asig_mensuales", "asignacion_mensual"),
            ("salario_familiar", "salario_familiar"),
            ("descuentos_mensuales", "descuentos"),
            ("liquido", "liquido"),
        ]),
        remove_colum("nromes")
    ],
    'parse_options': {
        'sep': ';'
    }
}

sueldos2014 = {
    'input_path': 'sueldo-funcionarios/sueldos-funcionarios-2014.csv',
    'output_path': 'sueldo-funcionarios/clean/sueldos-funcionarios-2014.csv',
    'cleaner_rules': [
        rename_column([
            ("anio", "anio"),
            ("mes", "mes"),
            ("apellido", "apellido"),
            ("nombre", "nombre"),
            ("cargo", "cargo"),
            ("asig_mensuales", "asignacion_mensual"),
            ("salario_familiar", "salario_familiar"),
            ("descuentos_mensuales", "descuentos"),
            ("liquido", "liquido"),
        ]),
        remove_colum("nromes")
    ],
    'parse_options': {
        'sep': ';'
    }
}

sueldos2015 = {
    'input_path': 'sueldo-funcionarios/sueldos-funcionarios-2015.csv',
    'output_path': 'sueldo-funcionarios/clean/sueldos-funcionarios-2015.csv',
    'cleaner_rules': [
        rename_column([
            (u"AÑO", "anio"),
            ("MES", "mes"),
            ("APELLIDO", "apellido"),
            ("NOMBRES", "nombre"),
            ("CARGO", "cargo"),
            ("ASIG_MENSUALES", "asignacion_mensual"),
            ("SALARIO_FAMILIAR", "salario_familiar"),
            ("DESCUENTOS_MENSUALES", "descuentos"),
            ("LIQUIDO", "liquido"),
        ]),
        remove_colum("N")
    ],
    'parse_options': {
        'sep': ';'
    }
}

sueldos2016 = {
    'input_path': 'sueldo-funcionarios/sueldos-funcionarios-2016.csv',
    'output_path': 'sueldo-funcionarios/clean/sueldos-funcionarios-2016.csv',
    'cleaner_rules': [
        rename_column([
            (u"AÑO", "anio"),
            ("MES", "mes"),
            ("APELLIDO", "apellido"),
            ("NOMBRE", "nombre"),
            ("CARGO", "cargo"),
            ("TOTAL_DE_ASIGNACIONES", "asignacion_mensual"),
            ("SALARIO_FAMILIAR", "salario_familiar"),
            ("TOTAL_DE_DESCUENTOS", "descuentos"),
            ("LIQUIDO", "liquido"),
        ]),
        remove_colum("NUMERO")
    ],
    'parse_options': {
        'sep': ';'
    }
}

sueldos2017 = {
    'input_path': 'sueldo-funcionarios/sueldos-funcionarios-2017.csv',
    'output_path': 'sueldo-funcionarios/clean/sueldos-funcionarios-2017.csv',
    'cleaner_rules': [
        rename_column([
            (u"AÑO", "anio"),
            ("MES", "mes"),
            ("APELLIDO", "apellido"),
            ("NOMBRE", "nombre"),
            ("CARGO", "cargo"),
            ("TOTAL_DE_ASIGNACIONES", "asignacion_mensual"),
            ("SALARIO_FAMILIAR", "salario_familiar"),
            ("TOTAL_DE_DESCUENTOS", "descuentos"),
            ("LIQUIDO", "liquido"),
        ]),
        remove_colum("NUMERO")
    ],
    'parse_options': {
        'sep': ';'
    }
}

sueldos2018 = {
    'input_path': 'sueldo-funcionarios/sueldos-funcionarios-2018.csv',
    'output_path': 'sueldo-funcionarios/clean/sueldos-funcionarios-2018.csv',
    'cleaner_rules': [
        rename_column([
            (u"AÑO", "anio"),
            ("MES", "mes"),
            ("APELLIDO", "apellido"),
            ("NOMBRE", "nombre"),
            ("CARGO", "cargo"),
            ("TOTAL_ASIGNACIONES", "asignacion_mensual"),
            ("SALARIO_FAMILIAR", "salario_familiar"),
            ("DESCUENTOS", "descuentos"),
            ("LIQUIDO", "liquido"),
        ])
    ],
}

target_datasets = [
    obras,
    sueldos2012,
    sueldos2013,
    sueldos2014,
    sueldos2015,
    sueldos2016,
    sueldos2017,
    sueldos2018,
]
