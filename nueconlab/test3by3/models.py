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
author = 'vouch11'

doc = """
Test 3-by-3 inspector vs. firm game 
"""
p = []


class Constants(BaseConstants):
    name_in_url = 'test3by3'
    players_per_group = 2
    num_rounds = 2

    instructions_template = 'test3by3/Instructions.html'

    # firm's points
    firm_fully_comply = c(100)  # fully comply (payoff is the same when inspection is full, light or there is not inspection at all

    firm_PF = c(50)  # paritally comply when fully inspected
    firm_PL = c(200) # partially comply when lightly inspected
    firm_PN = c(300) # partially comply when not inspected

    firm_NF = c(0)  # not comply when fully inspected
    firm_NL = c(100)  # not comply when lightly inspected
    firm_NN = c(400)  # not comply when not inspected

    # inspector's points
    insp_FI = c(100)  # full inspection when fully comply
    insp_FL = c(200)  # light inspection when fully comply
    insp_FN = c(400)  # not inspect when when fully comply

    insp_PF = c(300)  # full inspection when paritally comply
    insp_PL = c(50)  # light inspection when paritally comply
    insp_PN = c(200)  # not inspect when paritally comply

    insp_NF = c(200)  # full inspection when not comply
    insp_NL = c(300)  # light inspection when not comply
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
        choices=['Full_Inspection','Light_Inspection','No_Inspection', 'Fully_Comply','Partially_Comply','Not_Comply'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        payoff_matrix = dict(
            Fully_Comply=dict(
                Full_Inspection=Constants.firm_fully_comply,
                Light_Inspection=Constants.firm_fully_comply,
                No_Inspection = Constants.firm_fully_comply,
            ),
            Partially_Comply=dict(
                Full_Inspection=Constants.firm_PF,
                Light_Inspection=Constants.firm_PL,
                No_Inspection=Constants.firm_PN,
            ),
            Not_Comply=dict(
                Full_Inspection=Constants.firm_NF,
                Light_Inspection=Constants.firm_NL,
                No_Inspection=Constants.firm_NN,
            ),
            Full_Inspection = dict(
                Fully_Comply = Constants.insp_FI,
                Partially_Comply = Constants.insp_PF,
                Not_Comply = Constants.insp_NF,
            ),
            Light_Inspection=dict(
                Fully_Comply=Constants.insp_FL,
                Partially_Comply=Constants.insp_PL,
                Not_Comply=Constants.insp_NL,
            ),
            No_Inspection=dict(
                Fully_Comply=Constants.insp_NF,
                Partially_Comply=Constants.insp_PN,
                Not_Comply=Constants.insp_NN,
            ),
        )
        self.payoff = payoff_matrix[self.decision][self.other_player().decision]
        p.append(self.payoff)

    def total_payoff(self):

        temp = random.sample(p, k=5)
        total = sum(temp)
        self.participant.payoff = total
        return total

    pass

