from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'welcome_instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class welcome(Page):
    pass


class general_instruction(Page):
    pass


class risky_choice_price_instruction(Page):
    pass


class risky_choice_allocation_instruction(Page):
    pass


class real_effort_decoding_instruction(Page):
    pass


class asian_handicap_instruction(Page):
    pass


class confirmation(Page):
    pass


page_sequence = [
    welcome,
    general_instruction,
    risky_choice_price_instruction,
    risky_choice_allocation_instruction,
    real_effort_decoding_instruction,
    asian_handicap_instruction,
    confirmation
]
