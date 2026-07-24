from otree.api import *
import random

doc = """
Investment Panel Allocation
"""


class Constants(BaseConstants):
    name_in_url = 'investment_panel_allocation'
    players_per_group = None
    num_rounds = 3
    endowment = cu(100)
    additional = cu(30)
    consumption = cu(50)
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
    uang_sesudah_tambah_bansos = models.CurrencyField(initial=0)
    uang_sebelum_tambah_bansos = models.CurrencyField(initial=0)
    bantuan_sosial = models.CurrencyField(initial=0)
    beban_konsumsi = models.CurrencyField(initial=0)
    total_profit_return = models.FloatField(initial=0)
    total_alokasi_opsi = models.CurrencyField(initial=0)
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
    form_model = "player"
    form_fields = [
        'asian_ev_1', 'asian_ev_2', 'asian_ev_3', 'asian_ev_4', 'asian_ev_5', 'asian_ev_6', 'asian_ev_7', 'asian_ev_8',
        'asian_ev_9', 'asian_ev_10', 'asian_ev_11', 'asian_ev_12', 'asian_ev_13', 'asian_ev_14', 'asian_ev_15',
        'asian_ev_16', 'asian_ev_17'
    ]

    # @staticmethod
    # def is_displayed(player: Player):
    #     # Hanya tampilkan halaman ini jika pemain memilih "Ya" di ronde pertama
    #     return not player.participant.vars.get('end_game', False)

    @staticmethod
    def vars_for_template(player: Player):
        # Ambil sisa uang subjek dari ronde sebelumnya
        if player.round_number > 1:
            previous_round_endowment = player.in_round(player.round_number - 1).payoff
            player.uang_sebelum_tambah_bansos = previous_round_endowment
            player.bantuan_sosial = Constants.additional
            player.uang_sesudah_tambah_bansos = player.uang_sebelum_tambah_bansos + player.bantuan_sosial
            player.beban_konsumsi = Constants.consumption

        # Mengonversi probabilitas menjadi persentase
        investment_scheme_with_percentage = [
            {
                "investment_return": scheme["investment_return"],
                "probability": int(scheme["probability"] * 100)  # Konversi ke persentase
            }
            for scheme in Constants.investment_scheme
        ]

        return {
            'investment_scheme': investment_scheme_with_percentage,
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

        player.total_profit_return = sum([
            (player.asian_ev_1 * player.result_asian_1), (player.asian_ev_2 * player.result_asian_2),
            (player.asian_ev_3 * player.result_asian_3), (player.asian_ev_4 * player.result_asian_4),
            (player.asian_ev_5 * player.result_asian_5), (player.asian_ev_6 * player.result_asian_6),
            (player.asian_ev_7 * player.result_asian_7), (player.asian_ev_8 * player.result_asian_8),
            (player.asian_ev_9 * player.result_asian_9), (player.asian_ev_10 * player.result_asian_10),
            (player.asian_ev_11 * player.result_asian_11), (player.asian_ev_12 * player.result_asian_12),
            (player.asian_ev_13 * player.result_asian_13), (player.asian_ev_14 * player.result_asian_14),
            (player.asian_ev_15 * player.result_asian_15), (player.asian_ev_16 * player.result_asian_16),
            (player.asian_ev_17 * player.result_asian_17)
        ])

        # player.uang_sesudah_tambah_bansos = player.uang_sesudah_tambah_bansos - sum([
        #     player.asian_ev_1, player.asian_ev_2, player.asian_ev_3, player.asian_ev_4, player.asian_ev_5,
        #     player.asian_ev_6, player.asian_ev_7, player.asian_ev_8, player.asian_ev_9, player.asian_ev_10,
        #     player.asian_ev_11, player.asian_ev_12, player.asian_ev_13, player.asian_ev_14,
        #     player.asian_ev_15, player.asian_ev_16, player.asian_ev_17
        # ])


    @staticmethod
    def error_message(player: Player, values):
        # Hitung total investasi
        total_investasi = (values['asian_ev_1'] + values['asian_ev_2'] + values['asian_ev_3'] +
                           values['asian_ev_4'] + values['asian_ev_5'] + values['asian_ev_6'] +
                           values['asian_ev_7'] + values['asian_ev_8'] + values['asian_ev_9'] +
                           values['asian_ev_10'] + values['asian_ev_11'] + values['asian_ev_12'] +
                           values['asian_ev_13'] + values['asian_ev_14'] + values['asian_ev_15'] +
                           values['asian_ev_16'] + values['asian_ev_17'])

        # Periksa apakah total investasi melebihi uang_sebelum_tambah_bansos
        error_msgs = []
        if total_investasi > player.uang_sesudah_tambah_bansos:
            error_msgs.append(
                f"Endowment Anda tidak mencukupi untuk membeli opsi-opsi tersebut"
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


class single_results(Page):
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
        sum_profit = player.uang_sesudah_tambah_bansos + player.total_profit_return
        player.total_alokasi_opsi = total_allocation
        player.payoff = ((player.uang_sesudah_tambah_bansos + player.total_profit_return) -
                         player.total_alokasi_opsi - player.beban_konsumsi)

        return {
            'investment_results': investment_results,
            'total_allocation': total_allocation,
            'total_profit_return': total_return,
            'sum_profit': sum_profit,
        }


class final_results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        # Ambil ronde terakhir bermain
        last_round_investment4 = player.participant.vars.get('last_round_played_investment4', player.round_number)

        # Tentukan ronde terakhir yang dimainkan
        end_game = participant.vars.get('end_game', False)
        if end_game:
            last_round_investment4 = participant.vars.get('last_round_played_investment4', 1)
        else:
            last_round_investment4 = player.round_number

        final_endowment = player.in_round(last_round_investment4).payoff

        # Ambil data semua ronde
        rounds_data = []
        for p in player.in_rounds(1, last_round_investment4):
            rounds_data.append({
                'round_number': p.round_number,
                'return': p.total_profit_return,
                'cost': sum([
                    p.asian_ev_1, p.asian_ev_2, p.asian_ev_3, p.asian_ev_4, p.asian_ev_5,
                    p.asian_ev_6, p.asian_ev_7, p.asian_ev_8, p.asian_ev_9, p.asian_ev_10,
                    p.asian_ev_11, p.asian_ev_12, p.asian_ev_13, p.asian_ev_14, p.asian_ev_15,
                    p.asian_ev_16, p.asian_ev_17
                ]),
                'payoff': p.payoff,
                'endowment_investment4': p.payoff,
                'additional_investment4': p.bantuan_sosial,
                'consumption_investment4': p.beban_konsumsi
            })

        # Hitung hasil akhir
        final_return = sum([p.total_profit_return for p in player.in_rounds(1, last_round_investment4)])
        final_cost = sum([
            sum([
                p.asian_ev_1, p.asian_ev_2, p.asian_ev_3, p.asian_ev_4, p.asian_ev_5,
                p.asian_ev_6, p.asian_ev_7, p.asian_ev_8, p.asian_ev_9, p.asian_ev_10,
                p.asian_ev_11, p.asian_ev_12, p.asian_ev_13, p.asian_ev_14, p.asian_ev_15,
                p.asian_ev_16, p.asian_ev_17
            ])
            for p in player.in_rounds(1, last_round_investment4)
        ])
        final_payoff = sum([p.payoff for p in player.in_rounds(1, last_round_investment4)])

        return {
            'last_round': last_round_investment4,
            'final_endowment': final_endowment,
            'rounds_data': rounds_data,
            'final_return': final_return,
            'final_cost': final_cost,
            'final_payoff': final_payoff
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        results_by_round_investment4 = player.participant.vars.get('results_by_round_investment4', [])

        if participant.vars.get('end_game', False):
            last_round = participant.vars.get('last_round_played_investment4', 1)
            participant.dynamic_endowment = player.in_round(last_round).payoff
        else:
            participant.dynamic_endowment = player.payoff

        participant.app_investment4 = sum(item['final_return'] for item in results_by_round_investment4)


page_sequence = [endowment_information, game, single_results, final_results]
