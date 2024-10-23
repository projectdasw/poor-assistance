from otree.api import *
import random
from pathlib import Path

doc = """
Multiplayer word search game
"""


def load_word_list():
    # words from https://github.com/dovenokan/oxford-words
    return set(Path(__name__ + '/words.txt').read_text().split())


class Constants(BaseConstants):
    name_in_url = 'practice_experiment'
    players_per_group = None
    num_rounds = 1  # 10 periods
    initial_endowment = 100
    additional_endowment = 30
    deduction = 50
    dim = 5
    num_squares = dim * dim
    lexicon = load_word_list()

    COORDS = []

    for x in range(dim):
        for y in range(dim):
            COORDS.append((x, y))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    board = models.LongStringField()


class Player(BasePlayer):
    endowment = models.IntegerField(initial=0)
    option_price = models.IntegerField(initial=0, label='Jumlah yang ingin di investasikan')
    option_allocation = models.IntegerField(initial=0, label='Jumlah yang ingin di alokasi')
    score = models.IntegerField(initial=0)


class FoundWord(ExtraModel):
    word = models.StringField()
    player = models.Link(Player)
    group = models.Link(Group)


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


class Game1(Page):
    pass
    # form_model = 'player'
    # form_fields = ['option_price']


class Game2(Page):
    pass


class Confirmation_Cognitive_Task(Page):
    pass


class Buytime(Page):
    pass


# COGNITIVE TASK DEVOPS
def word_in_board(word, board):
    lengths = list(range(1, len(word) + 1))
    paths = {_: [] for _ in lengths}

    for i in range(Constants.dim):
        for j in range(Constants.dim):
            coord = (i, j)
            if board[coord] == word[0]:
                paths[1].append([coord])

    for length in lengths[1:]:
        target_char = word[length - 1]
        for path in paths[length - 1]:
            cur_x, cur_y = path[-1]
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    check_coord = (cur_x + dx, cur_y + dy)
                    if (
                        check_coord in Constants.COORDS
                        and board[check_coord] == target_char
                        and check_coord not in path
                    ):
                        paths[length].append(path + [check_coord])
    return bool(paths[len(word)])


def load_board(board_str):
    return dict(zip(Constants.COORDS, board_str.replace('\n', '').lower()))


class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        rows = []
        for _ in range(Constants.dim):
            # add extra vowels
            row = ''.join(
                [random.choice('AAABCDEEEEEFGHIIKLMNNOOPRRSTTUUVWXYZ') for _ in range(Constants.dim)]
            )
            rows.append(row)
        group.board = '\n'.join(rows)


def live_method(player: Player, data):
    group = player.group
    board = group.board

    if 'word' in data:
        word = data['word'].lower()
        is_in_board = len(word) >= 3 and word_in_board(word, load_board(board))
        is_in_lexicon = is_in_board and word.lower() in Constants.lexicon
        is_valid = is_in_board and is_in_lexicon
        already_found = is_valid and bool(FoundWord.filter(group=group, word=word))
        success = is_valid and not already_found
        news = dict(
            word=word,
            success=success,
            is_in_board=is_in_board,
            is_in_lexicon=is_in_lexicon,
            already_found=already_found,
            id_in_group=player.id_in_group,
        )
        if success:
            FoundWord.create(group=group, word=word)
            player.score += 2
    else:
        news = {}
    scores = [[p.id_in_group, p.score] for p in group.get_players()]
    found_words = [fw.word for fw in FoundWord.filter(group=group)]
    return {0: dict(news=news, scores=scores, found_words=found_words)}


class Game3(Page):
    live_method = live_method
    timeout_seconds = 30

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(board=group.board.upper().split('\n'))

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)


class Game3_Results(Page):
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

    @staticmethod
    def vars_for_template(player: Player):
        player.payoff = player.endowment


page_sequence = [Intro, Game1, Game2, Confirmation_Cognitive_Task, Buytime, WaitToStart, Game3, Game3_Results, Game4,
                 Results]
