from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'before_experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    initial_endowment = 100
    additional_endowment = 30
    consumption_cost = 50


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Before_Experiment(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.dynamic_endowment = C.initial_endowment
        participant.dynamic_additional_endowment = C.additional_endowment
        participant.dynamic_consumption_cost = C.consumption_cost


page_sequence = [Before_Experiment]
