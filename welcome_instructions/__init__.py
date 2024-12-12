from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'welcome_instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    initial_endowment_practice = 100
    additional_endowment_practice = 30
    consumption_cost_practice = 50


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Instruction1(Page):
    pass


class Instruction2(Page):
    pass


class Confirmation(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.dynamic_endowment_practice = C.initial_endowment_practice
        participant.dynamic_additional_endowment_practice = C.additional_endowment_practice
        participant.dynamic_consumption_cost_practice = C.consumption_cost_practice


page_sequence = [Instruction1, Instruction2, Confirmation]
