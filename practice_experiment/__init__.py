from otree.api import *
import random
import json
from pathlib import Path

doc = """
Poor Assistance Experiment
"""


def load_word_list():
    # words from https://github.com/dovenokan/oxford-words
    return set(Path(__name__ + '/words.txt').read_text().split())


class Constants(BaseConstants):
    name_in_url = 'practice_experiment'
    players_per_group = None
    num_rounds = 3  # 5 periods
    initial_endowment = 100
    additional_endowment = 30
    deduction = 50

    # RISKY OPTION - PRICE
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
    ]
    # RISKY OPTION - PRICE

    # RISKY OPTION - ALLOCATION
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
    # RISKY OPTION - ALLOCATION

    # COGINITIVE TASK
    board_rows = 3  # Jumlah baris papan
    board_columns = 13  # Jumlah kolom papan
    target_character = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')  # Huruf atau angka yang dicari
    # COGINITIVE TASK

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.FloatField()

    # RISKY OPTION - PRICE
    selected_optionprice = models.StringField()
    result_price = models.FloatField(initial=0)
    # RISKY OPTION - PRICE

    # RISKY OPTION - ALLOCATION
    selected_optionallocation = models.StringField()
    allocation_invest = models.FloatField(initial=0)
    result_allocation = models.FloatField(initial=0)
    # RISKY OPTION - ALLOCATION

    buy_time = models.IntegerField(initial=0, label='Masukkan jumlah Endowment yang ingin Anda gunakan untuk membeli waktu')
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


class Intro(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Menggunakan PARTICIPANT sebagai variabel menampilkan hasil pada tampilan halaman
        participant = player.participant

        # Dynamic Endowment
        if player.round_number == 1:
            # Inisialisasi Endowment Awal Periode
            player.endowment = Constants.initial_endowment
            player.endowment += Constants.additional_endowment - Constants.deduction
        else:
            # Endowment dari periode sebelumnya digunakan kembali pada periode berikutnya
            previous_player = player.in_round(player.round_number - 1)
            participant.get_endowment = previous_player.endowment  # Menampilkan endowment periode sebelumnya
            player.endowment = previous_player.endowment  # Ambil endowment dari periode sebelumnya
            player.endowment += Constants.additional_endowment - Constants.deduction

        return {
            'endowment': player.endowment,
        }


class BeforeGame1(Page):
    form_model = 'player'
    form_fields = ['offer_accepted']


class BeforeGame2(Page):
    form_model = 'player'
    form_fields = ['offer_accepted']


class RiskyOption_Price(Page):
    form_model = 'player'
    form_fields = ['selected_optionprice']

    @staticmethod
    def vars_for_template(player: Player):
        # Mendapatkan pilihan acak (contoh daftar pilihan opsi)
        random_options = random.sample(Constants.options_data_price, 5)

        # Membuat teks yang terstruktur untuk setiap opsi dalam format list items
        for i, option in enumerate(random_options):
            option_outcomes = option['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan {value} dengan peluang {int(probability * 100)}%")
            option['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        return {
            'random_options': random_options,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Temukan opsi yang dipilih pemain berdasarkan nama
        selected_option = next(
            (option for option in Constants.options_data_price if option['name'] == player.selected_optionprice), None
        )

        # Lakukan drawing angka 1-100
        if selected_option:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_price = outcome
                    player.endowment -= 25
                    break

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Iya"
        return player.offer_accepted is not None and player.offer_accepted


class PriceResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'result': player.result_price
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.endowment += player.result_price

        # player.endowment += player.result_price1 + player.result_price2 +\
        #                     player.result_price3 + player.result_price4 +\
        #                     player.result_price5


class RiskyOption_Allocation(Page):
    form_model = 'player'
    form_fields = ['allocation_invest', 'selected_optionallocation']

    @staticmethod
    def vars_for_template(player: Player):
        # Mendapatkan pilihan acak (contoh daftar pilihan opsi)
        random_options = random.sample(Constants.options_data_allocation, 5)

        # Membuat teks yang terstruktur untuk setiap opsi dalam format list items
        for i, option in enumerate(random_options):
            option_outcomes = option['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        return {
            'random_options': random_options,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Temukan opsi yang dipilih pemain berdasarkan nama
        selected_option = next(
            (option for option in Constants.options_data_allocation if option['name'] == player.selected_optionallocation), None
        )

        # Lakukan drawing angka 1-100
        if selected_option:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_allocation = outcome
                    player.endowment -= player.allocation_invest
                    break

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Iya"
        return player.offer_accepted is not None and player.offer_accepted


class AllocationResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'allocation': player.allocation_invest,
            'result': player.result_allocation
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.endowment += player.allocation_invest * player.result_allocation


class Confirmation_Cognitive_Task(Page):
    pass


class Buytime(Page):
    form_model = 'player'
    form_fields = ['buy_time']

    @staticmethod
    def error_message(player: Player, values):
        if values['buy_time'] > player.endowment:
            return 'Anda tidak memiliki cukup endowment untuk membeli waktu ini.'
        if values['buy_time'] % 10 != 0:
            return 'Jumlah endowment yang dibelanjakan harus dalam kelipatan 10.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Memastikan input adalah kelipatan 10 dan tidak melebihi endowment yang ada
        if player.buy_time % 10 == 0 and player.buy_time <= player.endowment:
            player.endowment -= player.buy_time
        else:
            # Jika endowment 0, maka waktu pembelian adalah 0
            player.buy_time = 0


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


class Game3(Page):
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


class Game3_Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'final_score': player.score,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.endowment = player.endowment + player.score
# COGNITIVE TASK DEVOPS

class Game4(Page):
    pass


class Results(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        previous_player = player.in_round(player.round_number)
        player.endowment = previous_player.endowment

        participant = player.participant

        if player.round_number == Constants.num_rounds:
            random_round = random.randint(1, Constants.num_rounds)
            participant.selected_round = random_round
            player_in_selected_round = player.in_round(random_round)
            participant.get_payment = player_in_selected_round.payoff

    @staticmethod
    def vars_for_template(player: Player):
        player.payoff = player.endowment


page_sequence = [Intro, BeforeGame1, RiskyOption_Price, PriceResults, BeforeGame2, RiskyOption_Allocation,
                 AllocationResults, Confirmation_Cognitive_Task, Buytime, Game3, Game3_Results, Game4, Results]

# page_sequence = [Intro, BeforeGame1, RiskyOption_Price1, RiskyOption_Price2, RiskyOption_Price3, RiskyOption_Price4,
#                  RiskyOption_Price5, PriceResults, BeforeGame2, Game2, Confirmation_Cognitive_Task, Buytime, Game3,
#                  Game3_Results, Game4, Results]
