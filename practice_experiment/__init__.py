from otree.api import *
import random
import json
from pathlib import Path

doc = """
Poor Assistance Experiment
"""

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
    target_character = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    # COGINITIVE TASK


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.FloatField()

    # RISKY OPTION - PRICE
    selected_optionprice1 = models.StringField(blank=True, initial="")
    result_price1 = models.FloatField(initial=0)
    selected_optionprice2 = models.StringField(blank=True, initial="")
    result_price2 = models.FloatField(initial=0)
    selected_optionprice3 = models.StringField(blank=True, initial="")
    result_price3 = models.FloatField(initial=0)
    selected_optionprice4 = models.StringField(blank=True, initial="")
    result_price4 = models.FloatField(initial=0)
    selected_optionprice5 = models.StringField(blank=True, initial="")
    result_price5 = models.FloatField(initial=0)
    # RISKY OPTION - PRICE

    # RISKY OPTION - ALLOCATION
    selected_optionallocation1 = models.StringField()
    allocation_invest1 = models.FloatField(initial=0)
    result_allocation1 = models.FloatField(initial=0)
    selected_optionallocation2 = models.StringField()
    allocation_invest2 = models.FloatField(initial=0)
    result_allocation2 = models.FloatField(initial=0)
    selected_optionallocation3 = models.StringField()
    allocation_invest3 = models.FloatField(initial=0)
    result_allocation3 = models.FloatField(initial=0)
    selected_optionallocation4 = models.StringField()
    allocation_invest4 = models.FloatField(initial=0)
    result_allocation4 = models.FloatField(initial=0)
    selected_optionallocation5 = models.StringField()
    allocation_invest5 = models.FloatField(initial=0)
    result_allocation5 = models.FloatField(initial=0)
    # RISKY OPTION - ALLOCATION

    # COGNITIVE TASK
    buy_time = models.IntegerField(initial=0, label='Masukkan jumlah Endowment yang ingin Anda gunakan untuk membeli waktu')
    count_guess = models.IntegerField(label="Berapa kali huruf/angka muncul:")
    actual_count = models.IntegerField(initial=0)
    score = models.IntegerField(initial=0)
    current_target = models.StringField()  # Target huruf/angka yang diacak setiap putaran
    # COGNITIVE TASK

    # ASIAN HANDICAP
    return_values = models.FloatField()
    pr_of_winning_values = models.FloatField()
    # ASIAN HANDICAP

    offer_accepted = models.BooleanField(
        choices=[
            (True, 'Iya'),
            (False, 'Tidak')
        ]
    )


class Intro(Page):
    @staticmethod
    def vars_for_template(player: Player):
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
    form_fields = ['selected_optionprice1', 'selected_optionprice2', 'selected_optionprice3', 'selected_optionprice4',
                   'selected_optionprice5']

    @staticmethod
    def vars_for_template(player: Player):
        # Mendapatkan pilihan acak (contoh daftar pilihan opsi)
        random_options1 = random.sample(Constants.options_data_price, 1)
        random_options2 = random.sample(Constants.options_data_price, 1)
        random_options3 = random.sample(Constants.options_data_price, 1)
        random_options4 = random.sample(Constants.options_data_price, 1)
        random_options5 = random.sample(Constants.options_data_price, 1)

        # Membuat teks yang terstruktur untuk setiap opsi dalam format list items
        for i, option1 in enumerate(random_options1):
            option_outcomes = option1['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan {value} dengan peluang {int(probability * 100)}%")
            option1['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option2 in enumerate(random_options2):
            option_outcomes = option2['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan {value} dengan peluang {int(probability * 100)}%")
            option2['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option3 in enumerate(random_options3):
            option_outcomes = option3['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan {value} dengan peluang {int(probability * 100)}%")
            option3['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option4 in enumerate(random_options4):
            option_outcomes = option4['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan {value} dengan peluang {int(probability * 100)}%")
            option4['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option5 in enumerate(random_options5):
            option_outcomes = option5['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan {value} dengan peluang {int(probability * 100)}%")
            option5['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        return {
            'random_options1': random_options1,
            'random_options2': random_options2,
            'random_options3': random_options3,
            'random_options4': random_options4,
            'random_options5': random_options5,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Temukan opsi yang dipilih pemain berdasarkan nama
        selected_option1 = next(
            (option1 for option1 in Constants.options_data_price if
             option1['name'] == player.selected_optionprice1), None
        )
        selected_option2 = next(
            (option2 for option2 in Constants.options_data_price if
             option2['name'] == player.selected_optionprice2), None
        )
        selected_option3 = next(
            (option3 for option3 in Constants.options_data_price if
             option3['name'] == player.selected_optionprice3), None
        )
        selected_option4 = next(
            (option4 for option4 in Constants.options_data_price if
             option4['name'] == player.selected_optionprice4), None
        )
        selected_option5 = next(
            (option5 for option5 in Constants.options_data_price if
             option5['name'] == player.selected_optionprice5), None
        )

        # Lakukan drawing angka 1-100
        if selected_option1:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option1['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_price1 = outcome
                    player.endowment -= 25
                    break

        if selected_option2:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option2['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_price2 = outcome
                    player.endowment -= 25
                    break

        if selected_option3:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option3['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_price3 = outcome
                    player.endowment -= 25
                    break

        if selected_option4:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option4['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_price4 = outcome
                    player.endowment -= 25
                    break

        if selected_option5:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option5['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_price5 = outcome
                    player.endowment -= 25
                    break

    @staticmethod
    def error_message(player: Player, values):
        selected_options = [
            values['selected_optionprice1'],
            values['selected_optionprice2'],
            values['selected_optionprice3'],
            values['selected_optionprice4'],
            values['selected_optionprice5']
        ]
        selected_count = sum(1 for option in selected_options if option)
        total_cost = selected_count * 25

        # Pesan kesalahan untuk biaya lebih besar dari endowment
        error_msgs = []
        if total_cost > player.endowment:
            error_msgs.append(
                f"Endowment Anda tidak mencukupi untuk membeli {selected_count} opsi (Total biaya: {total_cost}).")

        # Pesan kesalahan jika tidak ada opsi yang dipilih
        if not (values['selected_optionprice1'] or values['selected_optionprice2'] or values['selected_optionprice3'] or
                values['selected_optionprice4'] or values['selected_optionprice5']):
            error_msgs.append('Anda harus memilih setidaknya satu opsi.')

        # Jika ada pesan kesalahan, gabungkan dan kembalikan
        if error_msgs:
            return "<br>".join(error_msgs)
        return ""

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Iya"
        return player.offer_accepted is not None and player.offer_accepted


class PriceResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'result1': player.result_price1,
            'result2': player.result_price2,
            'result3': player.result_price3,
            'result4': player.result_price4,
            'result5': player.result_price5
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.endowment += player.result_price1 + player.result_price2 +\
                            player.result_price3 + player.result_price4 +\
                            player.result_price5


class RiskyOption_Allocation(Page):
    form_model = 'player'
    form_fields = ['selected_optionallocation1', 'allocation_invest1', 'selected_optionallocation2',
                   'allocation_invest2', 'selected_optionallocation2', 'selected_optionallocation3',
                   'allocation_invest3', 'selected_optionallocation4', 'allocation_invest4',
                   'selected_optionallocation5', 'allocation_invest5']

    @staticmethod
    def vars_for_template(player: Player):
        # Mendapatkan pilihan acak (contoh daftar pilihan opsi)
        random_options1 = random.sample(Constants.options_data_allocation, 1)
        random_options2 = random.sample(Constants.options_data_allocation, 1)
        random_options3 = random.sample(Constants.options_data_allocation, 1)
        random_options4 = random.sample(Constants.options_data_allocation, 1)
        random_options5 = random.sample(Constants.options_data_allocation, 1)

        # Membuat teks yang terstruktur untuk setiap opsi dalam format list items
        for i, option1 in enumerate(random_options1):
            option_outcomes = option1['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option1['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option2 in enumerate(random_options2):
            option_outcomes = option2['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option2['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option3 in enumerate(random_options3):
            option_outcomes = option3['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option3['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option4 in enumerate(random_options4):
            option_outcomes = option4['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option4['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        for i, option5 in enumerate(random_options5):
            option_outcomes = option5['outcomes']
            formatted_outcomes = []
            for j, (value, probability) in enumerate(option_outcomes):
                formatted_outcomes.append(f"Anda mendapatkan x{value} dengan peluang {int(probability * 100)}%")
            option5['formatted_outcomes'] = formatted_outcomes  # List of outcomes for each option

        return {
            'random_options1': random_options1,
            'random_options2': random_options2,
            'random_options3': random_options3,
            'random_options4': random_options4,
            'random_options5': random_options5,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Temukan opsi yang dipilih pemain berdasarkan nama
        selected_option1 = next(
            (option1 for option1 in Constants.options_data_allocation if
             option1['name'] == player.selected_optionallocation1), None
        )
        selected_option2 = next(
            (option2 for option2 in Constants.options_data_allocation if
             option2['name'] == player.selected_optionallocation2), None
        )
        selected_option3 = next(
            (option3 for option3 in Constants.options_data_allocation if
             option3['name'] == player.selected_optionallocation3), None
        )
        selected_option4 = next(
            (option4 for option4 in Constants.options_data_allocation if
             option4['name'] == player.selected_optionallocation4), None
        )
        selected_option5 = next(
            (option5 for option5 in Constants.options_data_allocation if
             option5['name'] == player.selected_optionallocation5), None
        )

        # Lakukan drawing angka 1-100
        if selected_option1:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option1['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_allocation1 = outcome
                    player.endowment -= player.allocation_invest1
                    break

        if selected_option2:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option2['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_allocation2 = outcome
                    player.endowment -= player.allocation_invest2
                    break

        if selected_option3:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option3['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_allocation3 = outcome
                    player.endowment -= player.allocation_invest3
                    break

        if selected_option4:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option4['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_allocation4 = outcome
                    player.endowment -= player.allocation_invest4
                    break

        if selected_option5:
            draw = random.randint(1, 100)

            # Hitung hasil berdasarkan peluang
            cumulative_probability = 0
            for outcome, probability in selected_option5['outcomes']:
                cumulative_probability += probability * 100
                if draw <= cumulative_probability:
                    player.result_allocation5 = outcome
                    player.endowment -= player.allocation_invest5
                    break

    @staticmethod
    def error_message(player: Player, values):
        total_allocation = (values['allocation_invest1'] + values['allocation_invest2'] + values['allocation_invest3'] +
                            values['allocation_invest4'] + values['allocation_invest5'])

        if total_allocation > player.endowment:
            return f"Endowment Anda tidak mencukupi untuk membeli opsi-opsi tersebut" \
                   f" (Total alokasi: {total_allocation})."
        return ""

    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Iya"
        return player.offer_accepted is not None and player.offer_accepted


class AllocationResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'allocation1': player.allocation_invest1,
            'result1': player.result_allocation1,
            'profit1': player.allocation_invest1 * player.result_allocation1,
            'allocation2': player.allocation_invest2,
            'result2': player.result_allocation2,
            'profit2': player.allocation_invest2 * player.result_allocation2,
            'allocation3': player.allocation_invest3,
            'result3': player.result_allocation3,
            'profit3': player.allocation_invest3 * player.result_allocation3,
            'allocation4': player.allocation_invest4,
            'result4': player.result_allocation4,
            'profit4': player.allocation_invest4 * player.result_allocation4,
            'allocation5': player.allocation_invest5,
            'result5': player.result_allocation5,
            'profit5': player.allocation_invest5 * player.result_allocation5,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.endowment += (player.allocation_invest1 * player.result_allocation1) + \
                            (player.allocation_invest2 * player.result_allocation2) + \
                            (player.allocation_invest3 * player.result_allocation3) + \
                            (player.allocation_invest4 * player.result_allocation4) + \
                            (player.allocation_invest5 * player.result_allocation5)

class Confirmation_Cognitive_Task(Page):
    form_model = 'player'
    form_fields = ['offer_accepted']


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


    @staticmethod
    def is_displayed(player: Player):
        # Hanya tampilkan halaman ini jika pemain memilih "Iya"
        return player.offer_accepted is not None and player.offer_accepted


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


class CognitiveTask(Page):
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
    @staticmethod
    def vars_for_template(player: Player):
        # Data yang digunakan untuk tabel Return dan Pr of Winning
        return_values = [1.15, 1.2, 1.25, 1.35, 1.45, 1.55, 1.67, 1.85, 2, 2.25, 2.5, 2.9, 3.4, 4, 5, 7, 10]
        pr_of_winning_values = [0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1]

        # Menggabungkan return_values dan pr_of_winning_values menjadi satu list pasangan
        options = list(zip(return_values, pr_of_winning_values))

        return {
            'options': options,
        }


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
                 AllocationResults, Confirmation_Cognitive_Task, Buytime, CognitiveTask, Game3_Results, Game4, Results]
