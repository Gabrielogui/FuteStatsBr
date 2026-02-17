from enum import Enum

class StateEnum(str, Enum):
    AC = "AC"; AL = "AL"; AP = "AP"; AM = "AM"; BA = "BA"; CE = "CE"; DF = "DF"
    ES = "ES"; GO = "GO"; MA = "MA"; MT = "MT"; MS = "MS"; MG = "MG"; PA = "PA"
    PB = "PB"; PR = "PR"; PE = "PE"; PI = "PI"; RJ = "RJ"; RN = "RN"; RS = "RS"
    RO = "RO"; RR = "RR"; SC = "SC"; SP = "SP"; SE = "SE"; TO = "TO"

class CompetitionTypeEnum(str, Enum):
    LEAGUE = "Liga"
    CUP = "Copa"
    STATE = "Estadual"
    REGIONAL = "Regional"
    INTERNATIONAL = "Internacional"

class RegionEnum(str, Enum):
    NACIONAL = "Nacional"
    SUL = "Sul"
    SUDESTE = "Sudeste"
    CENTRO_OESTE = "Centro-Oeste"
    NORDESTE = "Nordeste"
    NORTE = "Norte"
    CONTINENTAL = "Continental"