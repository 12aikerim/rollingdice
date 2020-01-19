from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Group


class Introduction(Page):
    def is_displayed (self):
        return self.round_number == 1
    timeout_seconds = 100

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()
    pass

class Results(Page):

 def vars_for_template(self):
    me = self.player
    opponent = me.other_player()

    return dict (
        my_decision=me.decision,
        opponent_decision = opponent.decision,
    )
    pass

class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    pass

page_sequence = [Introduction, Decision, ResultsWaitPage, Results,FinalResults]
