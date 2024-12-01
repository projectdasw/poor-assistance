from otree.api import *
import random
import json
from pathlib import Path

doc = """
Cognitive Task
"""

class Constants(BaseConstants):
    name_in_url = 'cognitive_task'
    players_per_group = None
    num_rounds = 10
    subject_interest = 5 # Atur tingkat ketertarikan Subjek dalam mengikuti permainan
    board_rows = 5  # Jumlah baris papan
    board_columns = 10 # Jumlah kolom papan
    target_character = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.CurrencyField(initial=0)
    buy_time = models.IntegerField(initial=0)
    count_guess = models.IntegerField(label="Berapa kali huruf/angka muncul:")
    actual_count = models.IntegerField(initial=0)
    score = models.IntegerField(initial=0)
    current_target = models.StringField()  # Target huruf/angka yang diacak setiap putaran
    offer_accepted = models.BooleanField(choices=[(True), (False)], initial=None)
    subject_action = models.StringField(
        choices=['start', 'end', 'endowment_limit'],  # Tombol yang dipilih
        initial="", blank=True
    )


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
        player.endowment = player.participant.dynamic_endowment

        if player.participant.offer_accepted:
            # Jika pemain memilih 'Yes', lanjutkan ke Game
            pass
        else:
            # Jika pemain memilih 'No', tandai end_game dan arahkan ke AllResults
            player.participant.vars['end_game'] = True
            # Tetapkan ronde terakhir bermain
            player.participant.vars['last_round_played'] = player.round_number
            player.payoff = player.endowment


class BuyTime(Page):
    form_model = 'player'
    form_fields = ['buy_time', 'subject_action']

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Ya"
        return player.participant.offer_accepted is True and not player.participant.vars.get('end_game', False)

    @staticmethod
    def vars_for_template(player: Player):
        # Hitung total skip akumulatif
        still_interested = sum(1 for p in player.in_all_rounds() if p.subject_action == 'start')

        # Simpan endowment terakhir
        previous_round_endowment = player.in_round(
            player.round_number - 1).endowment if player.round_number > 1 else player.participant.dynamic_endowment
        player.endowment = previous_round_endowment

        return {'checkpoint': still_interested}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        action = player.subject_action
        if action == "start":
            player.endowment -= player.buy_time
        elif action == "end" or action == "endowment_limit":
            # Permainan selesai
            player.participant.vars['end_game'] = True
            # Tetapkan ronde terakhir bermain
            player.participant.vars['last_round_played'] = player.round_number
            # Simpan endowment terakhir
            previous_round_endowment = player.in_round(
                player.round_number - 1).endowment if player.round_number > 1 else player.participant.dynamic_endowment
            player.endowment = previous_round_endowment
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


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not player.participant.vars.get('end_game', False)

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'final_score': player.score,
            'get_time': (player.buy_time // 10) * 20
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Update endowment dengan skor ronde ini
        player.endowment += player.score
        player.payoff = player.endowment

        # Simpan hasil ronde ke participant.vars
        if 'cognitive_task_results' not in player.participant.vars:
            player.participant.vars['cognitive_task_results'] = []

        player.participant.vars['cognitive_task_results'].append({
            'round_number': player.round_number,
            'score': player.score,
            'time_cost': player.buy_time
        })


class AllResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        # Ambil ronde terakhir bermain
        last_round = player.participant.vars.get('last_round_played', player.round_number)
        final_endowment = player.in_round(last_round).endowment

        # Ambil hasil dari semua ronde
        all_rounds_results = player.participant.vars.get('cognitive_task_results', [])
        total_score = sum(result['score'] for result in all_rounds_results)
        total_cost = sum(result['time_cost'] for result in all_rounds_results)

        return {
            'last_round': last_round,
            'final_endowment': final_endowment,
            'all_rounds_results': all_rounds_results,
            'total_score': total_score,
            'total_cost': total_cost
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.dynamic_endowment = player.endowment


page_sequence = [Welcome, Confirmation, BuyTime, Game, Results, AllResults]