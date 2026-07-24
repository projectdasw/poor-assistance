from otree.api import *
import random

doc = """
Real Effort Decoding
"""


class Constants(BaseConstants):
    name_in_url = 'real_effort_decoding'
    players_per_group = None
    num_rounds = 3
    endowment = cu(100)
    additional = cu(30)
    consumption = cu(50)

    # game Setup
    board_rows = 5  # Jumlah baris papan
    board_columns = 7  # Jumlah kolom papan
    price_time = 5
    target_character = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    uang_sesudah_tambah_bansos = models.CurrencyField(initial=0)
    uang_sebelum_tambah_bansos = models.CurrencyField(initial=0)
    bantuan_sosial = models.CurrencyField(initial=0)
    beban_konsumsi = models.CurrencyField(initial=0)
    beli_waktu = models.IntegerField(initial=0)
    waktu_bermain = models.IntegerField(initial=0)
    total_score = models.IntegerField(initial=0)
    count_guess = models.IntegerField(label="Berapa kali huruf/angka muncul:")
    actual_count = models.IntegerField(initial=0)
    current_target = models.StringField()  # Target huruf/angka yang diacak setiap putaran


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


class buy_time(Page):
    form_model = 'player'
    form_fields = ['beli_waktu']

    @staticmethod
    def vars_for_template(player: Player):
        # Ambil sisa uang subjek dari ronde sebelumnya
        if player.round_number > 1:
            previous_round_endowment = player.in_round(player.round_number - 1).payoff
            player.uang_sebelum_tambah_bansos = previous_round_endowment
            player.bantuan_sosial = Constants.additional
            player.uang_sesudah_tambah_bansos = player.uang_sebelum_tambah_bansos + player.bantuan_sosial
            player.beban_konsumsi = Constants.consumption

    @staticmethod
    def error_message(player: Player, values):
        error_msgs = []
        if values['beli_waktu'] > player.uang_sesudah_tambah_bansos:
            error_msgs.append(
                f"Uang Anda tidak cukup untuk membeli waktu."
            )
        elif values['beli_waktu'] % Constants.price_time != 0:
            error_msgs.append(
                f"Jumlah endowment yang dibelanjakan harus dalam kelipatan 5."
            )

        # Jika ada pesan kesalahan, gabungkan dan kembalikan
        if error_msgs:
            return "<br>".join(error_msgs)
        return ""


def live_method(player: Player, data):
    if 'count_guess' in data:
        guess = int(data['count_guess'])
        # Tambah skor jika jawaban benar
        if guess == player.actual_count:
            player.total_score += 3

        # Randomize ulang papan dan target karakter
        player.current_target = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        board = [
            [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for _ in range(Constants.board_columns)]
            for _ in range(Constants.board_rows)
        ]
        player.actual_count = sum(row.count(player.current_target) for row in board)

        # Return data untuk diperbarui di sisi klien
        return {
            player.id_in_group: {
                'new_board': board,
                'new_target_character': player.current_target,
                'new_score': player.total_score,
            }
        }


class game(Page):
    form_model = 'player'
    form_fields = ['count_guess']
    live_method = live_method

    # Menggunakan waktu yang dibeli oleh pemain
    @staticmethod
    def get_timeout_seconds(player: Player):
        return (player.beli_waktu // Constants.price_time) * 20

    @staticmethod
    def vars_for_template(player: Player):
        board = [
            [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for _ in range(Constants.board_columns)]
            for _ in range(Constants.board_rows)
        ]
        player.current_target = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        player.actual_count = sum(row.count(player.current_target) for row in board)

        return {
            'board': board,
            'target_character': player.current_target,
            'player_score': player.total_score,
        }


class single_results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        player.payoff = ((player.uang_sesudah_tambah_bansos + player.total_score) -
                         player.beli_waktu - player.beban_konsumsi)

        return {
            'final_score': player.total_score,
            'get_time': (player.beli_waktu // Constants.price_time) * 20,
            'sum_profit': player.uang_sesudah_tambah_bansos + player.total_score
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Simpan hasil ronde ke participant.vars
        if 'cognitive_task_results_investment3' not in player.participant.vars:
            player.participant.vars['cognitive_task_results_investment3'] = []

        player.participant.vars['cognitive_task_results_investment3'].append({
            'round_number_investment3': player.round_number,
            'score_investment3': player.total_score,
            'time_cost_investment3': player.beli_waktu,
            'endowment_investment3': player.payoff,
            'additional_investment3': player.bantuan_sosial,
            'consumption_investment3': player.beban_konsumsi
        })


class final_results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        all_rounds_results_investment3 = player.participant.vars.get('cognitive_task_results_investment3', [])

        # Tentukan ronde terakhir yang dimainkan
        end_game = participant.vars.get('end_game', False)
        if end_game:
            last_round_investment3 = participant.vars.get('last_round_played_investment3', 1)
        else:
            last_round_investment3 = player.round_number

        # Ambil nilai payoff dari ronde terakhir yang dimainkan
        final_endowment_investment3 = player.in_round(last_round_investment3).payoff

        # Ambil hasil dari semua ronde
        total_score_investment3 = sum(result['score_investment3'] for result in all_rounds_results_investment3)
        total_cost_investment3 = sum(result['time_cost_investment3'] for result in all_rounds_results_investment3)

        return {
            'last_round_investment3': last_round_investment3,
            'final_endowment_investment3': final_endowment_investment3,
            'all_rounds_results_investment3': all_rounds_results_investment3,
            'total_score_investment3': total_score_investment3,
            'total_cost_investment3': total_cost_investment3
        }


page_sequence = [endowment_information, buy_time, game, single_results, final_results]
