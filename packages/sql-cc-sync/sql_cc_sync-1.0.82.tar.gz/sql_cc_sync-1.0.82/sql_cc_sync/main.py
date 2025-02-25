import sys
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field, InitVar
from itertools import chain

from typing import List, Tuple, Dict, Optional, Union, Any, Sequence, cast

from rich.console import Console
from rich.panel import Panel
from rich.markup import escape

import percival as pv
from combocurve_api_helper import ComboCurveAPI, Item, ItemList

from .types import Literals, WellDict, WellList
from .cc_wellheader import CC_WELLHEADER

API = ComboCurveAPI()

CONSOLE = Console()


COMPANY_DATABASES = ['EIV', 'EIV2', 'ARP']
SQL_DATABASES = [*COMPANY_DATABASES, 'VDR', 'Xcalibur']


# def get_databases() -> List[str]:
#     sql = """
#     SELECT
#         [name]

#     FROM [master].[sys].[databases]

#     WHERE [name] NOT IN ('master', 'tempdb', 'model', 'msdb')
#     ;
#     """

#     tf = pv.tf.read(sql)
#     return tf[tf.columns[0]].tolist()


# SQL_DATABASES = get_databases()


def print(message: Any, *args: Any, **kwargs: Any) -> None:
    CONSOLE.print(message, *args, **kwargs)


def print_error(message: Any, *args: Any, **kwargs: Any) -> None:
    msg = str(message)
    print(f'[bold red]{msg}[/]', *args, **kwargs)


SQL = '[yellow]SQL[/]'
SQL_LC = '[yellow]sql[/]'
COMBOCURVE = '[green]ComboCurve[/]'
CC_LC = '[green]cc[/]'

QUIT_RESPONSE = ('n', 'no', 'e', 'exit', 'q', 'quit')


DEFAULT_DATABASE = 'VDR'
DEFAULT_TABLE = 'AC_PROPERTY'


SQL_SCHEMAS = """
SELECT
    [SCHEMA_NAME] AS [Schema]

FROM [{database}].[INFORMATION_SCHEMA].[SCHEMATA]

WHERE [SCHEMA_OWNER] NOT LIKE 'db\_%'
;

"""


SQL_TABLES = """
SELECT
    [TABLE_NAME] AS [Table]

FROM [{database}].[INFORMATION_SCHEMA].[Tables]

WHERE [TABLE_SCHEMA] = '{schema}'
;
"""


SQL_COLUMNS = """
SELECT
    [COLUMN_NAME] AS [Column]

FROM [{database}].[INFORMATION_SCHEMA].[COLUMNS]

WHERE [TABLE_SCHEMA] = '{schema}'
  AND [TABLE_NAME] = '{table}'
;
"""


SQL_MISSING_UPDATE_COLUMN = """
SELECT [{update_column}] FROM [{database}].[{schema}].[{table}] WHERE [{update_column}] IS NULL
;
"""


SQL_UPDATE_COLUMN = """
SELECT [{join_column}], [{update_column}] FROM [{database}].[{schema}].[{table}]
;
"""


SQL_CREATE_STAGING_TABLE = """
CREATE TABLE [{database}].[stg].[{schema}_cc_sql_sync] (
     [{join_column}] varchar(255)
    ,[{update_column}] varchar(255)
);
"""


SQL_DROP_STAGING_TABLE = """
DROP TABLE IF EXISTS [{database}].[stg].[{schema}_cc_sql_sync];
"""


SQL_INSERT_STAGING_TABLE = """
INSERT INTO [{database}].[stg].[{schema}_cc_sql_sync] (
     [{join_column}]
    ,[{update_column}]
)
VALUES
    (?, ?)
;
"""


SQL_UPDATE_VALUES = """
BEGIN TRAN;

UPDATE a
SET
    a.[{update_column}] = v.[{update_column}]

FROM [{database}].[{schema}].[{table}] AS a

INNER JOIN [{database}].[stg].[{schema}_cc_sql_sync] AS v
    ON v.[{join_column}] = CONVERT(varchar(128), a.[{join_column}])
;

COMMIT TRAN;
"""


SQL_COUNT_SUMMARY = """
SELECT
    'OK' AS [Status]
    ,COUNT(*) AS [Count]

FROM [{database}].[{schema}].[{table}] AS a

INNER JOIN [{database}].[stg].[{schema}_cc_sql_sync] AS v
    ON v.[{join_column}] = CONVERT(varchar(128), a.[{join_column}])

WHERE a.[{update_column}] IS NOT NULL

UNION ALL

SELECT
    'Null' AS [Status]
    ,COUNT(*) AS [Count]

FROM [{database}].[{schema}].[{table}] AS a

INNER JOIN [{database}].[stg].[{schema}_cc_sql_sync] AS v
    ON v.[{join_column}] = CONVERT(varchar(128), a.[{join_column}])

WHERE a.[{update_column}] IS NULL
;
"""


@dataclass
class ArgCache:
    args: InitVar[Namespace]
    update_target: str = field(init=False)
    cc_project_name: str = field(init=False)
    cc_project_id: str = field(init=False)
    sql_database: str = field(init=False)
    sql_schema: str = field(init=False)
    sql_table: str = field(init=False)
    sql_join_column: str = field(init=False)
    cc_join_column: str = field(init=False)
    sql_update_column: str = field(init=False)
    cc_update_column: str = field(init=False)
    one_shot: bool = field(init=False)
    cc_wells: WellList = field(init=False)
    cc_custom_columns: Dict[str, str] = field(init=False)
    cc_custom_columns_reverse: Dict[str, str] = field(init=False)

    sql_schemas: List[str] = field(init=False)
    sql_tables: List[str] = field(init=False)
    sql_columns: List[str] = field(init=False)


    def __post_init__(self, args: Namespace) -> None:
        self.update_target = args.update_target
        self.cc_project_name = args.project_name
        self.sql_database = args.database
        self.sql_schema = args.schema
        self.sql_table = args.table
        self.sql_join_column = args.sql_join_column
        self.cc_join_column = args.cc_join_column
        self.sql_update_column = args.sql_update_column
        self.cc_update_column = args.cc_update_column
        self.one_shot = args.one_shot

        self.cc_wells = [{}]

        self.sql_schemas = []
        self.sql_tables = []
        self.sql_columns = []

        self.cache_custom_columns()
        self.validate_args()
        self.get_cc_project_id()


    def cache_custom_columns(self) -> None:
        self.cc_custom_columns_reverse = API.get_custom_columns('wells')  # type: ignore
        self.cc_custom_columns = {v: k for k, v in self.cc_custom_columns_reverse.items()}


    def cache_cc_wells(self, filters: Optional[Dict[str, str]] = None) -> None:
        self.cc_wells = cast(WellList, API.get_project_wells(project_id=self.cc_project_id, filters=filters))

        if self.sql_database in COMPANY_DATABASES:
            self.cc_wells.extend(cast(WellList, API.get_project_company_wells(
                project_id=self.cc_project_id, filters=filters)))


    def get_escaped_sql_name(self) -> str:
        return escape(f'[{self.sql_database}].[{self.sql_schema}].[{self.sql_table}]')


    def get_cc_project_id(self) -> None:
        # filters = {'name': self.cc_project_name}
        projects = API.get_projects()
        for (name, id_) in ((str(p['name']), str(p['id'])) for p in projects):
            if self.cc_project_name.lower() == name.lower():
                self.cc_project_name = name
                self.cc_project_id = id_
                return

        print(f'Invalid {COMBOCURVE} project name: [red]{self.cc_project_name}[/]')
        sys.exit(1)


    def validate_args(self) -> None:
        self.cc_join_column = self.validate_cc_column(self.cc_join_column)
        self.cc_update_column = self.validate_cc_column(self.cc_update_column)
        self.sql_database = self.validate_database(self.sql_database)
        self.sql_schema = self.validate_schema(self.sql_schema)
        self.sql_table = self.validate_table(self.sql_table)
        self.sql_join_column = self.validate_sql_column(self.sql_join_column)
        self.sql_update_column = self.validate_sql_column(self.sql_update_column)


    def validate_database(self, database: str) -> str:
        for (l, s) in ((s.lower(), s) for s in SQL_DATABASES):
            if database.lower() == l:
                return s

        print(f'\nInvalid database: [red]{database}[/]\n\n'
              f'Valid databases:\n{SQL_DATABASES}')
        sys.exit(1)


    def validate_schema(self, schema: str) -> str:
        if len(self.sql_schemas) == 0:
            df_schemas = pv.read(SQL_SCHEMAS.format(database=self.sql_database))
            self.sql_schemas = df_schemas['Schema'].tolist()

        for (l, s) in ((s.lower(), s) for s in self.sql_schemas):
            if schema.lower() == l:
                return s

        print(f'\nInvalid schema: [red]{schema}[/]\n\n'
              f'Valid schemas:\n{self.sql_schemas}')
        sys.exit(1)


    def validate_table(self, table: str) -> str:
        if len(self.sql_tables) == 0:
            df_tables = pv.read(SQL_TABLES.format(database=self.sql_database, schema=self.sql_schema))
            self.sql_tables = df_tables['Table'].tolist()

        for (l, s) in ((s.lower(), s) for s in self.sql_tables):
            if table.lower() == l:
                return s

        print(f'\nInvalid table: [red]{table}[/]\n\n'
              f'Valid tables:\n{self.sql_tables}')
        sys.exit(1)


    def _validate_sql_column(self, column: str) -> Tuple[bool, str]:
        if len(self.sql_columns) == 0:
            df_columns = pv.read(SQL_COLUMNS.format(
                database=self.sql_database, schema=self.sql_schema, table=self.sql_table))
            self.sql_columns = df_columns['Column'].tolist()

        for (l, c) in ((c.lower(), c) for c in self.sql_columns):
            if column.lower() == l:
                return True, c

        print(f'\nInvalid {SQL} column: [red]{column}[/]\n\nValid columns:')
        print(f'{self.sql_columns}\n', sep='')
        return False, ''


    def validate_sql_column(self, column: str) -> str:
        found, column = self._validate_sql_column(column)
        if found:
            return column

        sys.exit(1)


    def validate_sql_column_update(self, column: str) -> Tuple[bool, str]:
        return self._validate_sql_column(column)


    def _validate_cc_column(self, column: str) -> Tuple[bool, str]:
        for (l, k) in ((k.lower(), k) for k in CC_WELLHEADER.keys()):
            if column.lower() == l:
                return True, k

        for (l, k) in ((k.lower(), k) for k in self.cc_custom_columns.keys()):
            if column.lower() == l:
                return True, self.cc_custom_columns[k]

        columns = list(chain(CC_WELLHEADER.keys(), self.cc_custom_columns.keys()))
        print(f'\nInvalid {COMBOCURVE} column: [red]{column}[/]\n\nValid columns:')
        print(f'{columns}\n', sep='')
        return False, ''


    def validate_cc_column(self, column: str) -> str:
        found, column = self._validate_cc_column(column)
        if found:
            return column

        sys.exit(1)


    def validate_cc_column_update(self, column: str) -> Tuple[bool, str]:
        return self._validate_cc_column(column)


    def validate_update_target(self, update_target: str) -> Tuple[bool, str]:
        if update_target in ('sql', 'cc'):
            return True, update_target

        print(f'Invalid update target: [red]{update_target}[/]\n'
              f'Must be either: {SQL_LC} or {CC_LC}\n')
        return False, ''


    def set_update_columns(self) -> None:
        print('\n[blue]Enter new values to update another column.[/]')

        valid: bool = False
        while not valid:
            response = CONSOLE.input(f'Update Target: [{SQL_LC} / {CC_LC} / [red]exit[/]]: ')
            if response in QUIT_RESPONSE:
                exit_program()

            valid, self.update_target = self.validate_update_target(response)

        valid = False
        while not valid:
            response = CONSOLE.input(f'{SQL} Update Column: [[yellow]<sql column>[/] / [red]exit[/]]: ')
            if response in QUIT_RESPONSE:
                exit_program()

            valid, self.sql_update_column = self.validate_sql_column_update(response)

        valid = False
        while not valid:
            response = CONSOLE.input(f'{COMBOCURVE} Update Column: [[green]<cc column>[/] / [red]exit[/]]: ')
            if response in QUIT_RESPONSE:
                exit_program()

            valid, self.cc_update_column = self.validate_cc_column_update(response)


def update_values_sql(
    cache: ArgCache, values: List[Tuple[Literals, Literals]],
    database: str, schema: str, table: str, join_column: str, update_column: str
) -> str:
    try:
        pv.execute(SQL_DROP_STAGING_TABLE.format(database=database, schema=schema))
        pv.execute(SQL_CREATE_STAGING_TABLE.format(
            database=database, schema=schema, join_column=join_column, update_column=update_column))
        pv.insert(SQL_INSERT_STAGING_TABLE.format(
            database=database, schema=schema, join_column=join_column, update_column=update_column), values)
        pv.execute(SQL_UPDATE_VALUES.format(
            database=database, schema=schema, table=table, join_column=join_column, update_column=update_column))
        df_counts = pv.read(SQL_COUNT_SUMMARY.format(
            database=database, schema=schema, table=table, join_column=join_column, update_column=update_column))
    except Exception as e:
        raise e

    finally:
        pv.execute(SQL_DROP_STAGING_TABLE.format(database=database, schema=schema))

    status = {k: v for k, v in zip(df_counts['Status'], df_counts['Count'])}

    matched_wells = sum(status.values())
    status['Unmatched'] = len(cache.cc_wells) - matched_wells

    summary = 'Update Summary:'
    for k, v in status.items():
        v = status[k]
        if k == 'OK':
            color = '[green]'
        elif k == 'Error':
            color = '[red]'
        else:
            color = '[yellow]'

        summary += f'\n  {color}{(k + ":").ljust(11)}[/] {v} wells'

    return summary


def cc_to_sql(cache: ArgCache) -> None:
    response = ''
    while response not in ('y', *QUIT_RESPONSE):
        response = CONSOLE.input(
            f'Updating [#f1c40f]{len(cache.cc_wells)}[/] wells in '
            f'[yellow]{cache.get_escaped_sql_name()}[/] from {COMBOCURVE}. '
            f'Continue? [[green]y[/] / [red]n[/]]: ').lower()

        if response in QUIT_RESPONSE:
            exit_program()
        elif response == 'y':
            break

    insert_values = [
        (well[cache.cc_join_column], well[cache.cc_update_column]) for well in cache.cc_wells
        if cache.cc_join_column in well and cache.cc_update_column in well
    ]

    status_message = 'Updating... '
    with CONSOLE.status(status_message):
        summary = update_values_sql(
            cache, insert_values,
            database=cache.sql_database, schema=cache.sql_schema, table=cache.sql_table,
            join_column=cache.sql_join_column, update_column=cache.sql_update_column)
    print(f'{status_message}Done!')
    print(summary)


def filter_to_well(cc_wells: WellList, sql_well: WellDict,
                   cc_join_column: str, sql_join_column: str) -> Optional[WellDict]:
    for well in cc_wells:
        if well[cc_join_column] == sql_well[sql_join_column]:
            return well
    else:
        return None


def get_sql_wells(database: str, schema: str, table: str, join_column: str, update_column: str) -> WellList:
    df_wells = pv.read(SQL_UPDATE_COLUMN.format(
        database=database, schema=schema, table=table, join_column=join_column, update_column=update_column))
    wells: WellList = df_wells.to_dict('records')
    return wells


def update_values_cc(cache: ArgCache, data: WellList, null_count: int) -> str:
    results: WellList

    if len(data) == 0:
        # No data to update
        results = []

    else:
        try:
            if cache.sql_database not in COMPANY_DATABASES:
                response = API.patch_project_wells(project_id=cache.cc_project_id, data=cast(ItemList, data))
            else:
                response = API.patch_company_wells(data=cast(ItemList, data))

            results = cast(WellList, response[0].get('results', []))

        except IndexError:
            results = []

    status: Dict[str, int] = {}
    for r in results:
        stat = str(r['status'])
        status.setdefault(stat, 0)
        status[stat] += 1

        if stat == 'Error':
            print(f'Error: {r}')

    status['Null'] = null_count

    unmatched_wells = cache.cc_wells.copy()
    matched_wells: WellList = []
    for d in data:
        for i, well in enumerate(unmatched_wells):
            if well['chosenID'] == d['chosenID'] and well['dataSource'] == d['dataSource']:
                well[cache.cc_update_column] = d[cache.cc_update_column]
                break
        else:
            continue

        matched_wells.append(unmatched_wells.pop(i))

    status['Unmatched'] = len(unmatched_wells)

    cache.cc_wells = matched_wells + unmatched_wells

    summary = 'Update Summary:'
    for k, v in status.items():
        if k == 'OK':
            color = '[green]'
        elif k == 'Error':
            color = '[red]'
        else:
            color = '[yellow]'

        summary += f'\n  {color}{(k + ":").ljust(11)}[/] {v} wells'

    return summary


def sql_to_cc(cache: ArgCache) -> None:
    response = ''
    while response not in ('y', *QUIT_RESPONSE):
        response = CONSOLE.input(
            f'Updating [#f1c40f]{len(cache.cc_wells)}[/] wells in {COMBOCURVE} '
            f'from [yellow]{cache.get_escaped_sql_name()}[/]. '
            f'Continue? [[green]y[/] / [red]n[/]]: ').lower()

        if response in QUIT_RESPONSE:
            exit_program()
        elif response == 'y':
            break


    def _format_value(value: Any, column: Literals) -> Any:
        if isinstance(column, str):
            if isinstance(value, bool):
                return str(value)

            elif isinstance(value, int):
                return str(int(value))

            elif isinstance(value, float):
                if value.is_integer():
                    return str(int(value))
                else:
                    return str(float(value))

            else:
                return str(value)

        elif isinstance(column, bool):
            return bool(value)

        elif isinstance(column, (float, int)):
            return float(value)


    sql_wells = get_sql_wells(
        database=cache.sql_database, schema=cache.sql_schema, table=cache.sql_table,
        join_column=cache.sql_join_column, update_column=cache.sql_update_column)

    patch_values: WellList = list()
    null_count: int = 0
    for sql_well in sql_wells:
        cc_well = filter_to_well(
            cc_wells=cache.cc_wells, sql_well=sql_well,
            cc_join_column=cache.cc_join_column, sql_join_column=cache.sql_join_column)
        if cc_well is None:
            continue

        value = sql_well[cache.sql_update_column]
        formatted_value: Any

        if value is not None:
            if str(value).lower() in ('none', 'null', 'nan', 'nat'):
                null_count += 1
                continue

            else:
                formatted_value = _format_value(value, CC_WELLHEADER[cache.cc_update_column])

        patch_values.append({
            'chosenID': cc_well['chosenID'],
            'dataSource': cc_well['dataSource'],
            cache.cc_update_column: formatted_value
        })

    status_message = 'Updating... '
    with CONSOLE.status(status_message):
        summary = update_values_cc(cache, patch_values, null_count)
    print(f'{status_message}Done!')
    print(summary)


def build_update_statement(cache: ArgCache) -> Panel:
    if cache.update_target == 'sql':
        arrow = '[dodger_blue1]<-[/] '
    elif cache.update_target == 'cc':
        arrow = '[dodger_blue1]->[/] '

    statement = f'[#f39c12]Updating[/] [yellow][{cache.sql_update_column}][/] '
    statement += arrow
    statement += f'[green]{cache.cc_update_column}[/] '
    if (cc_alias := cache.cc_custom_columns_reverse.get(cache.cc_update_column)) is not None:
        statement += f'[green]({cc_alias})[/] '
    statement += '[#f39c12]for[/] '
    statement += f'[yellow]{cache.get_escaped_sql_name()}[/] '
    statement += arrow
    statement += f'[green]{cache.cc_project_name}[/] '
    statement += '[#f39c12]joining on[/] '
    statement += f'[yellow][{cache.sql_join_column}][/] '
    statement += arrow
    statement += f'[green]{cache.cc_join_column}[/] '

    return Panel(statement)


def make_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        'update_target',
        metavar='update-target',
        choices=['sql', 'cc'],
        help='ComboCurve Project Name',
        type=str,
    )
    parser.add_argument(
        'schema',
        metavar='schema',
        help='VDR schema',
        type=str,
    )
    parser.add_argument(
        'project_name',
        metavar='project-name',
        help='ComboCurve Project Name',
        type=str,
    )
    parser.add_argument(
        'sql_join_column',
        metavar='sql-join-column',
        help='SQL Database Column to Join On',
        type=str,
    )
    parser.add_argument(
        'cc_join_column',
        metavar='cc-join-column',
        help='ComboCurve Column to Join On',
        type=str,
    )
    parser.add_argument(
        'sql_update_column',
        metavar='sql-update-column',
        help='SQL Database Column to Join On',
        type=str,
    )
    parser.add_argument(
        'cc_update_column',
        metavar='cc-update-column',
        help='ComboCurve Column to Join On',
        type=str,
    )
    parser.add_argument(
        '--database',
        help='SQL database name',
        type=str,
        default=DEFAULT_DATABASE,
    )
    parser.add_argument(
        '--table',
        help='SQL table name',
        type=str,
        default=DEFAULT_TABLE,
    )
    parser.add_argument(
        '--one-shot',
        help='One-shot mode',
        action='store_true',
    )

    return parser


def exit_program() -> None:
    print('\nGoodbye!')
    CONSOLE.rule()
    sys.exit(0)


def main() -> None:
    args = make_parser().parse_args()
    cache = ArgCache(args)

    status_message = f'Getting well data from {COMBOCURVE} API for [green]{cache.cc_project_name}[/]... '
    with CONSOLE.status(status_message):
        cache.cache_cc_wells()
    print(f'{status_message}Done!')

    if len(cache.cc_wells) == 0:
        print('\n[cyan]No wells found in project.[/] Exiting...\n')
        exit_program()

    while True:
        print(build_update_statement(cache))

        if cache.update_target == 'sql':
            cc_to_sql(cache)

        elif cache.update_target == 'cc':
            sql_to_cc(cache)

        if cache.one_shot:
            break

        CONSOLE.rule()
        cache.set_update_columns()

    sys.exit(0)


if __name__ == '__main__':
    main()
