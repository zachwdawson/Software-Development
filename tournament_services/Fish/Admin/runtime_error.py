
class FishRuntimeException(Exception):
    """
    This is an exception type that is used to represent all errors that happen during the run-time
    of executing a Fish game that a referee runs. These run-time effects would crash the referee
    if we did not handle them.
    """
    pass


class NotWellFormedReturnValue(FishRuntimeException):
    """
    Subclass of a run-time exception where the Referee asks for a value back from the player
    for a movement or a placement and the player returns back a value that has a type that is not well-formed
    in some way. A well-formed value will be a Coordinate type (defined elsewhere) for a placement and
    an Action type for a movement.
    """
    pass


class PlayerInternalException(FishRuntimeException):
    """
    This is a run-time exception in which a referee asks a player to perform some method and the player
    throws an internal exception when trying to produce that value. We want to remove such failing players.
    This is a wide error, encompassing any error the player throws, since we cannot know all the errors
    a player could throw.
    """
    pass
