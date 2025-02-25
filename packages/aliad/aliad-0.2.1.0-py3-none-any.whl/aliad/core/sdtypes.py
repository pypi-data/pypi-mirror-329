from typing import Dict, ClassVar

from quickstats import DescriptiveEnum

class StatDataType(DescriptiveEnum):
    """Statistical data type enumeration.
    
    An enumeration class that defines different types of statistical data,
    including numerical, categorical, binary, count, and positive real numbers.
    Inherits from DescriptiveEnum to provide descriptive text for each data type.
    
    Attributes
    ----------
    NUMERICAL : tuple[int, str]
        Represents general numerical data
    CATEGORICAL : tuple[int, str]
        Represents categorical or nominal data with distinct categories
    BINARY : tuple[int, str]
        Represents binary/boolean data
    COUNT : tuple[int, str]
        Represents count data (non-negative integers)
    POSITIVE_REAL : tuple[int, str]
        Represents strictly positive real numbers
        
    Class Variables
    --------------
    __aliases__ : ClassVar[Dict[str, str]]
        Maps alternative names to enum member names. Currently maps 'FLAG' to 'BINARY'
    
    Examples
    --------
    >>> data_type = StatDataType.NUMERICAL
    >>> data_type.description
    'Numerical data that can be positive, negative, or zero'
    
    >>> StatDataType.parse('FLAG')  # Using alias
    <SDTypes.BINARY: 3>
    
    Notes
    -----
    The enum values are assigned integers from 1-5 for internal representation,
    but these values should not be relied upon for any logical operations.
    Use the enum members directly instead.
    """
    
    __aliases__: ClassVar[Dict[str, str]] = {
        'FLAG': 'BINARY',
        'INDICATOR': 'BINARY'
    }
    
    NUMERICAL = (
        'NUMERICAL',
        'Numerical data'
    )
    CATEGORICAL = (
        'CATEGORICAL',
        'Categorical data'
    )
    BINARY = (
        'BINARY',
        'Binary/boolean data'
    )
    COUNT = (
        'COUNT',
        'Non-negative integers'
    )
    POSITIVE_REAL = (
        'POSITIVE_REAL',
        'Strictly positive real numbers'
    )