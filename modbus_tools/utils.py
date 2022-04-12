# enum for metter_types
from enum import Enum

class MetterTypes(Enum):
    """Enumeracion para acotar los tipos de medidores soportados
    """
    G4 = 'G4'
    G4G3 = 'G4G3'
    PBB = 'PBB'

class RegName(Enum):
    """ 'Register Name' Estandarizacion de nombres y registros a leer para medidores PureBB y G44XX
    """
    
    V1N = 'V1N',
    I1 = 'I1',
    V3N = 'V3N',
    I3 = 'I3',
    V2N = 'V2N',
    I2 = 'I2',
    V23 = 'V23',
    V12 = 'V12',
    V31 = 'V31',
    P1 = 'P1',
    P3 = 'P3',
    P2 = 'P2',
    PT = 'PT',
    Q1 = 'Q1',
    Q3 = 'Q3',
    Q2 = 'Q2',
    QT = 'QT',
    S1 = 'S1',
    S3 = 'S3',
    S2 = 'S2',
    ST = 'ST',
    PF1 = 'PF1',
    PF3 = 'PF3',
    PF2 = 'PF2',
    PFT = 'PFT',
    EPinT = 'EPinT',
    EPoutT = 'EPoutT',
    EQinT = 'EQinT',
    EQoutT = 'EQoutT',
    PST23 = 'PST23',
    PST12 = 'PST12',
    PST31 = 'PST31',
    THDI1 = 'THDI1',
    THDI3 = 'THDI3',
    THDI2 = 'THDI2',
    V1pos = 'V1pos',
    I1pos = 'I1pos',
    V1neg = 'V1neg',
    I1neg = 'I1neg',
    V1zero = 'V1zero',
    I1zero = 'I1zero',
    f1_Vneg = "f1_Vneg", 
    f1_Ineg = "f1_Ineg",
    f2_Vneg = "f2_Vneg",
    f2_Ineg = "f2_Ineg",
    f3_Vneg = "f3_Vneg",
    f3_Ineg = "f3_Ineg",
    f1_Vpos = "f1_Vpos",
    f1_Ipos = "f1_Ipos",
    f2_Vpos = "f2_Vpos",
    f2_Ipos = "f2_Ipos",
    f3_Vpos = "f3_Vpos",
    f3_Ipos = "f3_Ipos"