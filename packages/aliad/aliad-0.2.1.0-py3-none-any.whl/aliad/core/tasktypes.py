from typing import Dict, ClassVar, Type, Optional, Any

from quickstats import DescriptiveEnum

class TaskType(DescriptiveEnum):

    BINCLASS = ('BINCLASS', 'Binary Classification')

    MULTICLASS = ('MULTICLASS', 'Multi-Class Classification')

    REGRESSION = ('REGRESSION', 'Regression')