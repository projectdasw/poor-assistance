from otree.api import *
import random

doc = """
Investment Game 4
"""


class Constants(BaseConstants):
    name_in_url = 'investment_game4'
    players_per_group = None
    num_rounds = 3
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
    additional_endowment = models.CurrencyField(initial=0)
    consumption_cost = models.CurrencyField(initial=0)
    total_return = models.FloatField(initial=0)
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
    offer_accepted = models.BooleanField(choices=[True, False], initial=None)
    subject_action = models.StringField(
        choices=['skip', 'invested'], initial="", blank=True
    )  # Untuk mencatat tombol yang dipilih

    still_interested = models.StringField(
        choices=['yes', 'no'], initial="", blank=True
    )  # Untuk mencatat tombol yang dipilih


class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instruction(Page):
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
        participant = player.participant
        player.participant.offer_accepted = player.offer_accepted

        if player.participant.offer_accepted:
            # Jika pemain memilih 'Yes', lanjutkan ke Game
            player.participant.vars['end_game'] = False
            player.endowment = participant.dynamic_endowment
        else:
            # Jika pemain memilih 'No', tandai end_game dan arahkan ke AllResults
            player.participant.vars['end_game'] = True
            # Tetapkan ronde terakhir bermain
            player.endowment = participant.dynamic_endowment
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
        participant = player.participant
        if player.still_interested == "no":
            # Hentikan permainan dan ambil endowment dari ronde sebelumnya
            player.participant.vars['end_game'] = True
            last_round = player.round_number - 1 if player.round_number > 1 else 1
            player.participant.vars['last_round_played_investment4'] = last_round

            # Tetapkan endowment ke nilai payoff ronde sebelumnya
            previous_round = player.in_round(last_round)
            player.endowment = previous_round.payoff + participant.dynamic_additional_endowment
            player.payoff = player.endowment
        elif player.still_interested == "yes":
            # Lanjutkan permainan
            player.participant.vars['end_game'] = False
            last_round = player.round_number - 1 if player.round_number > 1 else 1
            previous_round = player.in_round(last_round)
            player.endowment = previous_round.payoff + participant.dynamic_additional_endowment

            # Perbarui checkpoint skip
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
        participant = player.participant

        previous_round_endowment = player.in_round(
            player.round_number - 1).payoff + participant.dynamic_additional_endowment \
            if player.round_number > 1 else participant.dynamic_endowment + participant.dynamic_additional_endowment
        player.endowment = previous_round_endowment
        player.additional_endowment = participant.dynamic_additional_endowment

        # Menyediakan investment_scheme untuk template
        return {
            'investment_scheme': Constants.investment_scheme,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant

        if player.subject_action == 'skip':
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

            player.total_return = sum([
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

            player.endowment = player.endowment - sum([
                player.asian_ev_1, player.asian_ev_2, player.asian_ev_3, player.asian_ev_4, player.asian_ev_5,
                player.asian_ev_6, player.asian_ev_7, player.asian_ev_8, player.asian_ev_9, player.asian_ev_10,
                player.asian_ev_11, player.asian_ev_12, player.asian_ev_13, player.asian_ev_14,
                player.asian_ev_15, player.asian_ev_16, player.asian_ev_17
            ])

        # Penentuan Beban Konsumsi
        sum_profit = player.endowment + player.total_return
        consumption_fix = sum_profit - participant.dynamic_consumption_cost
        if sum_profit < participant.dynamic_consumption_cost:
            player.consumption_cost = sum_profit
            player.payoff = 0
        else:
            player.consumption_cost = participant.dynamic_consumption_cost
            player.payoff = consumption_fix


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
        sum_profit = player.endowment + player.total_return

        return {
            'investment_results': investment_results,
            'total_allocation': total_allocation,
            'total_return': total_return,
            'sum_profit': sum_profit,
        }


class AllResults(Page):
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
                'return': p.total_return,
                'cost': sum([
                    p.asian_ev_1, p.asian_ev_2, p.asian_ev_3, p.asian_ev_4, p.asian_ev_5,
                    p.asian_ev_6, p.asian_ev_7, p.asian_ev_8, p.asian_ev_9, p.asian_ev_10,
                    p.asian_ev_11, p.asian_ev_12, p.asian_ev_13, p.asian_ev_14, p.asian_ev_15,
                    p.asian_ev_16, p.asian_ev_17
                ]),
                'payoff': p.payoff,
                'endowment_investment4': p.payoff,
                'additional_investment4': p.additional_endowment,
                'consumption_investment4': p.consumption_cost
            })

        # Hitung hasil akhir
        final_return = sum([p.total_return for p in player.in_rounds(1, last_round_investment4)])
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


page_sequence = [Welcome, Instruction, Confirmation, CheckInterest, Game, Results, AllResults]
