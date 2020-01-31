from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Group

class Introduction(Page):
    def is_displayed (self):
        return self.round_number == 1



class S2(Page):
    def is_displayed (self):
        return self.round_number == 1



class S3(Page) :
    def is_displayed (self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['q1','q2','q3']


class Answers(Page) :
    def is_displayed(self):
        return self.round_number == 1


class game1_instructions(Page):
    def is_displayed (self):
        return self.round_number == 1

class Decision1(Page):
    form_model = 'player'
    form_fields = ['decision']

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def wait_for_all_groups(self):
        self.wait_for_all_groups = True


class RandomizePlayers(WaitPage):
    def is_displayed(self):
        return self.round_number!=Constants.num_rounds
    body_text = "Matching you with the new player..."
    def wait_for_all_groups(self):
        self.wait_for_all_groups = True
    pass

class Results(Page):

    def vars_for_template(self):
        me = self.player
        opponent = me.other_player()

        return dict(
            my_decision=me.decision,
            opponent_decision=opponent.decision,

        )

    pass


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return self.player.total_payoff()

    pass


page_sequence = [Introduction,S2,S3,Answers,game1_instructions,Decision1,
                 ResultsWaitPage,Results,FinalResults]
