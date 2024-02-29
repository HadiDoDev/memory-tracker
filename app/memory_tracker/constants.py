from enum import Enum

__all__ = ['TRUE_VALUES', 'FALSE_VALUES', 'NULL_VALUES']


TRUE_VALUES = {
    't', 'T',
    'y', 'Y', 'yes', 'Yes', 'YES',
    'true', 'True', 'TRUE',
    'on', 'On', 'ON',
    '1', 1,
    True
}
FALSE_VALUES = {
    'f', 'F',
    'n', 'N', 'no', 'No', 'NO',
    'false', 'False', 'FALSE',
    'off', 'Off', 'OFF',
    '0', 0, 0.0,
    False
}
NULL_VALUES = {'null', 'Null', 'NULL', 'none', 'None', 'NONE', '', None}


