from otree.api import *
import random

doc = """
Investment Game 3
"""


class Constants(BaseConstants):
    name_in_url = 'cognitive_task'
    players_per_group = None
    num_rounds = 3
    subject_interest = 3  # Atur tingkat ketertarikan Subjek dalam mengikuti permainan
    board_rows = 5  # Jumlah baris papan
    board_columns = 7  # Jumlah kolom papan
    target_character = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.CurrencyField(initial=0)
    additional_endowment = models.CurrencyField(initial=0)
    consumption_cost = models.CurrencyField(initial=0)
    buy_time = models.IntegerField(initial=0)
    score = models.IntegerField(initial=0)
    count_guess = models.IntegerField(label="Berapa kali huruf/angka muncul:")
    actual_count = models.IntegerField(initial=0)
    current_target = models.StringField()  # Target huruf/angka yang diacak setiap putaran
    offer_accepted = models.BooleanField(choices=[True, False], initial=None)
    subject_action = models.StringField(
        choices=['start', 'end'],  # Tombol yang dipilih
        initial="", blank=True
    )


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
            player.endowment = participant.dynamic_endowment
            player.participant.vars['end_game'] = False
        else:
            # Jika pemain memilih 'No', tandai end_game dan arahkan ke AllResults
            player.participant.vars['end_game'] = True
            # Tetapkan ronde terakhir bermain
            player.endowment = participant.dynamic_endowment
            player.payoff = player.endowment


class BuyTime(Page):
    form_model = 'player'
    form_fields = ['buy_time', 'subject_action']

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Ya"
        return not player.participant.vars.get('end_game', False)

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        # Hitung total skip akumulatif
        still_interested = sum(1 for p in player.in_all_rounds() if p.subject_action == 'start')

        # Simpan endowment terakhir
        previous_round_endowment = player.in_round(
            player.round_number - 1).payoff + participant.dynamic_additional_endowment \
            if player.round_number > 1 else participant.dynamic_endowment + participant.dynamic_additional_endowment
        player.endowment = previous_round_endowment
        player.additional_endowment = participant.dynamic_additional_endowment

        return {'checkpoint': still_interested}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        action = player.subject_action

        if action == "start":
            player.endowment -= player.buy_time
        elif action == "end":
            # Hentikan permainan dan ambil endowment dari ronde sebelumnya
            player.participant.vars['end_game'] = True
            last_round = player.round_number - 1 if player.round_number > 1 else 1
            player.participant.vars['last_round_played_investment3'] = last_round

            # Tetapkan endowment ke nilai payoff ronde sebelumnya
            previous_round = player.in_round(last_round)
            player.endowment = previous_round.payoff
            player.payoff = player.endowment



    @staticmethod
    def error_message(player: Player, values):
        if values['subject_action'] == "start":
            error_msgs = []
            if values['buy_time'] > player.endowment:
                error_msgs.append(
                    f"Anda tidak memiliki cukup endowment untuk membeli waktu."
                )
            elif values['buy_time'] % 10 != 0:
                error_msgs.append(
                    f"Jumlah endowment yang dibelanjakan harus dalam kelipatan 10."
                )
            elif values['buy_time'] == 0:
                error_msgs.append(
                    f"Anda tidak melakukan alokasi untuk membeli waktu."
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
            player.score += 2

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
                'new_score': player.score,
            }
        }


class Game(Page):
    form_model = 'player'
    form_fields = ['count_guess']
    live_method = live_method

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan permainan jika subjek memilih "Mulai"
        return not player.participant.vars.get('end_game', False)

    # Menggunakan waktu yang dibeli oleh pemain
    @staticmethod
    def get_timeout_seconds(player: Player):
        return (player.buy_time // 10) * 20  # Setiap 10 endowment = 20 detik

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
            'player_score': player.score,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        # Penentuan Beban Konsumsi
        sum_profit = player.endowment + player.score
        consumption_fix = sum_profit - participant.dynamic_consumption_cost
        if sum_profit < participant.dynamic_consumption_cost:
            player.consumption_cost = sum_profit
            player.payoff = 0
        else:
            player.consumption_cost = participant.dynamic_consumption_cost
            player.payoff = consumption_fix


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not player.participant.vars.get('end_game', False)

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'final_score': player.score,
            'get_time': (player.buy_time // 10) * 20,
            'sum_profit': player.endowment + player.score
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Simpan hasil ronde ke participant.vars
        if 'cognitive_task_results_investment3' not in player.participant.vars:
            player.participant.vars['cognitive_task_results_investment3'] = []

        player.participant.vars['cognitive_task_results_investment3'].append({
            'round_number_investment3': player.round_number,
            'score_investment3': player.score,
            'time_cost_investment3': player.buy_time,
            'endowment_investment3': player.payoff,
            'additional_investment3': player.additional_endowment,
            'consumption_investment3': player.consumption_cost
        })


class AllResults(Page):
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

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        all_rounds_results_investment3 = player.participant.vars.get('cognitive_task_results_investment3', [])

        if participant.vars.get('end_game', False):
            last_round = participant.vars.get('last_round_played_investment2', 1)
            participant.dynamic_endowment = player.in_round(last_round).payoff
        else:
            participant.dynamic_endowment = player.payoff

        participant.app_investment3 = sum(result['score_investment3'] for result in all_rounds_results_investment3)


page_sequence = [Welcome, Instruction, Confirmation, BuyTime, Game, Results, AllResults]