from otree.api import *
import random
import json
from pathlib import Path

doc = """
Risky Option Price
"""

class Constants(BaseConstants):
    name_in_url = 'risky_option_price'
    players_per_group = None
    num_rounds = 10
    initial_endowment = 100
    options_data_price = [
        {'name': 'Opsi 1', 'outcomes': [(45, 0.5), (10, 0.25), (0, 0.25)]},
        {'name': 'Opsi 2', 'outcomes': [(45, 0.4), (20, 0.35), (0, 0.25)]},
        {'name': 'Opsi 3', 'outcomes': [(45, 0.4), (15, 0.4), (5, 0.2)]},
        {'name': 'Opsi 4', 'outcomes': [(45, 0.35), (15, 0.55), (10, 0.1)]},
        {'name': 'Opsi 5', 'outcomes': [(45, 0.45), (10, 0.40), (5, 0.15)]},
        {'name': 'Opsi 6', 'outcomes': [(40, 0.5), (10, 0.5), (0, 0)]},
        {'name': 'Opsi 7', 'outcomes': [(40, 0.4), (20, 0.4), (5, 0.2)]},
        {'name': 'Opsi 8', 'outcomes': [(40, 0.6), (5, 0.2), (0, 0.2)]},
        {'name': 'Opsi 9', 'outcomes': [(40, 0.45), (20, 0.35), (0, 0.2)]},
        {'name': 'Opsi 10', 'outcomes': [(40, 0.5), (15, 0.25), (5, 0.25)]},
        {'name': 'Opsi 11', 'outcomes': [(35, 0.4), (20, 0.4), (15, 0.2)]},
        {'name': 'Opsi 12', 'outcomes': [(35, 0.5), (25, 0.25), (5, 0.25)]},
        {'name': 'Opsi 13', 'outcomes': [(35, 0.6), (15, 0.2), (5, 0.5)]},
        {'name': 'Opsi 14', 'outcomes': [(35, 0.25), (25, 0.65), (0, 0.1)]},
        {'name': 'Opsi 15', 'outcomes': [(35, 0.5), (20, 0.25), (10, 0.25)]},
        {'name': 'Opsi 16', 'outcomes': [(30, 0.7), (20, 0.2), (0, 0.1)]},
        {'name': 'Opsi 17', 'outcomes': [(30, 0.5), (25, 0.4), (0, 0.1)]},
        {'name': 'Opsi 18', 'outcomes': [(30, 0.6), (20, 0.3), (10, 0.1)]},
        {'name': 'Opsi 19', 'outcomes': [(30, 0.7), (15, 0.25), (5, 0.05)]},
        {'name': 'Opsi 20', 'outcomes': [(30, 0.6), (25, 0.25), (5, 0.15)]},
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.CurrencyField(initial=0)
    selected_optionprice1 = models.StringField(blank=True, initial="")
    result_price1 = models.FloatField(initial=0)
    selected_optionprice2 = models.StringField(blank=True, initial="")
    result_price2 = models.FloatField(initial=0)
    selected_optionprice3 = models.StringField(blank=True, initial="")
    result_price3 = models.FloatField(initial=0)
    selected_optionprice4 = models.StringField(blank=True, initial="")
    result_price4 = models.FloatField(initial=0)
    selected_optionprice5 = models.StringField(blank=True, initial="")
    result_price5 = models.FloatField(initial=0)
    total_profit = models.FloatField(initial=0)
    offer_accepted = models.BooleanField(choices=[(True), (False)], initial=None)
    subject_action = models.StringField(
        choices=['skip', 'invested', 'endowment_limit'], initial="", blank=True
    ) # Untuk mencatat tombol yang dipilih

    still_interested = models.StringField(
        choices=['yes', 'no'], initial="", blank=True
    ) # Untuk mencatat tombol yang dipilih


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
    form_model = 'player'
    form_fields = ['selected_optionprice1', 'selected_optionprice2', 'selected_optionprice3',
                   'selected_optionprice4', 'selected_optionprice5', 'subject_action']

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman jika pemain masih tertarik
        return not player.participant.vars.get('end_game', False)

    @staticmethod
    def vars_for_template(player: Player):
        # Simpan endowment terakhir
        previous_round_endowment = player.in_round(
            player.round_number - 1).endowment if player.round_number > 1 else Constants.initial_endowment
        player.endowment = previous_round_endowment

        # Mendapatkan 5 pilihan acak unik dari daftar opsi
        random_options = random.sample(Constants.options_data_price, 5)

        # Membuat teks yang terstruktur untuk setiap opsi
        for option in random_options:
            option_outcomes = option['outcomes']
            formatted_outcomes = [
                f"Anda mendapatkan {value} dengan peluang {int(probability * 100)}%"
                for value, probability in option_outcomes
            ]
            option['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        return {
            'random_options': random_options,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.subject_action == 'endowment_limit':
            player.participant.vars['end_game'] = True
            # Tetapkan ronde terakhir bermain
            player.participant.vars['last_round_played'] = player.round_number
            player.payoff = player.endowment
        elif player.subject_action == 'skip':
            # Jika tombol "Lewati" dipilih, set hasil kosong dan lanjut ke Results
            player.result_price1 = 0
            player.result_price2 = 0
            player.result_price3 = 0
            player.result_price4 = 0
            player.result_price5 = 0
        elif player.subject_action == 'invested':
            # Daftar pilihan opsi
            selected_options = [
                (player.selected_optionprice1, 'result_price1'),
                (player.selected_optionprice2, 'result_price2'),
                (player.selected_optionprice3, 'result_price3'),
                (player.selected_optionprice4, 'result_price4'),
                (player.selected_optionprice5, 'result_price5'),
            ]

            # Proses setiap pilihan
            for selected_option_name, result_field in selected_options:
                selected_option = next(
                    (option for option in Constants.options_data_price if option['name'] == selected_option_name),
                    None
                )

                if selected_option:
                    draw = random.randint(1, 100)  # Lakukan drawing angka 1-100
                    cumulative_probability = 0

                    # Hitung hasil berdasarkan peluang
                    for outcome, probability in selected_option['outcomes']:
                        cumulative_probability += probability * 100
                        if draw <= cumulative_probability:
                            setattr(player, result_field, outcome)  # Set hasil ke field yang sesuai
                            player.endowment -= 25  # Kurangi endowment
                            break

    @staticmethod
    def error_message(player: Player, values):
        selected_options = [
            values['selected_optionprice1'],
            values['selected_optionprice2'],
            values['selected_optionprice3'],
            values['selected_optionprice4'],
            values['selected_optionprice5']
        ]
        selected_count = sum(1 for option in selected_options if option)
        total_cost = selected_count * 25

        # Pesan kesalahan untuk biaya lebih besar dari endowment
        error_msgs = []
        if player.endowment >= 25:
            if total_cost > player.endowment:
                error_msgs.append(
                    f"Endowment Anda tidak mencukupi untuk membeli {selected_count} opsi (Total biaya: {total_cost})."
                )

            # Pesan kesalahan jika tidak ada opsi yang dipilih
            if values['subject_action'] == 'invested':
                if not any(selected_options):
                    error_msgs.append('Anda harus memilih setidaknya satu opsi.')

            # Jika ada pesan kesalahan, gabungkan dan kembalikan
            if error_msgs:
                return "<br>".join(error_msgs)
            return ""


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        # Tampilkan hanya jika permainan belum diakhiri
        return not player.participant.vars.get('end_game', False)

    @staticmethod
    def vars_for_template(player: Player):
        total_profit = player.result_price1 + player.result_price2 + \
                       player.result_price3 + player.result_price4 + \
                       player.result_price5
        sum_profit = player.endowment + total_profit

        return {
            'result1': player.result_price1,
            'result2': player.result_price2,
            'result3': player.result_price3,
            'result4': player.result_price4,
            'result5': player.result_price5,
            'sum_profit': sum_profit
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        total_profit = player.result_price1 + player.result_price2 +\
                       player.result_price3 + player.result_price4 +\
                       player.result_price5
        player.endowment += total_profit
        player.total_profit = total_profit
        player.payoff = player.endowment

        # Hitung total cost berdasarkan opsi yang dipilih
        selected_options = [
            player.selected_optionprice1,
            player.selected_optionprice2,
            player.selected_optionprice3,
            player.selected_optionprice4,
            player.selected_optionprice5
        ]

        # Filter opsi yang valid (tidak kosong) dan hitung biaya
        cost_per_option = 25
        total_cost = len([option for option in selected_options if option]) * cost_per_option

        # Tambahkan payoff dan cost ke list di participant.vars
        if 'results_by_round' not in player.participant.vars:
            player.participant.vars['results_by_round'] = []

        player.participant.vars['results_by_round'].append({
            'round_number': player.round_number,
            'payoff': player.total_profit,
            'cost': total_cost
        })


class AllResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        # Ambil daftar hasil dari participant.vars
        results_by_round = player.participant.vars.get('results_by_round', [])

        # Ambil ronde terakhir bermain
        last_round = player.participant.vars.get('last_round_played', player.round_number)
        final_endowment = player.in_round(last_round).endowment

        # Hitung total payoff dan total cost
        total_payoff = sum(item['payoff'] for item in results_by_round)
        total_cost = sum(item['cost'] for item in results_by_round)

        return {
            'results_by_round': results_by_round,
            'total_payoff': total_payoff,
            'total_cost': total_cost,
            'last_round': last_round,
            'final_endowment': final_endowment
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.dynamic_endowment = player.endowment


page_sequence = [Welcome, Confirmation, CheckInterest, Game, Results, AllResults]
