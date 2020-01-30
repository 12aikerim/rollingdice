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
import random as rand
import numpy as np
author = 'vouch11'

doc = """
Test 3-by-3 inspector vs. firm game 
"""
p = []


class Constants(BaseConstants):
    name_in_url = 'game4'
    players_per_group = 2
    num_rounds = 30
    k = 3  # number of randomly selected rounds

    instructions_template = 'threeBythree/Instructions.html'

    # firm's points
    firm_fully_comply = c(20)  # fully comply (payoff is the same when inspection is full, light or there is not inspection at all

    firm_PF10= c(50)# paritally comply when fully inspected with 10% chance of fine
    firm_PF = c(0)   # paritally comply when fully inspected with 90% chance of fine
    firm_PL = c(50)  # partially comply when lightly inspected
    firm_PN = c(50)  # partially comply when not inspected

    firm_NF = c(10)  # not comply when fully inspected
    firm_NL = c(10)  # not comply when lightly inspected with 10% chance of fine
    firm_NL10 = c(60) #not comply when lightly inspected with 90% chance of fine
    firm_NN = c(60)  # not comply when not inspected

    # inspector's points
    insp_FI = c(20)  # full inspection when fully comply
    insp_FL = c(50)  # light inspection when fully comply
    insp_FN = c(60)  # not inspect when when fully comply

    insp_PF = c(20)  # full inspection when paritally comply
    insp_PF10 = c(-30)  # full inspection when paritally comply with 10% chance
    insp_PL = c(0)  # light inspection when paritally comply
    insp_PN = c(10)  # not inspect when paritally comply

    insp_NF = c(20)  # full inspection when not comply
    insp_NL = c(50)  # light inspection when not comply with 90% chance of fine
    insp_NF10 = c(0) # light inspection when not comply with 10% chance of fine
    insp_NN = c(10)  # not inspect when not comply


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly(fixed_id_in_group=True)

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
        x=c(np.random.choice([50,0],1,p=[0.1,0.9]).item(0))
        y=c(np.random.choice([60,10],1,p=[0.1,0.9]).item(0))
        payoff_matrix = dict(
            Fully_Comply=dict(
                Full_Inspection=Constants.firm_fully_comply,
                Light_Inspection=Constants.firm_fully_comply,
                No_Inspection = Constants.firm_fully_comply,
            ),
            Partially_Comply=dict(
                Full_Inspection=x,
                Light_Inspection=Constants.firm_PL,
                No_Inspection=Constants.firm_PN,
            ),
            Not_Comply=dict(
                Full_Inspection=Constants.firm_NF,
                Light_Inspection=y,
                No_Inspection=Constants.firm_NN,
            ),
            Full_Inspection = dict(
                Fully_Comply = Constants.insp_FI,
                Partially_Comply = c(-30 if x==c(50) else 20),
                Not_Comply = Constants.insp_NF,
            ),
            Light_Inspection=dict(
                Fully_Comply=Constants.insp_FL,
                Partially_Comply=Constants.insp_PL,
                Not_Comply=c(50 if y ==c(10) else 0),
            ),
            No_Inspection=dict(
                Fully_Comply=Constants.insp_NF,
                Partially_Comply=Constants.insp_PN,
                Not_Comply=Constants.insp_NN,
            ),
        )
        self.payoff = payoff_matrix[self.decision][self.other_player().decision]

    def payments_per_round(self):
        # get list of all players for each participant
        players = self.in_all_rounds()
        print(players)
        payments = [p.payoff for p in players]
        print("new payments var: ", payments)
        return payments

    def total_payoff(self):

        listOfPayments = [p.payoff for p in self.in_all_rounds()]
        temp = rand.sample(listOfPayments, Constants.k)
        total = sum(temp)
        self.participant.vars['lump'].append(total)
        self.participant.payoff = sum(self.participant.vars['lump'])

        return dict(
            list_of_all_payments=listOfPayments,
            round_earning=total,
            random_payments=temp, )
    pass

