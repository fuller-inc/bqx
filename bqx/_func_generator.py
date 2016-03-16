_func = {}

_func['aggregate'] = [
    'AVG',
    'BIT_AND',
    'BIT_OR',
    'BIT_XOR',
    'CORR',
    'COUNT',
    'COVAR_POP',
    'COVAR_SAMP',
    'EXACT_COUNT_DISTINCT',
    'FIRST',
    'GROUP_CONCAT',
    'GROUP_CONCAT_UNQUOTED',
    'LAST',
    'MAX',
    'MIN',
    'NEST',
    'NTH',
    'QUANTILES',
    'STDDEV',
    'STDDEV_POP',
    'STDDEV_SAMP',
    'SUM',
    'TOP',
    'UNIQUE',
    'VARIANCE',
    'VAR_POP',
    'VAR_SAMP'
]

_func['arithmetic'] = [
    'BIT_COUNT'
]

_func['casting'] = [
    'BOOLEAN',
    # 'CAST',  # Implemented.
    'FLOAT',
    'HEX_STRING',
    'INTEGER',
    'STRING'
]

_func['comparison'] = [
    # 'BETWEEN'  # Implemented.
    # 'IS_NULL', # Implemented.
    # 'IN',  # Implemented.
    'COALESCE',
    'GREATEST',
    'IFNULL',
    'IS_INF',
    'IS_NAN',
    'IS_EXPLICITLY_DEFINED',
    'LEAST',
    'NVL'
]

_func['date'] = [
    'CURRENT_DATE',
    'CURRENT_TIME',
    'CURRENT_TIMESTAMP',
    'DATE',
    'DATE_ADD',
    'DATEDIFF',
    'DAY',
    'DAYOFWEEK',
    'DAYOFYEAR',
    'FORMAT_UTC_USEC',
    'HOUR',
    'MINUTE',
    'MONTH',
    'MSEC_TO_TIMESTAMP',
    'NOW',
    'PARSE_UTC_USEC',
    'QUARTER',
    'SEC_TO_TIMESTAMP',
    'SECOND',
    'STRFTIME_UTC_USEC',
    'TIME',
    'TIMESTAMP',
    'TIMESTAMP_TO_MSEC',
    'TIMESTAMP_TO_SEC',
    'TIMESTAMP_TO_USEC',
    'USEC_TO_TIMESTAMP',
    'UTC_USEC_TO_DAY',
    'UTC_USEC_TO_HOUR',
    'UTC_USEC_TO_MONTH',
    'UTC_USEC_TO_WEEK',
    'UTC_USEC_TO_YEAR',
    'WEEK',
    'YEAR'
]

_func['ip'] = [
    'FORMAT_IP',
    'PARSE_IP',
    'FORMAT_PACKED_IP',
    'PARSE_PACKED_IP'
]

_func['json'] = [
    'JSON_EXTRACT',
    'JSON_EXTRACT_SCALAR'
]

_func['math'] = [
    'ABS',
    'ACOS',
    'ACOSH',
    'ASIN',
    'ASINH',
    'ATAN',
    'ATANH',
    'ATAN2',
    'CEIL',
    'COS',
    'COSH',
    'DEGREES',
    'EXP',
    'FLOOR',
    'LN',
    'LOG',
    'LOG2',
    'LOG10',
    'PI',
    'POW',
    'RADIANS',
    'RAND',
    'ROUND',
    'SIN',
    'SINH',
    'SQRT',
    'TAN',
    'TANH'
]

_func['regex'] = [
    'REGEXP_MATCH',
    'REGEXP_EXTRACT',
    'REGEXP_REPLACE'
]

_func['string'] = [
    #'CONTAINS',  # Implemented.
    #'CONCAT',  # Implemented.
    'INSTR',
    'LEFT',
    'LENGTH',
    'LOWER',
    'LPAD',
    'LTRIM',
    'REPLACE',
    'RIGHT',
    'RPAD',
    'RTRIM',
    'SPLIT',
    'SUBSTR',
    'UPPER'
]

_func['table_wildcard'] = [
    'TABLE_DATE_RANGE',
    'TABLE_DATE_RANGE_STRICT',
    'TABLE_QUERY'
]

_func['url'] = [
    'HOST',
    'DOMAIN',
    'TLD'
]

_func['func_syntax'] = [
    'CUME_DIST',
    'DENSE_RANK',
    'FIRST_VALUE',
    'LAG',
    'LAST_VALUE',
    'LEAD',
    'NTH_VALUE',
    'NTILE',
    'PERCENT_RANK',
    'PERCENTILE_CONT',
    'PERCENTILE_DISC',
    'RANK',
    'RATIO_TO_REPORT',
    'ROW_NUMBER'
]

_func['other'] = [
    'CURRENT_USER',
    'EVERY',
    'HASH',
    'IF',
    'POSITION',
    'SOME'
]


def generate_from_dict(d):
    funcs = []
    for _, v in d.items():
        funcs.extend("{fn} = _fn_factory('{fn}')".format(fn=n) for n in v)
    return funcs


def generate_funcpy(funcpy_in, funcpy):
    fl = '\n'.join(generate_from_dict(_func))
    with open(funcpy_in, 'r') as f:
        src = '{funcpy}\n{generated}\n'.format(funcpy=f.read(), generated=fl)

    with open(funcpy, 'w') as f:
        caution = '"""This file is auto-generated from _func.py by setup.py. Do not edit lines!"""\n\n'
        f.write(caution)
        f.write(src)
