from dataclasses import fields, asdict
from datetime import datetime

class BaseModel:
    """
    Base class for models with common functionality for field initialization,
    type conversion, and SQL generation.
    """

    def __init__(self, **kwargs):
        """
        Initialize the model with given keyword arguments.
        """
        self._additional_fields = {}
        cls_fields = self._get_class_fields()
        init_values = self._filter_known_fields(cls_fields, kwargs)
        self._set_field_values(cls_fields, init_values)

    def _get_class_fields(self):
        """
        Retrieve the class fields with their aliases.
        """
        return {f.metadata.get('alias', f.name): f for f in fields(self)}

    def _filter_known_fields(self, cls_fields, kwargs):
        """
        Filter the known fields from the provided keyword arguments.
        """
        return {cls_fields[k].name: v for k, v in kwargs.items() if k in cls_fields}

    def _set_field_values(self, cls_fields, init_values):
        """
        Set the field values for the model.
        """
        for f in fields(self):
            value = self._convert_field_type(f.type, init_values.get(f.name, f.default))
            if isinstance(value, str):
                setattr(self, f.name, value.replace('\'', '´'))
            else:
                setattr(self, f.name, value)

    def _convert_field_type(self, field_type, value):
        """
        Convert the field type to the appropriate type.
        """
        if value is None:
            if field_type is str:
                return ''
            elif field_type is int:
                return -1
        if field_type is datetime and isinstance(value, str):
            return self._parse_datetime(value)
        return self._try_convert(field_type, value)

    def _parse_datetime(self, value):
        """
        Parse a string to a datetime object.
        """
        try:
            return datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return value

    def _try_convert(self, field_type, value):
        """
        Try to convert the value to the specified field type.
        """
        try:
            return field_type(value)
        except (TypeError, ValueError):
            return value

    def _to_sql(self, field_name):
        """
        Check if the field should be included in SQL operations.
        """

        return next(f for f in fields(self) if f.name == field_name).metadata.get('to_sql', True)

    def _format_field_value(self, value):
        """
        Format the field value for SQL.
        """
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S.%f')
        return value

    def _get_unique(self):
        """
        Retrieve if the value must be unique.
        """
        for f in fields(self):
            if f.metadata.get('unique', False):
                return f.metadata.get('field_name', f.name)

    def get_unique_fields(self):
        """
        Retrieve the model's unique fields
        :returns: A list, containing the model's unique fields, identified by 'field_name'
        """
        ret: list = []
        for f in fields(self):
            if f.metadata.get('unique', False):
                ret.append(f.metadata.get('field_name', f.name))
        return ret

    def get_sql_update_fields(self):
        """
        Retrieve fields needed for an update clause in an sql query, i.e. fields with "to_sql": True && "unique": False
        """
        ret: list = []
        for f in fields(self):
            if self._to_sql(f.name) and not f.metadata.get('unique', False):
                ret.append(f.metadata.get('field_name', f.name))
        return ret

    def _get_primary_key(self):
        """
        Retrieve the primary key field name.
        """
        for f in fields(self):
            if f.metadata.get('primary_key', False):
                return f.name
        raise ValueError("No primary key defined")

    def to_dict(self):
        """
        Convert the model to a dictionary, excluding fields not meant for SQL.
        """
        dict = {}
        for f in fields(self):
            if self._to_sql(f.name):
                key = f.metadata.get('field_name', f.name)
                dict.update({key: getattr(self, f.name)})
        return dict

    def add_to_sql(self, additional_fields):
        """
        Add additional fields to be included in SQL operations.
        """
        self._additional_fields.update(additional_fields)


    def to_sql(self):
        """
        Generate a dictionary with the values ready for SQL operations.
        """
        data = self.to_dict()
        data.update(self._additional_fields)
        return {k: self._format_field_value(v) for k, v in data.items()}

    def to_query(self, schema_db=None, table_name=None):
        """
        Generate an SQL insert/update statement for the model.
        """
        data = self.to_sql()
        columns = ', '.join(data.keys())
        table_name = table_name if table_name else f"{schema_db}.{self.__class__.__name__.lower()}" if schema_db else self.__class__.__name__.lower()
        full_table_name = f"{schema_db}.{table_name}" if schema_db else table_name
        values = ', '.join(f"'{v}'" if isinstance(v, str) else str(v) for v in data.values())

        unique = self._get_unique()
        update = ''
        for k, v in data.items():
            if k != unique:
                update += f"{k} = '{v}', " if isinstance(v, str) else f"{k} = {v}, "
        update += f"ult_modificado = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}'"
        updates = ''.join(update)

        return (f"INSERT INTO {full_table_name} ({columns}) VALUES ({values}) "
                f"ON CONFLICT ({unique}) DO UPDATE SET {updates};")

    # def to_query(self, schema_db=None, table_name=None):
    #     """
    #     Generate an SQL insert/update statement for the model.
    #     """
    #     data = self.to_sql()
    #     columns = ', '.join(data.keys())
    #     table_name = table_name if table_name else f"{schema_db}.{self.__class__.__name__.lower()}" if schema_db else self.__class__.__name__.lower()
    #     full_table_name = f"{schema_db}.{table_name}" if schema_db else table_name
    #     values = ', '.join(f"'{v}'" if isinstance(v, str) else str(v) for v in data.values())
    #
    #     return (f"INSERT INTO {full_table_name} ({columns}) VALUES ({values}))"


def sql_bulk(models, schema_db=None, table_name=None):
    """
    Generate a bulk SQL insert statement for a list of models, using an ON CONFLICT/UPDATE clause when needed.

    :param models: List of model instances.
    :param schema_db: Optional schema database name.
    :param table_name: Optional table name.
    :return: Bulk SQL insert statement.
    """
    if not models:
        return ""

    table_name = table_name if table_name else models[0].__class__.__name__.lower()
    full_table_name = f"{schema_db}.{table_name}" if schema_db else table_name
    columns = ', '.join(models[0].to_sql().keys())

    values_tuples = []
    for model in models:
        values = ', '.join(f"'{v}'" if isinstance(v, str) else str(v) for v in model.to_sql().values())
        values_tuples.append(f"({values})")
    values_clause = ', '.join(values_tuples)

    query = f"""INSERT INTO {full_table_name} ({columns}) VALUES {values_clause}"""

    unique_fields = models[0].get_unique_fields()
    if not unique_fields:
        return query + ";"

    on_conflict_columns = ', '.join(models[0].get_unique_fields())
    update_columns = models[0].get_sql_update_fields()
    on_conflict_update_str = ", ".join(
        [f"{col} = EXCLUDED.{col}" for col in update_columns] + ["ult_modificado = NOW()"]
    )

    query += f"""
    ON CONFLICT ({on_conflict_columns})
    DO UPDATE SET {on_conflict_update_str};
    """

    return query
