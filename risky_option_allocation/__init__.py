from otree.api import *
import random
import json
from pathlib import Path

doc = """
Poor Assistance Experiment
"""

class Constants(BaseConstants):
    name_in_url = 'risky_option_allocation'
    players_per_group = None
    num_rounds = 10
    initial_endowment = 100
    options_data_allocation = [
        {'name': 'Opsi 1', 'outcomes': [(1.5, 0.65), (0.25, 0.1), (0, 0.25)]},
        {'name': 'Opsi 2', 'outcomes': [(1.5, 0.6), (0.5, 0.2), (0, 0.2)]},
        {'name': 'Opsi 3', 'outcomes': [(1.5, 0.55), (0.75, 0.25), (0, 0.3)]},
        {'name': 'Opsi 4', 'outcomes': [(1.5, 0.4), (1, 0.4), (0, 0.2)]},
        {'name': 'Opsi 5', 'outcomes': [(1.5, 0.5), (1.25, 0.2), (0, 0.3)]},
        {'name': 'Opsi 6', 'outcomes': [(2, 0.4), (0.5, 0.4), (0, 0.2)]},
        {'name': 'Opsi 7', 'outcomes': [(2, 0.35), (0.75, 0.4), (0, 0.25)]},
        {'name': 'Opsi 8', 'outcomes': [(2, 0.45), (0.25, 0.4), (0, 0.05)]},
        {'name': 'Opsi 9', 'outcomes': [(2, 0.4), (1, 0.2), (0, 0.4)]},
        {'name': 'Opsi 10', 'outcomes': [(2, 0.35), (1.5, 0.2), (0, 0.45)]},
        {'name': 'Opsi 11', 'outcomes': [(2.5, 0.35), (0.25, 0.5), (0, 0.15)]},
        {'name': 'Opsi 12', 'outcomes': [(2.5, 0.3), (0.5, 0.5), (0, 0.2)]},
        {'name': 'Opsi 13', 'outcomes': [(2.5, 0.3), (0.75, 0.35), (0, 0.35)]},
        {'name': 'Opsi 14', 'outcomes': [(2.5, 0.2), (1, 0.5), (0, 0.3)]},
        {'name': 'Opsi 15', 'outcomes': [(2.5, 0.1), (1.25, 0.6), (0, 0.3)]},
        {'name': 'Opsi 16', 'outcomes': [(3, 0.3), (0.5, 0.2), (0, 0.5)]},
        {'name': 'Opsi 17', 'outcomes': [(3, 0.3), (0.25, 0.4), (0, 0.3)]},
        {'name': 'Opsi 18', 'outcomes': [(3, 0.2), (1, 0.4), (0, 0.4)]},
        {'name': 'Opsi 19', 'outcomes': [(3, 0.25), (1.25, 0.25), (0, 0.55)]},
        {'name': 'Opsi 20', 'outcomes': [(3, 0.15), (0.75, 0.75), (0, 0.1)]},
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.CurrencyField()
    selected_optionallocation1 = models.StringField(blank=True, initial="")
    allocation_invest1 = models.FloatField(initial=0)
    result_allocation1 = models.FloatField(initial=0, decimal=1)
    selected_optionallocation2 = models.StringField(blank=True, initial="")
    allocation_invest2 = models.FloatField(initial=0)
    result_allocation2 = models.FloatField(initial=0, decimal=1)
    selected_optionallocation3 = models.StringField(blank=True, initial="")
    allocation_invest3 = models.FloatField(initial=0)
    result_allocation3 = models.FloatField(initial=0, decimal=1)
    selected_optionallocation4 = models.StringField(blank=True, initial="")
    allocation_invest4 = models.FloatField(initial=0)
    result_allocation4 = models.FloatField(initial=0, decimal=1)
    selected_optionallocation5 = models.StringField(blank=True, initial="")
    allocation_invest5 = models.FloatField(initial=0)
    result_allocation5 = models.FloatField(initial=0, decimal=1)
    total_profit = models.FloatField(initial=0)
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
    form_model = 'player'
    form_fields = ['selected_optionallocation1', 'allocation_invest1', 'selected_optionallocation2',
                   'allocation_invest2', 'selected_optionallocation2', 'selected_optionallocation3',
                   'allocation_invest3', 'selected_optionallocation4', 'allocation_invest4',
                   'selected_optionallocation5', 'allocation_invest5', 'subject_action']

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

        # Mendapatkan pilihan acak (contoh daftar pilihan opsi)
        random_options1 = random.sample(Constants.options_data_allocation, 1)
        random_options2 = random.sample(Constants.options_data_allocation, 1)
        random_options3 = random.sample(Constants.options_data_allocation, 1)
        random_options4 = random.sample(Constants.options_data_allocation, 1)
        random_options5 = random.sample(Constants.options_data_allocation, 1)

        # Membuat teks yang terstruktur untuk setiap opsi dalam format list items
        for i, option1 in enumerate(random_options1):
            option_outcomes = option1['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option1['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option2 in enumerate(random_options2):
            option_outcomes = option2['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option2['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option3 in enumerate(random_options3):
            option_outcomes = option3['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option3['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option4 in enumerate(random_options4):
            option_outcomes = option4['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option4['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option5 in enumerate(random_options5):
            option_outcomes = option5['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option5['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        return {
            'random_options1': random_options1,
            'random_options2': random_options2,
            'random_options3': random_options3,
            'random_options4': random_options4,
            'random_options5': random_options5,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Jika endowment sama dengan 0, langsung akhiri permainan
        if player.subject_action == 'endowment_limit':
            player.participant.vars['end_game'] = True
            # Tetapkan ronde terakhir bermain
            player.participant.vars['last_round_played'] = player.round_number
            player.payoff = player.endowment
        elif player.subject_action == 'skip':
            # Jika tombol "Lewati" dipilih, set hasil kosong dan lanjut ke Results
            player.selected_optionallocation1 = ""
            player.result_allocation1 = 0
            player.selected_optionallocation2 = ""
            player.result_allocation2 = 0
            player.selected_optionallocation3 = ""
            player.result_allocation3 = 0
            player.selected_optionallocation4 = ""
            player.result_allocation4 = 0
            player.selected_optionallocation5 = ""
            player.result_allocation5 = 0
        elif player.subject_action == 'invested':
            # Temukan opsi yang dipilih pemain berdasarkan nama
            selected_option1 = next(
                (option1 for option1 in Constants.options_data_allocation if
                 option1['name'] == player.selected_optionallocation1), None
            )
            selected_option2 = next(
                (option2 for option2 in Constants.options_data_allocation if
                 option2['name'] == player.selected_optionallocation2), None
            )
            selected_option3 = next(
                (option3 for option3 in Constants.options_data_allocation if
                 option3['name'] == player.selected_optionallocation3), None
            )
            selected_option4 = next(
                (option4 for option4 in Constants.options_data_allocation if
                 option4['name'] == player.selected_optionallocation4), None
            )
            selected_option5 = next(
                (option5 for option5 in Constants.options_data_allocation if
                 option5['name'] == player.selected_optionallocation5), None
            )

            # Lakukan drawing angka 1-100
            if selected_option1:
                draw = random.randint(1, 100)

                # Hitung hasil berdasarkan peluang
                cumulative_probability = 0
                for outcome, probability in selected_option1['outcomes']:
                    cumulative_probability += probability * 100
                    if draw <= cumulative_probability:
                        player.result_allocation1 = outcome
                        player.endowment -= player.allocation_invest1
                        break

            if selected_option2:
                draw = random.randint(1, 100)

                # Hitung hasil berdasarkan peluang
                cumulative_probability = 0
                for outcome, probability in selected_option2['outcomes']:
                    cumulative_probability += probability * 100
                    if draw <= cumulative_probability:
                        player.result_allocation2 = outcome
                        player.endowment -= player.allocation_invest2
                        break

            if selected_option3:
                draw = random.randint(1, 100)

                # Hitung hasil berdasarkan peluang
                cumulative_probability = 0
                for outcome, probability in selected_option3['outcomes']:
                    cumulative_probability += probability * 100
                    if draw <= cumulative_probability:
                        player.result_allocation3 = outcome
                        player.endowment -= player.allocation_invest3
                        break

            if selected_option4:
                draw = random.randint(1, 100)

                # Hitung hasil berdasarkan peluang
                cumulative_probability = 0
                for outcome, probability in selected_option4['outcomes']:
                    cumulative_probability += probability * 100
                    if draw <= cumulative_probability:
                        player.result_allocation4 = outcome
                        player.endowment -= player.allocation_invest4
                        break

            if selected_option5:
                draw = random.randint(1, 100)

                # Hitung hasil berdasarkan peluang
                cumulative_probability = 0
                for outcome, probability in selected_option5['outcomes']:
                    cumulative_probability += probability * 100
                    if draw <= cumulative_probability:
                        player.result_allocation5 = outcome
                        player.endowment -= player.allocation_invest5
                        break

    @staticmethod
    def error_message(player: Player, values):
        total_allocation = (values['allocation_invest1'] + values['allocation_invest2'] + values['allocation_invest3'] +
                            values['allocation_invest4'] + values['allocation_invest5'])

        error_msgs = []
        if values['subject_action'] == 'invested':
            if total_allocation > player.endowment:
                error_msgs.append(
                    f"Endowment Anda tidak mencukupi untuk membeli opsi-opsi tersebut" \
                    f" (Total alokasi: {total_allocation})."
                )
            elif total_allocation == 0:
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
        # Tampilkan hanya jika permainan belum diakhiri
        return not player.participant.vars.get('end_game', False)

    @staticmethod
    def vars_for_template(player: Player):
        total_profit = (player.allocation_invest1 * player.result_allocation1) + \
                       (player.allocation_invest2 * player.result_allocation2) + \
                       (player.allocation_invest3 * player.result_allocation3) + \
                       (player.allocation_invest4 * player.result_allocation4) + \
                       (player.allocation_invest5 * player.result_allocation5)
        sum_profit = player.endowment + total_profit

        return {
            'allocation1': player.allocation_invest1,
            'result1': player.result_allocation1,
            'profit1': player.allocation_invest1 * player.result_allocation1,
            'allocation2': player.allocation_invest2,
            'result2': player.result_allocation2,
            'profit2': player.allocation_invest2 * player.result_allocation2,
            'allocation3': player.allocation_invest3,
            'result3': player.result_allocation3,
            'profit3': player.allocation_invest3 * player.result_allocation3,
            'allocation4': player.allocation_invest4,
            'result4': player.result_allocation4,
            'profit4': player.allocation_invest4 * player.result_allocation4,
            'allocation5': player.allocation_invest5,
            'result5': player.result_allocation5,
            'profit5': player.allocation_invest5 * player.result_allocation5,
            'sum_profit': sum_profit
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        total_profit = (player.allocation_invest1 * player.result_allocation1) +\
                       (player.allocation_invest2 * player.result_allocation2) +\
                       (player.allocation_invest3 * player.result_allocation3) +\
                       (player.allocation_invest4 * player.result_allocation4) +\
                       (player.allocation_invest5 * player.result_allocation5)
        player.endowment += total_profit
        player.total_profit = total_profit
        player.payoff = player.endowment

        # Hitung total cost berdasarkan selected_optionprice
        total_cost = sum([
            player.allocation_invest1,
            player.allocation_invest2,
            player.allocation_invest3,
            player.allocation_invest4,
            player.allocation_invest5
        ])

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


page_sequence = [Welcome, Confirmation, CheckInterest, Game, Results, AllResults]
