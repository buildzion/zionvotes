
METHOD_WINNER_TAKES_ALL = "winner_takes_all"
METHOD_IRV = "irv"
METHOD_CSSD = "cssd"
METHOD_CHOICES = (
    (METHOD_WINNER_TAKES_ALL, "Winner takes all"),
    (METHOD_IRV, "Instant Runoff"),
    (METHOD_CSSD, "Cloneproof Schwartz Sequential Dropping"),
)


BALLOT_NEW = "new"
BALLOT_CAST = "cast"
BALLOT_ABANDONED = "abandoned"
BALLOT_CHOICES = (
    (BALLOT_NEW, "New"),
    (BALLOT_CAST, "Cast"),
    (BALLOT_ABANDONED, "Abandoned"),
)
