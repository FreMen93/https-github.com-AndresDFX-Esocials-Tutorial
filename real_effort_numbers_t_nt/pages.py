from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import *

# ******************************************************************************************************************** #
# *** STAGE 1
# ******************************************************************************************************************** #

class Consent(Page):

    form_model = "player"
    form_fields = ["numero_identificacion", "aceptar_dato"]

    def is_displayed(self):
        return self.round_number == 1
    

class Control1(Page):

    form_model = "player"
    form_fields = ["control_1", "control_2"]

    def is_displayed(self):
        return self.round_number == 1


# ******************************************************************************************************************** #
# *** MANAGEMENT STAGE
# ******************************************************************************************************************** #
stage_1_sequence = [Consent, Control1]
stage_2_sequence = []
stage_3_sequence = []

page_sequence = stage_1_sequence + stage_2_sequence + stage_3_sequence

