"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



class UnexpectedCondition(Exception):
    """
    Exception when action was not taken due to idempotency.
    """



class Idempotent(Exception):
    """
    Exception when action was not taken due to idempotency.
    """



class MultipleSource(Exception):
    """
    Exception when action was not taken due to idempotency.
    """
