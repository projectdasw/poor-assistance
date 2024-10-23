from otree.api import *
import random


doc = """
Select a random round for payment
"""


class C(BaseConstants):
    NAME_IN_URL = 'pay_random'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
    # round = models.IntegerField()
    # potential_payoff = models.FloatField(min=0, max=1, initial=0)


# PAGES
class Pay_info(Page):
    pass
    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     participant = player.participant
    #     player.potential_payoff = float(participant.ct_payment)
    #     player.round = int(participant.selected_round)


class Payment(Page):
    pass
    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     player.payoff = (player.potential_payoff * 50) + 10000


class End(Page):
    pass


page_sequence = [Pay_info, Payment, End]
