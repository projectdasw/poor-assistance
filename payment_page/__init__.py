from otree.api import *
import random


doc = """
Payment Page
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment_page'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pembayaran_akhir = models.CurrencyField(initial=0)
    sesi_terpilih = models.StringField()
    pembayaran_terpilih = models.CurrencyField(initial=0)
    # total_endowment_risky_purchase = models.CurrencyField()
    # total_endowment_risky_allocation = models.CurrencyField()
    # total_endowment_cognitive_task = models.CurrencyField()
    # total_endowment_panel_allocation = models.CurrencyField()


# PAGES
class info_sesi(Page):
    @staticmethod
    def vars_for_template(player):
        participant = player.participant

        # risky_purchase = participant.vars["summary_risky_purchase"]
        # risky_allocation = participant.vars["summary_risky_allocation"]
        # cognitive_task = participant.vars["summary_cognitive_task"]
        # panel_allocation = participant.vars["summary_panel_allocation"]

        # player.total_endowment_risky_purchase = risky_purchase["endowment"]
        # player.total_endowment_risky_allocation = risky_allocation["endowment"]
        # player.total_endowment_cognitive_task = cognitive_task["endowment"]
        # player.total_endowment_panel_allocation = panel_allocation["endowment"]

        return dict(
            risky_purchase=participant.vars.get("results_risky_purchase", []),
            risky_purchase_summary=participant.vars.get("summary_risky_purchase", {}),
            risky_allocation=participant.vars.get("results_risky_allocation", []),
            risky_allocation_summary=participant.vars.get("summary_risky_allocation", {}),
            cognitive_task=participant.vars.get("results_cognitive_task", []),
            cognitive_task_summary=participant.vars.get("summary_cognitive_task", {}),
            panel_allocation=participant.vars.get("results_panel_allocation", []),
            panel_allocation_summary=participant.vars.get("summary_panel_allocation", {}),
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant

        apps = [
            ("Risky Purchase", participant.vars.get("summary_risky_purchase")),
            ("Risky Allocation", participant.vars.get("summary_risky_allocation")),
            ("Investment Panel Allocation", participant.vars.get("summary_panel_allocation")),
            ("Cognitive Task", participant.vars.get("summary_cognitive_task")),
        ]

        selected_app, summary = random.choice(apps)
        player.sesi_terpilih = selected_app
        player.pembayaran_terpilih = summary["endowment"]
        player.pembayaran_akhir = (player.pembayaran_terpilih * 100) + 10000


class pembayaran(Page):
    pass


class akhir_eksperimen(Page):
    pass


page_sequence = [info_sesi, pembayaran]
