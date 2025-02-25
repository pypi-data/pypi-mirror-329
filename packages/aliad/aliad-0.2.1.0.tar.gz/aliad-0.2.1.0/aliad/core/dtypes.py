from typing import Dict, ClassVar, Type, Optional, Any

from quickstats import DescriptiveEnum

class DataType(DescriptiveEnum):
    """Data types enumeration for cross-language type mapping.
    
    An enumeration that defines common data types and their equivalents across
    different programming environments (Python, NumPy, and C). Each enum member
    represents a data type with its description and corresponding type
    representations.
    
    Attributes
    ----------
    description : str
        Human-readable description of the data type
    python : Optional[Type]
        Equivalent Python built-in type (if available)
    numpy : Optional[str]
        Equivalent NumPy dtype string (if available)
    ctype : Optional[str]
        Equivalent C type declaration (if available)
        
    Class Variables
    --------------
    __aliases__ : ClassVar[Dict[str, str]]
        Maps alternative type names to their canonical enum member names
    
    Examples
    --------
    >>> DataType.INT.description
    'Integers (64 bit)'
    >>> DataType.INT.python
    <class 'int'>
    >>> DataType.INT.numpy
    'int64'
    >>> DataType.parse('FLOAT64')  # Using alias
    <DTypes.FLOAT: ('FLOAT', 'Floating point numbers (64 bit)', float, 'float64', 'double')>
    
    Notes
    -----
    The enum uses tuples to store multiple attributes for each type.
    The order of tuple elements is: (value, description, python_type, numpy_type, c_type)
    """
    
    __aliases__: ClassVar[Dict[str, str]] = {
        'FLOAT64': 'FLOAT',
        'INT64': 'INT',
        'UINT64': 'UINT',
        'CHAR': 'INT8',
        'BYTE': 'INT8'
    }
    
    # Boolean type
    BOOL = ('BOOL', 'Boolean', bool, 'bool', 'bool')
    
    # 8-bit integers
    INT8 = ('INT8', 'Integers (8 bit)', None, 'int8', 'signed char')
    UINT8 = ('UINT8', 'Unsigned integers (8 bit)', None, 'uint8', 'unsigned char')
    
    # 16-bit integers
    INT16 = ('INT16', 'Integers (16 bit)', None, 'int16', 'short')
    UINT16 = ('UINT16', 'Unsigned integers (16 bit)', None, 'uint16', 'unsigned short')
    
    # 32-bit integers
    INT32 = ('INT32', 'Integers (32 bit)', None, 'int32', 'int')
    UINT32 = ('UINT32', 'Unsigned integers (32 bit)', None, 'uint32', 'unsigned int')
    
    # 64-bit integers
    INT = ('INT', 'Integers (64 bit)', int, 'int64', 'long')
    UINT = ('UINT', 'Unsigned integers (64 bit)', None, 'uint64', 'unsigned long')
    
    # Floating point numbers
    FLOAT32 = ('FLOAT32', 'Floating point numbers (32 bit)', None, 'float32', 'float')
    FLOAT = ('FLOAT', 'Floating point numbers (64 bit)', float, 'float64', 'double')
    
    # Special types
    STRING = ('STRING', 'Strings', str, None, None)
    DATETIME = ('DATETIME', 'Datetimes', None, None, None)
    
    def __new__(
        cls,
        value: str,
        description: str,
        python: Optional[Type[Any]] = None,
        numpy: Optional[str] = None,
        ctype: Optional[str] = None
    ) -> 'DTypes':
        """Create new enum member with type mappings.
        
        Parameters
        ----------
        value : str
            The canonical name of the type
        description : str
            Human-readable description of the type
        python : Optional[Type[Any]], optional
            Equivalent Python built-in type, by default None
        numpy : Optional[str], optional
            Equivalent NumPy dtype string, by default None
        ctype : Optional[str], optional
            Equivalent C type declaration, by default None
            
        Returns
        -------
        DTypes
            New enum member with specified attributes
        """
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.python = python
        obj.numpy = numpy
        obj.ctype = ctype
        return obj