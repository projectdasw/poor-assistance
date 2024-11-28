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
    num_rounds = 20
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
    endowment = models.CurrencyField(initial=0)
    asian_ev_1 = models.FloatField(initial=0)
    result_asian_1 = models.FloatField(initial=0)
    asian_ev_2 = models.FloatField(initial=0)
    result_asian_2 = models.FloatField(initial=0)
    asian_ev_3 = models.FloatField(initial=0)
    result_asian_3 = models.FloatField(initial=0)
    asian_ev_4 = models.FloatField(initial=0)
    result_asian_4 = models.FloatField(initial=0)
    asian_ev_5 = models.FloatField(initial=0)
    result_asian_5 = models.FloatField(initial=0)
    asian_ev_6 = models.FloatField(initial=0)
    result_asian_6 = models.FloatField(initial=0)
    asian_ev_7 = models.FloatField(initial=0)
    result_asian_7 = models.FloatField(initial=0)
    asian_ev_8 = models.FloatField(initial=0)
    result_asian_8 = models.FloatField(initial=0)
    asian_ev_9 = models.FloatField(initial=0)
    result_asian_9 = models.FloatField(initial=0)
    asian_ev_10 = models.FloatField(initial=0)
    result_asian_10 = models.FloatField(initial=0)
    asian_ev_11 = models.FloatField(initial=0)
    result_asian_11 = models.FloatField(initial=0)
    asian_ev_12 = models.FloatField(initial=0)
    result_asian_12 = models.FloatField(initial=0)
    asian_ev_13 = models.FloatField(initial=0)
    result_asian_13 = models.FloatField(initial=0)
    asian_ev_14 = models.FloatField(initial=0)
    result_asian_14 = models.FloatField(initial=0)
    asian_ev_15 = models.FloatField(initial=0)
    result_asian_15 = models.FloatField(initial=0)
    asian_ev_16 = models.FloatField(initial=0)
    result_asian_16 = models.FloatField(initial=0)
    asian_ev_17 = models.FloatField(initial=0)
    result_asian_17 = models.FloatField(initial=0)
    total_return = models.FloatField(initial=0)
    offer_accepted = models.BooleanField(choices=[(True), (False)], initial=None)
    subject_action = models.StringField(
        choices=['skip', 'invested', 'endowment_limit'], initial="", blank=True
    )  # Untuk mencatat tombol yang dipilih

    still_interested = models.StringField(
        choices=['yes', 'no'], initial="", blank=True
    )  # Untuk mencatat tombol yang dipilih


class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


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

        if player.participant.offer_accepted:
            # Jika pemain memilih 'Yes', lanjutkan ke Game
            pass
        else:
            # Jika pemain memilih 'No', tandai end_game dan arahkan ke AllResults
            player.participant.vars['end_game'] = True
            # Tetapkan ronde terakhir bermain
            player.participant.vars['last_round_played'] = player.round_number
            player.payoff = player.endowment


class CheckInterest(Page):
    form_model = 'player'
    form_fields = ['still_interested']

    @staticmethod
    def is_displayed(player: Player):
        # Hitung total skip akumulatif
        skips = sum(1 for p in player.in_all_rounds() if p.subject_action == 'skip')

        # Ambil checkpoint konfirmasi terakhir dari participant vars
        last_check = player.participant.vars.get('last_skip_checkpoint', 0)

        # Tampilkan halaman jika skips mencapai kelipatan 5 sejak checkpoint terakhir
        return (
            # Atur Checkpoint
            skips >= last_check + 5
            and not player.participant.vars.get('end_game', False)
        )

    @staticmethod
    def vars_for_template(player: Player):
        # Hitung total skip akumulatif
        skips = sum(1 for p in player.in_all_rounds() if p.subject_action == 'skip')

        return {
            'skips': skips
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.still_interested == "no":
            player.participant.vars['end_game'] = True
            # Tetapkan ronde terakhir bermain
            player.participant.vars['last_round_played'] = player.round_number
            # Simpan endowment terakhir
            previous_round_endowment = player.in_round(
                player.round_number - 1).endowment if player.round_number > 1 else Constants.initial_endowment
            player.endowment = previous_round_endowment
            player.payoff = player.endowment
        else:
            player.still_interested == "yes"
            # Simpan endowment terakhir
            previous_round_endowment = player.in_round(
                player.round_number - 1).endowment if player.round_number > 1 else Constants.initial_endowment
            player.endowment = previous_round_endowment
            # Update checkpoint ke jumlah skips saat ini
            skips = sum(1 for p in player.in_all_rounds() if p.subject_action == 'skip')
            player.participant.vars['last_skip_checkpoint'] = skips


class Game(Page):
    form_model = "player"
    form_fields = [
        'asian_ev_1', 'asian_ev_2', 'asian_ev_3', 'asian_ev_4', 'asian_ev_5', 'asian_ev_6', 'asian_ev_7', 'asian_ev_8',
        'asian_ev_9', 'asian_ev_10', 'asian_ev_11', 'asian_ev_12', 'asian_ev_13', 'asian_ev_14', 'asian_ev_15',
        'asian_ev_16', 'asian_ev_17', 'subject_action'
    ]

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Ya" di ronde pertama
        return not player.participant.vars.get('end_game', False)

    @staticmethod
    def vars_for_template(player: Player):
        # Simpan endowment terakhir
        previous_round_endowment = player.in_round(
            player.round_number - 1).endowment if player.round_number > 1 else Constants.initial_endowment
        player.endowment = previous_round_endowment

        # Menyediakan investment_scheme untuk template
        return {
            'investment_scheme': Constants.investment_scheme,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.subject_action == 'endowment_limit':
            player.participant.vars['end_game'] = True
            # Tetapkan ronde terakhir bermain
            player.participant.vars['last_round_played'] = player.round_number
            player.payoff = player.endowment
        elif player.subject_action == 'skip':
            player.result_asian_1 = 0
            player.asian_ev_1 = 0
            player.result_asian_2 = 0
            player.asian_ev_2 = 0
            player.result_asian_3 = 0
            player.asian_ev_3 = 0
            player.result_asian_4 = 0
            player.asian_ev_4 = 0
            player.result_asian_5 = 0
            player.asian_ev_5 = 0
            player.result_asian_6 = 0
            player.asian_ev_6 = 0
            player.result_asian_7 = 0
            player.asian_ev_7 = 0
            player.result_asian_8 = 0
            player.asian_ev_8 = 0
            player.result_asian_9 = 0
            player.asian_ev_9 = 0
            player.result_asian_10 = 0
            player.asian_ev_10 = 0
            player.result_asian_11 = 0
            player.asian_ev_11 = 0
            player.result_asian_12 = 0
            player.asian_ev_12 = 0
            player.result_asian_13 = 0
            player.asian_ev_13 = 0
            player.result_asian_14 = 0
            player.asian_ev_14 = 0
            player.result_asian_15 = 0
            player.asian_ev_15 = 0
            player.result_asian_16 = 0
            player.asian_ev_16 = 0
            player.result_asian_17 = 0
            player.asian_ev_17 = 0
        elif player.subject_action == 'invested':
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

            player.endowment = player.endowment - sum([
                player.asian_ev_1, player.asian_ev_2, player.asian_ev_3, player.asian_ev_4, player.asian_ev_5,
                player.asian_ev_6, player.asian_ev_7, player.asian_ev_8, player.asian_ev_9, player.asian_ev_10,
                player.asian_ev_11, player.asian_ev_12, player.asian_ev_13, player.asian_ev_14,
                player.asian_ev_15, player.asian_ev_16, player.asian_ev_17
            ])


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
        error_msgs = []
        if values['subject_action'] == 'invested':
            if total_investasi > player.endowment:
                error_msgs.append(
                    f"Endowment Anda tidak mencukupi untuk membeli opsi-opsi tersebut" \
                    f" (Total alokasi: {total_investasi})."
                )
            elif total_investasi == 0:
                error_msgs.append(
                    f"Anda tidak mengalokasikan apapun pada setiap opsi-opsi yang tersedia"
                )

        # Jika ada pesan kesalahan, gabungkan dan kembalikan
        if error_msgs:
            return "<br>".join(error_msgs)
        return ""


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Ya" di ronde pertama
        return not player.participant.vars.get('end_game', False)

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
        total_return = round(sum([inv['allocated'] * inv['return'] for inv in investment_results]), 5)  # Total hasil
        player.total_return = total_return

        return {
            'investment_results': investment_results,
            'total_allocation': total_allocation,
            'total_return': total_return,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
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
        total_return = round(sum([inv['allocated'] * inv['return'] for inv in investment_results]), 5)  # Total hasil

        player.endowment += total_return
        player.payoff = player.endowment


class AllResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        # Ambil ronde terakhir bermain
        last_round = player.participant.vars.get('last_round_played', player.round_number)

        # Ambil data semua ronde
        rounds_data = []
        for p in player.in_rounds(1, last_round):
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
        final_return = sum([p.total_return for p in player.in_rounds(1, last_round)])
        final_cost = sum([
            (p.total_return) - (p.endowment)  # Tangani nilai None
            for p in player.in_rounds(1, last_round)
        ])
        final_payoff = sum([p.payoff for p in player.in_rounds(1, last_round)])
        final_endowment = (player.in_round(last_round).endowment)

        return {
            'last_round': last_round,
            'final_endowment': final_endowment,
            'rounds_data': rounds_data,
            'final_return': final_return,
            'final_cost': final_cost,
            'final_payoff': final_payoff
        }


page_sequence = [Welcome, Confirmation, CheckInterest, Game, Results, AllResults]
