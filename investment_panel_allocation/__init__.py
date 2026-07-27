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
    total_profit_return = models.CurrencyField(initial=0)
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
    total_akhir_profit_return = models.CurrencyField(initial=0)
    total_akhir_alokasi_opsi = models.CurrencyField(initial=0)
    total_akhir_bantuan_sosial = models.CurrencyField(initial=0)
    total_akhir_beban_konsumsi = models.CurrencyField(initial=0)
    total_akhir_uang = models.CurrencyField(initial=0)


class Loading(WaitPage):
    title_text = "Ruang Tunggu Eksperimen"


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
    form_fields = [f"asian_ev_{i}" for i in range(1, 18)]

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

        player.total_profit_return = sum(
            getattr(player, f"asian_ev_{i}") *
            getattr(player, f"result_asian_{i}")
            for i in range(1, 18)
        )


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

        # Tentukan ronde terakhir yang dimainkan
        end_game = participant.vars.get('end_game', False)
        if end_game:
            last_round_panel_allocation = participant.vars.get('last_round_played_panel_allocation', 1)
        else:
            last_round_panel_allocation = player.round_number

        final_endowment = player.in_round(last_round_panel_allocation).payoff

        # Ambil data semua ronde
        rounds_data = []
        for p in player.in_rounds(1, last_round_panel_allocation):
            rounds_data.append({
                'round_number': p.round_number,
                'return': p.total_profit_return,
                "cost": sum(getattr(p, f"asian_ev_{i}") for i in range(1, 18)),
                'endowment_panel_allocation': p.payoff,
                'additional_panel_allocation': p.bantuan_sosial,
                'consumption_panel_allocation': p.beban_konsumsi
            })

        # Hitung hasil akhir
        player.total_akhir_profit_return = sum(
            [p.total_profit_return for p in player.in_rounds(1, last_round_panel_allocation)]
        )
        player.total_akhir_alokasi_opsi = sum(
            getattr(p, f"asian_ev_{i}")
            for p in player.in_rounds(1, last_round_panel_allocation)
            for i in range(1, 18)
        )
        player.total_akhir_bantuan_sosial = sum(
            [p.bantuan_sosial for p in player.in_rounds(1, last_round_panel_allocation)]
        )
        player.total_akhir_beban_konsumsi = sum(
            [p.beban_konsumsi for p in player.in_rounds(1, last_round_panel_allocation)]
        )
        player.total_akhir_uang = sum([p.payoff for p in player.in_rounds(1, last_round_panel_allocation)])

        return {
            'last_round': last_round_panel_allocation,
            'final_endowment': final_endowment,
            'rounds_data': rounds_data,
        }


page_sequence = [endowment_information, Loading, game, single_results, Loading, final_results]
