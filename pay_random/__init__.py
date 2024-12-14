from otree.api import *
import random


doc = """
Pay Random
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
    name_apps = models.StringField()
    payoff_apps = models.FloatField(initial=0)


# PAGES
class Pay_info(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        # Hitung total payoff dari setiap aplikasi
        participant = player.participant
        app_results = {
            'Investment Game 1': participant.app_investment1,
            'Investment Game 2': participant.app_investment2,
            'Investment Game 3': participant.app_investment3,
            'Investment Game 4': participant.app_investment4,
        }

        # Simpan hasil ke participant.vars untuk digunakan di halaman kedua
        participant.vars['pay_random_data'] = app_results

        return {
            'app_results': app_results
        }


class Payment(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        # Ambil data dari halaman sebelumnya
        pay_random_data = participant.vars.get('pay_random_data', {})

        # Lakukan pengacakan aplikasi
        selected_app = random.choice(list(pay_random_data.keys()))
        selected_payoff = pay_random_data[selected_app]
        player.name_apps = selected_app
        player.payoff_apps = selected_payoff
        player.payoff = (selected_payoff * 100) + 10000

        # Simpan hasil ke participant.vars untuk digunakan lebih lanjut
        participant.vars['pay_random_result'] = {
            'selected_app': selected_app,
            'selected_payoff': selected_payoff
        }

        return {
            'selected_app': selected_app,
            'selected_payoff': selected_payoff,
            'final_pay': (selected_payoff * 100) + 10000
        }


class End(Page):
    pass


page_sequence = [Pay_info, Payment, End]
