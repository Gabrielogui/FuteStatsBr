from enum import Enum

class StateEnum(str, Enum):
    AC = "AC"; AL = "AL"; AP = "AP"; AM = "AM"; BA = "BA"; CE = "CE"; DF = "DF"
    ES = "ES"; GO = "GO"; MA = "MA"; MT = "MT"; MS = "MS"; MG = "MG"; PA = "PA"
    PB = "PB"; PR = "PR"; PE = "PE"; PI = "PI"; RJ = "RJ"; RN = "RN"; RS = "RS"
    RO = "RO"; RR = "RR"; SC = "SC"; SP = "SP"; SE = "SE"; TO = "TO"

class StateCompleteEnum(str, Enum):
    ACRE = "Acre"; ALAGOAS = "Alagoas"; AMAPA = "Amapá"; AMAZONAS = "Amazonas"; BAHIA = "Bahia"
    CEARA = "Ceará"; DISTRITO_FEDERAL = "Distrito Federal"; ESPIRITO_SANTO = "Espírito Santo"
    GOIAS = "Goiás"; MARANHAO = "Maranhão"; MATO_GROSSO = "Mato Grosso"; MATO_GROSSO_DO_SUL = "Mato Grosso do Sul"
    MINAS_GERAIS = "Minas Gerais"; PARA = "Pará"; PARAIBA = "Paráiba"; PARANA = "Paraná"; PERNAMBUCO = "Pernambuco"
    PIAUI = "Piauí"; RIO_DE_JANEIRO = "Rio de Janeiro"; RIO_GRANDE_DO_NORTE = "Rio Grande do Norte"
    RIO_GRANDE_DO_SUL = "Rio Grande do Sul"; RONDONIA = "Rondônia"; RORAIMA = "Roraima"
    SANTA_CATARINA = "Santa Catarina"; SAO_PAULO = "São Paulo"; SERGIPE = "Sergipe"; TOCANTINS = "Tocantins"

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

class EditionFormatEnum(str, Enum):
    POINTS = "POINTS"               # Pontos Corridos (Ex: Brasileirão atual)
    KNOCKOUT = "KNOCKOUT"           # Mata-mata (Ex: Copa do Brasil)
    HYBRID = "HYBRID"               # Grupos + Mata-mata (Ex: Paulistão, Champions)

class MatchStatusEnum(str, Enum):
    SCHEDULED = "SCHEDULED"
    ONGOING = "ONGOING"
    FINISHED = "FINISHED"
    POSTPONED = "POSTPONED"

class PhaseTypeEnum(str, Enum):
    REGULAR_SEASON = "REGULAR_SEASON" # Rodadas de pontos corridos
    GROUP_STAGE = "GROUP_STAGE"       # Grupos
    PLAYOFFS = "PLAYOFFS"             # Chaveamento de mata-mata

class ColorEnum(str, Enum):
    BRANCO = "BRANCO"; PRETO = "PRETO"; AZUL = "AZUL"; VERMELHO = "VERMELHO"; VERDE = "VERDE"; AMARELO = "AMARELO"
    LARANJA = "LARANJA"; ROSA = "ROSA"; ROXO = "ROXO"; CINZA = "CINZA"

class EntityTypesEnum(str, Enum):
    TEAM = "TEAM"; STADIUM = "STADIUM"; COMPETITION = "COMPETITION"