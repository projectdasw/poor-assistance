from otree.api import *
import random


doc = """
Payment Page
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment_page'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class info_sesi(Page):
    @staticmethod
    def vars_for_template(player):
        participant = player.participant

        return dict(
            risky_purchase=participant.vars.get("results_risky_purchase", []),
            risky_allocation=participant.vars.get("results_risky_allocation", []),
            cognitive_task=participant.vars.get("results_cognitive_task", []),
        )


class pembayaran(Page):
    pass


class akhir_eksperimen(Page):
    pass


page_sequence = [info_sesi]
