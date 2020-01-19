from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random

from typing import List, Any

author = 'vouch11'

doc = """
Test 2-by-2 inspector vs. firm game 
"""
p = []  # type: list

class Constants(BaseConstants):
    name_in_url = 'test2by2'
    players_per_group = 2
    num_rounds = 10

    instructions_template = 'test2by2/Instructions.html'

    # firm's points
    firm_IC = c(100)  # comply when inspected
    firm_IN = c(0)  # not comply when inspected
    firm_NC = c(100)  # comply when not inspected
    firm_NN = c(400)  # not comply when not inspected

    # inspector's points
    insp_IC = c(100)  # inspect when comply
    insp_IN = c(300)  # inspect when not comply
    insp_NC = c(400)  # not inspect when comply
    insp_NN = c(0)  # not inspect when not comply


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def set_payoffs(self):
        for p in self.get_players():
            p.set_payoff()

    pass

class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'inspector'
        else:
            return 'firm'

    decision = models.StringField(
        choices=['Inspect', 'Comply','Not_inspect', 'Not_comply'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        payoff_matrix = dict(
            Comply=dict(
                Inspect=Constants.firm_IC,
                Not_inspect=Constants.firm_NC,
            ),
            Not_comply=dict(
                Inspect=Constants.firm_IN, Not_inspect=Constants.firm_NN
            ),
            Inspect = dict(
                Comply = Constants.insp_IC,
                Not_comply = Constants.insp_IN,
            ),
            Not_inspect = dict(
                Comply = Constants.insp_NC,
                Not_comply = Constants.insp_NN,
            ),

        )
        self.payoff = payoff_matrix[self.decision][self.other_player().decision]
        p.append(self.payoff)

    def total_payoff(self):

        temp = random.sample(p,k=5)
        total=sum(temp)
        self.participant.payoff = total
        return total

    pass


