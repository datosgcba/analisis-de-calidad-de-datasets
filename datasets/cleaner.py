from data_cleaner import DataCleaner
import os


def clean_and_save(input_path, output_path):
    output_folder = os.path.join(os.path.dirname(output_path))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dc = DataCleaner(input_path)
    dc.clean(rules)
    dc.df.set_index(dc.df.columns[0]).to_csv(
        output_path,
        encoding=dc.OUTPUT_ENCODING,
        sep=dc.OUTPUT_SEPARATOR,
        quotechar=dc.OUTPUT_QUOTECHAR
    )


def rename_column(column_tuples):
    columns = []
    for original_name, new_name in column_tuples:
        columns.append({
            "field": original_name,
            "new_field": new_name
        })
    return {"renombrar_columnas": columns}


if __name__ == '__main__':
    root_datasets_folder = os.path.dirname(__file__)
    csv_input = os.path.join(root_datasets_folder, "obras-registradas", "obras-registradas.csv")
    csv_output = os.path.join(root_datasets_folder, "obras-registradas", "clean", "obras-registradas.csv")

    rules = [
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
    clean_and_save(csv_input, csv_output)
