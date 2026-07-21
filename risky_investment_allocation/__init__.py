from otree.api import *
import random

doc = """
Risky Investment Allocation
"""


class Constants(BaseConstants):
    name_in_url = 'risky_investment_allocation'
    players_per_group = None
    num_rounds = 3
    endowment = cu(100)
    additional = cu(30)
    consumption = cu(50)
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
        {'name': 'Opsi 21', 'outcomes': [(3.5, 0.25), (0.5, 0.25), (0, 0.5)]},
        {'name': 'Opsi 22', 'outcomes': [(3.5, 0.25), (0.25, 0.5), (0, 0.25)]},
        {'name': 'Opsi 23', 'outcomes': [(3.5, 0.2), (1, 0.3), (0, 0.5)]},
        {'name': 'Opsi 24', 'outcomes': [(3.5, 0.2), (1.25, 0.25), (0, 0.55)]},
        {'name': 'Opsi 25', 'outcomes': [(3.5, 0.2), (0.75, 0.4), (0, 0.4)]},
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
    total_alokasi_opsi = models.CurrencyField(initial=0)
    opsi_1 = models.StringField(blank=True, initial="")
    alokasi_opsi_1 = models.FloatField(initial=0)
    hasil_opsi_1 = models.FloatField(initial=0)
    opsi_2 = models.StringField(blank=True, initial="")
    alokasi_opsi_2 = models.FloatField(initial=0)
    hasil_opsi_2 = models.FloatField(initial=0)
    opsi_3 = models.StringField(blank=True, initial="")
    alokasi_opsi_3 = models.FloatField(initial=0)
    hasil_opsi_3 = models.FloatField(initial=0)
    opsi_4 = models.StringField(blank=True, initial="")
    alokasi_opsi_4 = models.FloatField(initial=0)
    hasil_opsi_4 = models.FloatField(initial=0)
    opsi_5 = models.StringField(blank=True, initial="")
    alokasi_opsi_5 = models.FloatField(initial=0)
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
    form_fields = ['opsi_1', 'alokasi_opsi_1', 'opsi_2',
                   'alokasi_opsi_2', 'opsi_2', 'opsi_3',
                   'alokasi_opsi_3', 'opsi_4', 'alokasi_opsi_4',
                   'opsi_5', 'alokasi_opsi_5',]

    @staticmethod
    def vars_for_template(player: Player):
        # Ambil sisa uang subjek dari ronde sebelumnya
        if player.round_number > 1:
            previous_round_endowment = player.in_round(player.round_number - 1).payoff
            player.uang_sebelum_tambah_bansos = previous_round_endowment
            player.bantuan_sosial = Constants.additional
            player.uang_sesudah_tambah_bansos = player.uang_sebelum_tambah_bansos + player.bantuan_sosial
            player.beban_konsumsi = Constants.consumption

        # Mendapatkan 5 pilihan acak unik dari daftar opsi
        random_options = random.sample(Constants.options_data_allocation, 5)

        # Membuat teks yang terstruktur untuk setiap opsi
        for option in random_options:
            option_outcomes = option['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan {value}x dengan peluang {int(probability * 100)}%")
            option['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        return {
            'random_options': random_options,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Daftar pilihan yang dipilih pemain beserta alokasi dan hasilnya
        selected_allocations = [
            (
                getattr(player, f"opsi_{i}"),
                f"hasil_opsi_{i}",
                getattr(player, f"alokasi_opsi_{i}")
            )
            for i in range(1, 6)
        ]

        # Proses setiap pilihan
        for selected_name, result_field, allocation in selected_allocations:
            selected_option = next(
                (option for option in Constants.options_data_allocation if option['name'] == selected_name),
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
                        total_profit = (player.alokasi_opsi_1 * player.hasil_opsi_1) + \
                                       (player.alokasi_opsi_2 * player.hasil_opsi_2) + \
                                       (player.alokasi_opsi_3 * player.hasil_opsi_3) + \
                                       (player.alokasi_opsi_4 * player.hasil_opsi_4) + \
                                       (player.alokasi_opsi_5 * player.hasil_opsi_5)
                        player.total_profit = total_profit
                        break


class single_results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        allocations = [
            {
                "no": i,
                "option": getattr(player, f"opsi_{i}"),
                "allocation": allocation,
                "result": result,
                "profit": allocation * result,
            }
            for i in range(1, 6)
            for allocation, result in [(
                getattr(player, f"alokasi_opsi_{i}"),
                getattr(player, f"hasil_opsi_{i}")
            )]
            if allocation != 0
        ]

        player.total_profit = sum(item["profit"] for item in allocations)
        player.total_alokasi_opsi = sum(item["allocation"] for item in allocations)

        player.payoff = ((player.uang_sesudah_tambah_bansos + player.total_profit) -
                         player.total_alokasi_opsi - player.beban_konsumsi)

        return {
            "allocations": allocations,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Hitung total cost berdasarkan selected_optionprice
        total_cost = sum([
            player.alokasi_opsi_1,
            player.alokasi_opsi_2,
            player.alokasi_opsi_3,
            player.alokasi_opsi_4,
            player.alokasi_opsi_5
        ])

        # Tambahkan payoff dan cost ke list di participant.vars
        if 'results_by_round_investment2' not in player.participant.vars:
            player.participant.vars['results_by_round_investment2'] = []

        player.participant.vars['results_by_round_investment2'].append({
            'round_number_investment2': player.round_number,
            'payoff_investment2': player.total_profit,
            'cost_investment2': total_cost,
            'endowment_investment2': player.payoff,
            'additional_investment2': player.bantuan_sosial,
            'consumption_investment2': player.beban_konsumsi
        })


class final_results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        # Ambil daftar hasil dari participant.vars
        results_by_round_investment2 = player.participant.vars.get('results_by_round_investment2', [])

        # Tentukan ronde terakhir yang dimainkan
        end_game = participant.vars.get('end_game', False)
        if end_game:
            last_round_investment2 = participant.vars.get('last_round_played_investment2', 1)
        else:
            last_round_investment2 = player.round_number

        # Ambil nilai payoff dari ronde terakhir yang dimainkan
        final_endowment_investment2 = player.in_round(last_round_investment2).payoff

        # Hitung total payoff dan total cost
        total_payoff_investment2 = sum(item['payoff_investment2'] for item in results_by_round_investment2)
        total_cost_investment2 = sum(item['cost_investment2'] for item in results_by_round_investment2)

        return {
            'results_by_round_investment2': results_by_round_investment2,
            'total_payoff_investment2': total_payoff_investment2,
            'total_cost_investment2': total_cost_investment2,
            'last_round_investment2': last_round_investment2,
            'final_endowment_investment2': final_endowment_investment2
        }


page_sequence = [endowment_information, game, single_results, final_results]
