from .enum_base import EnumBase


class GameType(EnumBase):
    """
    Enum for MLB Game Types.

    REGULAR_SEASON = "R",
    PLAYOFFS = "PO",
    WILDCARD = "F",
    DIVISION_SERIES = "D",
    LEAGUE_CHAMPIONSHIP = "L",
    WORLD_SERIES = "W",
    SPRING_TRAINING = "S",
    ALL_STAR = "A"
    """

    REGULAR_SEASON = 'R'
    PLAYOFFS = 'PO'
    WILDCARD = 'F'
    DIVISION_SERIES = 'D'
    LEAGUE_CHAMPIONSHIP = 'L'
    WORLD_SERIES = 'W'
    SPRING_TRAINING = 'S'
    ALL_STAR = 'A'


class Month(EnumBase):
    """
    Enum for available Months.

    MARCH_AND_APRIL = "4",
    MAY = "5",
    JUNE = "6",
    JULY = "7",
    AUGUST = "8",
    SEPTEMBER_AND_OCTOBER = "9"
    """

    MARCH_AND_APRIL = '4'
    MAY = '5'
    JUNE = '6'
    JULY = '7'
    AUGUST = '8'
    SEPTEMBER_AND_OCTOBER = '9'


class MlbTeam(EnumBase):
    """
    Enum for MLB Teams.

    Check MLB Team Codes from https://github.com/jasonlttl/gameday-api-docs/blob/master/team-information.md
    """

    BLUE_JAYS = 'TOR'
    ORIOLES = 'BAL'
    RAYS = 'TB'
    RED_SOX = 'BOS'
    YANKEES = 'NYY'
    GUARDIANS = 'CLE'
    ROYALS = 'KC'
    TIGERS = 'DET'
    TWINS = 'MIN'
    WHITE_SOX = 'CWS'
    ANGELS = 'LAA'
    ASTROS = 'HOU'
    ATHLETICS = 'OAK'
    MARINERS = 'SEA'
    RANGERS = 'TEX'
    BRAVES = 'ATL'
    MARLINS = 'MIA'
    METS = 'NYM'
    NATIONALS = 'WSH'
    PHILLIES = 'PHI'
    BREWERS = 'MIL'
    CARDINALS = 'STL'
    CUBS = 'CHC'
    PIRATES = 'PIT'
    REDS = 'CIN'
    DIAMONDBACKS = 'AZ'
    DODGERS = 'LAD'
    GIANTS = 'SF'
    PADRES = 'SD'
    ROCKIES = 'COL'
    AMERICAN_LEAGUE = 'AmericanL'
    NATIONAL_LEAGUE = 'NationalL'
