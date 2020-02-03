from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):
    def play_round(self):
        yield pages.game3_instructions
        if self.player.role == 'inspector':
            yield pages.Decision2, dict(decision=random('Full_Inspection','Light_Inspection','No_Inspection'))
        else:
            yield pages.Decision2, dict(decision=random('Fully_Comply', 'Partially_Comply', 'Not_Comply'))
        yield pages.Results
        yield pages.FinalResults

        pass
