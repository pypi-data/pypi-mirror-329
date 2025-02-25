from enum import Enum


class SitkMetricType(str, Enum):
    MeanSquares = "MeanSquares"
    CrossCorrelation = "CrossCorrelation"
    ANTSNeighborhoodCorrelation = "ANTSNeighborhoodCorrelation"
    JointHistogramMutualInformation = "JointHistogramMutualInformation"
    MattesMutualInformation = "MattesMutualInformation"


class SitkOptimizerType(str, Enum):
    Exhaustive = "Exhaustive"
    Powell = "Powell"
    Evolutionary = "Evolutionary"
    GradientDescent = "GradientDescent"
    GradientDescentLineSearch = "GradientDescentLineSearch"
    CGLineSearch = "CGLineSearch"
    LBFGSB = "LBFGSB"


class KorniaMetricType(str, Enum):
    MeanAbsoluteError = "MeanAbsoluteError"
    MeanSquaredError = "MeanSquaredError"
    MutualInformation = "MutualInformation"


class KorniaOptimizerType(str, Enum):
    Adam = "Adam"
    SGD = "SGD"
    RMSprop = "RMSprop"
