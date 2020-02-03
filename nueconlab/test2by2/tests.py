from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):
    def play_round(self):
        yield pages.Introduction
        yield pages.S2
        yield pages.S3, dict(q1="Yes",q2="Yes",q3="No")
        yield pages.game1_instructions
        if self.player.role =='inspector':
            yield pages.Decision1, dict(decision=random("Inspect","Not_inspect"))
        else:
            yield pages.Decision1, dict(decision=random("Comply","Not_comply"))
        yield pages.Results
        yield pages.FinalResults

        pass
