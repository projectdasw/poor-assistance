from otree.api import *
import random

doc = """
Risky Investment Purchase
"""


class Constants(BaseConstants):
    name_in_url = 'risky_investment_purchase'
    players_per_group = None
    num_rounds = 3
    endowment = cu(100)
    additional = cu(30)
    consumption = cu(50)
    cost_per_option = cu(25)
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
        {'name': 'Opsi 21', 'outcomes': [(50, 0.5), (0, 0.25), (0, 0.25)]},
        {'name': 'Opsi 22', 'outcomes': [(50, 0.4), (10, 0.35), (6, 0.25)]},
        {'name': 'Opsi 23', 'outcomes': [(50, 0.4), (11, 0.4), (3, 0.2)]},
        {'name': 'Opsi 24', 'outcomes': [(50, 0.35), (12, 0.55), (9, 0.1)]},
        {'name': 'Opsi 25', 'outcomes': [(50, 0.45), (4, 0.4), (6, 0.15)]},
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    uang_sesudah_tambah_bansos = models.CurrencyField(initial=0)
    uang_sebelum_tambah_bansos = models.CurrencyField(initial=0)
    bantuan_sosial = models.CurrencyField(initial=0)
    beban_konsumsi = models.CurrencyField(initial=0)
    total_profit = models.CurrencyField(initial=0)
    total_biaya_beli_opsi = models.CurrencyField(initial=0)
    opsi_1 = models.StringField(blank=True, initial="")
    hasil_opsi_1 = models.FloatField(initial=0)
    opsi_2 = models.StringField(blank=True, initial="")
    hasil_opsi_2 = models.FloatField(initial=0)
    opsi_3 = models.StringField(blank=True, initial="")
    hasil_opsi_3 = models.FloatField(initial=0)
    opsi_4 = models.StringField(blank=True, initial="")
    hasil_opsi_4 = models.FloatField(initial=0)
    opsi_5 = models.StringField(blank=True, initial="")
    hasil_opsi_5 = models.FloatField(initial=0)


class endowment_information(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        player.uang_sebelum_tambah_bansos = Constants.endowment
        player.bantuan_sosial = Constants.additional
        player.beban_konsumsi = Constants.consumption

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.uang_sesudah_tambah_bansos = player.uang_sebelum_tambah_bansos + player.bantuan_sosial


class game(Page):
    form_model = 'player'
    form_fields = ['opsi_1', 'opsi_2', 'opsi_3',
                   'opsi_4', 'opsi_5']

    @staticmethod
    def error_message(player, values):

        # Hitung jumlah opsi yang dipilih
        selected_count = sum(
            1 for i in range(1, 6)
            if values[f'opsi_{i}']
        )

        total_cost = selected_count * Constants.cost_per_option

        if total_cost > player.uang_sesudah_tambah_bansos:
            return (
                f"Total biaya pembelian adalah {total_cost}, "
                f"sedangkan uang yang Anda miliki hanya "
                f"{player.uang_sesudah_tambah_bansos}."
            )

    @staticmethod
    def vars_for_template(player: Player):
        # Key berdasarkan ronde
        key = f'random_options_round_{player.round_number}'

        # Acak hanya sekali untuk ronde ini
        if key not in player.participant.vars:
            random_options = random.sample(Constants.options_data_price, 5)
            for option in random_options:
                option['formatted_outcomes'] = [
                    f"Anda mendapatkan {value} dengan peluang {int(probability * 100)}%"
                    for value, probability in option['outcomes']
                ]

            player.participant.vars[key] = random_options

        random_options = player.participant.vars[key]

        # Ambil sisa uang subjek dari ronde sebelumnya
        if player.round_number > 1:
            previous_round_endowment = player.in_round(player.round_number - 1).payoff
            player.uang_sebelum_tambah_bansos = previous_round_endowment
            player.bantuan_sosial = Constants.additional
            player.uang_sesudah_tambah_bansos = (
                    player.uang_sebelum_tambah_bansos + player.bantuan_sosial
            )
            player.beban_konsumsi = Constants.consumption

        return {
            'random_options': random_options,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Key berdasarkan ronde
        key = f'random_options_round_{player.round_number}'

        # Daftar pilihan opsi
        selected_options = [
            (getattr(player, f"opsi_{i}"), f"hasil_opsi_{i}")
            for i in range(1, 6)
        ]

        # Proses setiap pilihan
        for selected_option_name, result_field in selected_options:
            selected_option = next(
                (
                    option
                    for option in Constants.options_data_price
                    if option['name'] == selected_option_name
                ),
                None
            )

            if selected_option:
                draw = random.randint(1, 100)
                cumulative_probability = 0

                for outcome, probability in selected_option['outcomes']:
                    cumulative_probability += probability * 100

                    if draw <= cumulative_probability:
                        setattr(player, result_field, outcome)
                        player.total_profit += outcome
                        break

        # Hapus data acakan ronde ini
        player.participant.vars.pop(key, None)


class single_results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        selected_options = [
            (getattr(player, f"opsi_{i}"), f"hasil_opsi_{i}")
            for i in range(1, 6)
        ]

        selected_count = sum(1 for option, _ in selected_options if option)
        player.total_biaya_beli_opsi = (selected_count * Constants.cost_per_option)

        player.payoff = ((player.uang_sesudah_tambah_bansos + player.total_profit) -
                         player.total_biaya_beli_opsi - player.beban_konsumsi)

        return {
            "options": [
                {
                    "no": i,
                    "result": getattr(player, f"hasil_opsi_{i}"),
                }
                for i in range(1, 6)
                if getattr(player, f"opsi_{i}")
            ]
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Hitung total cost berdasarkan opsi yang dipilih
        selected_options = [
            player.opsi_1,
            player.opsi_2,
            player.opsi_3,
            player.opsi_4,
            player.opsi_5
        ]

        # Filter opsi yang valid (tidak kosong) dan hitung biaya
        total_cost = len([option for option in selected_options if option]) * Constants.cost_per_option

        # Tambahkan payoff dan cost ke list di participant.vars
        if 'results_by_round_investment1' not in player.participant.vars:
            player.participant.vars['results_by_round_investment1'] = []

        player.participant.vars['results_by_round_investment1'].append({
            'round_number_investment1': player.round_number,
            'payoff_investment1': player.total_profit,
            'cost_investment1': total_cost,
            'endowment_investment1': player.payoff,
            'additional_investment1': player.bantuan_sosial,
            'consumption_investment1': player.beban_konsumsi
        })


class final_results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        # Ambil daftar hasil dari participant.vars
        results_by_round_investment1 = player.participant.vars.get('results_by_round_investment1', [])

        # Tentukan ronde terakhir yang dimainkan
        end_game = participant.vars.get('end_game', False)
        if end_game:
            last_round_investment1 = participant.vars.get('last_round_played_investment1', 1)
        else:
            last_round_investment1 = player.round_number

        # Ambil nilai payoff dari ronde terakhir yang dimainkan
        final_endowment_investment1 = player.in_round(last_round_investment1).payoff

        # Hitung total payoff dan total cost
        total_payoff_investment1 = sum(item['payoff_investment1'] for item in results_by_round_investment1)
        total_cost_investment1 = sum(item['cost_investment1'] for item in results_by_round_investment1)

        return {
            'results_by_round_investment1': results_by_round_investment1,
            'total_payoff_investment1': total_payoff_investment1,
            'total_cost_investment1': total_cost_investment1,
            'last_round_played_investment1': last_round_investment1,
            'final_endowment_investment1': final_endowment_investment1
        }


page_sequence = [endowment_information, game, single_results, final_results]
