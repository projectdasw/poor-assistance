from otree.api import *
import random
import json
from pathlib import Path

doc = """
ASIAN Handicap
"""

class Constants(BaseConstants):
    name_in_url = 'asian_handicap'
    players_per_group = None
    num_rounds = 2
    initial_endowment = 100
    investment_scheme = [
        {"investment_return": 1.15, "probability": 0.9},
        {"investment_return": 1.2, "probability": 0.85},
        {"investment_return": 1.25, "probability": 0.8},
        {"investment_return": 1.35, "probability": 0.75},
        {"investment_return": 1.45, "probability": 0.7},
        {"investment_return": 1.55, "probability": 0.65},
        {"investment_return": 1.67, "probability": 0.6},
        {"investment_return": 1.85, "probability": 0.55},
        {"investment_return": 2.0, "probability": 0.5},
        {"investment_return": 2.25, "probability": 0.45},
        {"investment_return": 2.5, "probability": 0.4},
        {"investment_return": 2.9, "probability": 0.35},
        {"investment_return": 3.4, "probability": 0.3},
        {"investment_return": 4.0, "probability": 0.25},
        {"investment_return": 5.0, "probability": 0.2},
        {"investment_return": 7.0, "probability": 0.15},
        {"investment_return": 10.0, "probability": 0.1},
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.CurrencyField()
    asian_ev_1 = models.FloatField(initial=0)
    result_asian_1 = models.FloatField(initial=0, decimal=1)
    asian_ev_2 = models.FloatField(initial=0)
    result_asian_2 = models.FloatField(initial=0, decimal=1)
    asian_ev_3 = models.FloatField(initial=0)
    result_asian_3 = models.FloatField(initial=0, decimal=1)
    asian_ev_4 = models.FloatField(initial=0)
    result_asian_4 = models.FloatField(initial=0, decimal=1)
    asian_ev_5 = models.FloatField(initial=0)
    result_asian_5 = models.FloatField(initial=0, decimal=1)
    asian_ev_6 = models.FloatField(initial=0)
    result_asian_6 = models.FloatField(initial=0, decimal=1)
    asian_ev_7 = models.FloatField(initial=0)
    result_asian_7 = models.FloatField(initial=0, decimal=1)
    asian_ev_8 = models.FloatField(initial=0)
    result_asian_8 = models.FloatField(initial=0, decimal=1)
    asian_ev_9 = models.FloatField(initial=0)
    result_asian_9 = models.FloatField(initial=0, decimal=1)
    asian_ev_10 = models.FloatField(initial=0)
    result_asian_10 = models.FloatField(initial=0, decimal=1)
    asian_ev_11 = models.FloatField(initial=0)
    result_asian_11 = models.FloatField(initial=0, decimal=1)
    asian_ev_12 = models.FloatField(initial=0)
    result_asian_12 = models.FloatField(initial=0, decimal=1)
    asian_ev_13 = models.FloatField(initial=0)
    result_asian_13 = models.FloatField(initial=0, decimal=1)
    asian_ev_14 = models.FloatField(initial=0)
    result_asian_14 = models.FloatField(initial=0, decimal=1)
    asian_ev_15 = models.FloatField(initial=0)
    result_asian_15 = models.FloatField(initial=0, decimal=1)
    asian_ev_16 = models.FloatField(initial=0)
    result_asian_16 = models.FloatField(initial=0, decimal=1)
    asian_ev_17 = models.FloatField(initial=0)
    result_asian_17 = models.FloatField(initial=0, decimal=1)
    total_return = models.FloatField(initial=0, decimal=1)
    offer_accepted = models.BooleanField(
        choices=[
            (True, 'Iya'),
            (False, 'Tidak')
        ]
    )


class Confirmation(Page):
    form_model = 'player'
    form_fields = ['offer_accepted']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Simpan keputusan pemain di level participant
        player.participant.offer_accepted = player.offer_accepted
        player.endowment = Constants.initial_endowment


class Game(Page):
    form_model = "player"
    form_fields = [
        'asian_ev_1', 'asian_ev_2', 'asian_ev_3', 'asian_ev_4', 'asian_ev_5', 'asian_ev_6', 'asian_ev_7', 'asian_ev_8',
        'asian_ev_9', 'asian_ev_10', 'asian_ev_11', 'asian_ev_12', 'asian_ev_13', 'asian_ev_14', 'asian_ev_15',
        'asian_ev_16', 'asian_ev_17'
    ]

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Ya" di ronde pertama
        return player.participant.offer_accepted is True

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        # Dynamic Endowment
        if player.round_number > 1:
            # Endowment dari periode sebelumnya digunakan kembali pada periode berikutnya
            previous_player = player.in_round(player.round_number - 1)
            participant.get_endowment = previous_player.endowment  # Menampilkan endowment periode sebelumnya
            player.endowment = previous_player.endowment  # Ambil endowment dari periode sebelumnya

        # Menyediakan investment_scheme untuk template
        return {
            'investment_scheme': Constants.investment_scheme,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Random drawing untuk setiap opsi
        for i, investment_scheme in enumerate(Constants.investment_scheme, start=1):
            draw = random.randint(1, 100)  # Angka random 1-100
            probability = investment_scheme["probability"] * 100
            if draw <= probability:
                # Subjek mendapatkan return
                setattr(player, f"result_asian_{i}", investment_scheme["investment_return"])
            else:
                # Subjek tidak mendapatkan return
                setattr(player, f"result_asian_{i}", 0)

        if player.endowment < 0 or player.endowment == 0:
            player.result_asian_1 = 0
            player.result_asian_2 = 0
            player.result_asian_3 = 0
            player.result_asian_4 = 0
            player.result_asian_5 = 0
            player.result_asian_6 = 0
            player.result_asian_7 = 0
            player.result_asian_8 = 0
            player.result_asian_9 = 0
            player.result_asian_10 = 0
            player.result_asian_11 = 0
            player.result_asian_12 = 0
            player.result_asian_13 = 0
            player.result_asian_14 = 0
            player.result_asian_15 = 0
            player.result_asian_16 = 0
            player.result_asian_17 = 0

        player.total_return += (player.result_asian_1 * player.asian_ev_1) + \
                               (player.result_asian_2 * player.asian_ev_2) + \
                               (player.result_asian_3 * player.asian_ev_3) + \
                               (player.result_asian_4 * player.asian_ev_4) + \
                               (player.result_asian_5 * player.asian_ev_5) + \
                               (player.result_asian_6 * player.asian_ev_6) + \
                               (player.result_asian_7 * player.asian_ev_7) + \
                               (player.result_asian_8 * player.asian_ev_8) + \
                               (player.result_asian_9 * player.asian_ev_9) + \
                               (player.result_asian_10 * player.asian_ev_10) + \
                               (player.result_asian_11 * player.asian_ev_11) + \
                               (player.result_asian_12 * player.asian_ev_12) + \
                               (player.result_asian_13 * player.asian_ev_13) + \
                               (player.result_asian_14 * player.asian_ev_14) + \
                               (player.result_asian_15 * player.asian_ev_15) + \
                               (player.result_asian_16 * player.asian_ev_16) + \
                               (player.result_asian_17 * player.asian_ev_17)
        player.endowment += player.total_return

        total_asian = (player.asian_ev_1 + player.asian_ev_2 + player.asian_ev_3 +
                       player.asian_ev_4 + player.asian_ev_5 + player.asian_ev_6 +
                       player.asian_ev_7 + player.asian_ev_8 + player.asian_ev_9 +
                       player.asian_ev_10 + player.asian_ev_11 + player.asian_ev_12 +
                       player.asian_ev_13 + player.asian_ev_14 + player.asian_ev_15 +
                       player.asian_ev_16 + player.asian_ev_17)
        player.endowment -= total_asian

    @staticmethod
    def error_message(player: Player, values):
        # Hitung total investasi
        total_investasi = (values['asian_ev_1'] + values['asian_ev_2'] + values['asian_ev_3'] +
                           values['asian_ev_4'] + values['asian_ev_5'] + values['asian_ev_6'] +
                           values['asian_ev_7'] + values['asian_ev_8'] + values['asian_ev_9'] +
                           values['asian_ev_10'] + values['asian_ev_11'] + values['asian_ev_12'] +
                           values['asian_ev_13'] + values['asian_ev_14'] + values['asian_ev_15'] +
                           values['asian_ev_16'] + values['asian_ev_17'])

        # Periksa apakah total investasi melebihi endowment
        if total_investasi > player.endowment:
            return f"Endowment Anda tidak mencukupi untuk dialokasikan (Total biaya: {total_investasi})."
        return ""


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Kumpulkan data hasil dari setiap opsi investasi
        investment_results = []
        for i, investment_scheme in enumerate(Constants.investment_scheme, start=1):
            ev_field = f"asian_ev_{i}"
            result_field = f"result_asian_{i}"
            ev_value = getattr(player, ev_field)  # Alokasi dana untuk opsi ini
            result_value = getattr(player, result_field)  # Hasil dari opsi ini
            if ev_value > 0:  # Hanya tampilkan opsi yang dialokasikan dana
                investment_results.append({
                    'option_number': i,
                    'allocated': ev_value,
                    'return': result_value,
                })

        total_allocation = sum([inv['allocated'] for inv in investment_results])  # Total alokasi dana
        total_return = sum([inv['allocated'] * inv['return'] for inv in investment_results])  # Total hasil

        return {
            'investment_results': investment_results,
            'total_allocation': total_allocation,
            'total_return': total_return,
        }


class AllResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        # Ambil data semua ronde
        rounds_data = []
        for p in player.in_all_rounds():
            rounds_data.append({
                'round_number': p.round_number,
                'return': p.total_return,
                'cost': sum([
                    p.asian_ev_1, p.asian_ev_2, p.asian_ev_3, p.asian_ev_4, p.asian_ev_5,
                    p.asian_ev_6, p.asian_ev_7, p.asian_ev_8, p.asian_ev_9, p.asian_ev_10,
                    p.asian_ev_11, p.asian_ev_12, p.asian_ev_13, p.asian_ev_14, p.asian_ev_15,
                    p.asian_ev_16, p.asian_ev_17
                ]),
                'payoff': p.payoff,
            })

        # Hitung hasil akhir
        final_return = abs(sum([p.total_return for p in player.in_all_rounds()]))
        final_cost = abs(sum([p.total_return - p.endowment for p in player.in_all_rounds()]))
        final_payoff = sum([p.payoff for p in player.in_all_rounds()])

        return {
            'rounds_data': rounds_data,
            'final_return': final_return,
            'final_cost': final_cost,
            'final_payoff': final_payoff
        }


page_sequence = [Confirmation, Game, Results, AllResults]
