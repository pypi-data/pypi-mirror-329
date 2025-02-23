class BizException(Exception):
    def __init__(self, code: int, msg: str):
        self.code: int = code
        self.msg: str = msg
        super().__init__(self.msg)

class GameAlready4Players(BizException):
    def __init__(self):
        super().__init__(10001, "Game already has 4 players!")

class GamePlayerAlreadyAdded(BizException):
    def __init__(self):
        super().__init__(10002, "Game player already added!")

class GamePlayerNotFound(BizException):
    def __init__(self):
        super().__init__(10003, "Game player not found!")

class GamePartnerAlreadyChosenException(BizException):
    def __init__(self):
        super().__init__(10004, "Partner already chosen!")

class GameNotReadyToDealYetException(BizException):
    def __init__(self):
        super().__init__(10005, "Game not ready to deal yet!")

class GameAlreadyDealtException(BizException):
    def __init__(self):
        super().__init__(10006, "Game already dealt the cards!")

class GameInvalidBidStateException(BizException):
    def __init__(self):
        super().__init__(10007, "Game invalid bid state!")

class GameNotPlayerBidTurnException(BizException):
    def __init__(self):
        super().__init__(10008, "Game not player's turn to bid!")

class GameAuctionNotFinishedException(BizException):
    def __init__(self):
        super().__init__(10009, "Game auction not finished yet!")

class GameAuctionAlreadyFinishedException(BizException):
    def __init__(self):
        super().__init__(10010,  "Game auction already finished!")

class GameInvalidBidException(BizException):
    def __init__(self):
        super().__init__(10011, "Game invalid bid!")

class GameNotBidWinner(BizException):
    def __init__(self):
        super().__init__(10012, "Game not bid winner!")

class GameNotReadyForTrickWinnerExcception(BizException):
    def __init__(self):
        super().__init__(10013, "Game not ready for trick winner!")

class GameInvalidTrickStateException(BizException):
    def __init__(self):
        super().__init__(10014, "Game invalid trick state!")

class GameAlreadyFinishedException(BizException):
    def __init__(self):
        super().__init__(10015, "Game already finished!")

class GameNotPlayerTrickTurnException(BizException):
    def __init__(self):
        super().__init__(10016, "Game not player's turn to trick!")

class GameInvalidPlayerTrickException(BizException):
    def __init__(self):
        super().__init__(10017, "Game player tricks with invalid card!")

class PlayerInvalidHandException(BizException):
    def __init__(self):
        super().__init__(10018, "Player invalid hand!")

class BridgeGameAlreadyCreatedException(BizException):
    def __init__(self):
        super().__init__(10019, "Bridge game already created!")

class BridgeGameNotFoundException(BizException):
    def __init__(self):
        super().__init__(10020, "Bridge game not found!")
