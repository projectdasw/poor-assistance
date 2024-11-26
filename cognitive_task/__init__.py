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
    num_rounds = 2
    initial_endowment = 100
    board_rows = 5  # Jumlah baris papan
    board_columns = 10 # Jumlah kolom papan
    target_character = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.CurrencyField()
    buy_time = models.IntegerField(initial=0)
    count_guess = models.IntegerField(label="Berapa kali huruf/angka muncul:")
    actual_count = models.IntegerField(initial=0)
    score = models.IntegerField(initial=0)
    current_target = models.StringField()  # Target huruf/angka yang diacak setiap putaran
    offer_accepted = models.BooleanField(
        choices=[
            (True, 'Iya'),
            (False, 'Tidak')
        ]
    )


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


class BuyTime(Page):
    form_model = 'player'
    form_fields = ['buy_time']

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Ya" di ronde pertama
        return player.participant.offer_accepted is True

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        # Dynamic Endowment
        if player.round_number > 1:
            # Endowment dari periode sebelumnya digunakan kembali pada periode berikutnya
            previous_player = player.in_round(player.round_number - 1)
            participant.get_endowment = previous_player.endowment  # Menampilkan endowment periode sebelumnya
            player.endowment = previous_player.endowment  # Ambil endowment dari periode sebelumnya

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Memastikan input adalah kelipatan 10 dan tidak melebihi endowment yang ada
        if player.buy_time % 10 == 0 and player.buy_time <= player.endowment:
            player.endowment -= player.buy_time
        else:
            # Jika endowment 0, maka waktu pembelian adalah 0
            player.buy_time = 0

    @staticmethod
    def error_message(player: Player, values):
        if values['buy_time'] > player.endowment:
            return 'Anda tidak memiliki cukup endowment untuk membeli waktu ini.'
        if values['buy_time'] % 10 != 0:
            return 'Jumlah endowment yang dibelanjakan harus dalam kelipatan 10.'


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

    # Menggunakan waktu yang dibeli oleh pemain
    @staticmethod
    def get_timeout_seconds(player: Player):
        return (player.buy_time // 10) * 20  # Setiap 10 endowment = 20 detik

    @staticmethod
    def vars_for_template(player: Player):
        # Membuat papan dengan 3 baris dan 13 kolom
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
    def vars_for_template(player: Player):
        return {
            'final_score': player.score,
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

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        # Jika pemain memilih "Tidak" di ronde pertama, langsung ke aplikasi berikutnya
        if player.participant.offer_accepted is False:
            return 'asian_handicap'  # Ganti dengan nama aplikasi berikutnya


class AllResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        # Ambil hasil dari semua ronde
        all_rounds_results = player.participant.vars.get('cognitive_task_results', [])
        total_score = sum(result['score'] for result in all_rounds_results)
        total_cost = sum(result['time_cost'] for result in all_rounds_results)

        return {
            'all_rounds_results': all_rounds_results,
            'total_score': total_score,
            'total_cost': total_cost,
        }


page_sequence = [Confirmation, BuyTime, Game, Results, AllResults]
