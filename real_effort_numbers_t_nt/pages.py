from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import *
import random

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


class Stage1Questions(Page):
    
    form_model = "player"

    def is_displayed(self):
        return self.round_number == 1


class SubstractNumbers(Page):

    form_model = "player"
    timeout_seconds = 60 #tiempo en segundos
    timer_text = "Tiempo restante para completar la ronda: "

    def is_displayed(self):
        if self.round_number <= Constants.num_sub_rounds_stage_1:
            return self.round_number == self.round_number
 

    def vars_for_template(self): ###Funcion para mostrar variables que no se almacenan en la BD
        ###Este se ejecuta al cargar la pagina
        number1 = random.randint(1, 50)
        number2 = random.randint(number1, 99)

        return {
            "number_1": number1,
            "number_2": number2,
            "correct_answers": self.player.correct_answers_actual_round,
            "total_answers": self.player.total_substract_actual_round,
            "wrong_answers": self.player.wrong_substract_actual_round,
            "payment_actual": self.player.payment_actual_round
        }

        #number 2 - number 1
    
    def live_method(self, data): #Interaccion en vivo sin pasar de pagina
        ##Recibir la respuesta: 1 si es correcta y 0 sino es correcta y generar dos numeros nuevos
        number1 = random.randint(1, 50)
        number2 = random.randint(number1, 99)
        correct_answer = int(data) #es 0 o 1; esto llega desde el html
        #Actualizar la informacion que se muestra en cada ronda
        self.correct_answers_actual_round = self.correct_answers_actual_round + correct_answer
        self.total_substract_actual_round = self.total_substract_actual_round + 1
        self.wrong_substract_actual_round = self.total_substract_actual_round - self.correct_answers_actual_round
        self.payment_actual_round =  self.payment_actual_round + (self.correct_answers_actual_round * Constants.pay_per_correct_answer)

        response = dict(
            number_1=number1,
            number_2=number2,
            correct_answers=self.correct_answers_actual_round,
            total_answers=self.total_substract_actual_round,
            wrong_answers=self.wrong_substract_actual_round,
            payment_actual=self.payment_actual_round
        )
        return{
            self.id_in_group: response #self.id_in_group hace referencia al id unico del jugador en el grupo (sea 1 o 2)
        }



class ResultsWaitPage(WaitPage):
    
    def is_displayed(self):
        if self.round_number <= Constants.num_sub_rounds_stage_1:
            return self.round_number == self.round_number



class PartialResults(Page):

    timeout_seconds = 10
    timer_tex = "La siguiente ronda comenzara en "
    
    def is_displayed(self):
        if self.round_number <= Constants.num_sub_rounds_stage_1:
            return self.round_number == self.round_number
        

    def vars_for_template(self):
        player = self.player
        opponent = player.other_player()
        
        combined_payoff_team = player.payment_actual_round + opponent.payment_actual_round
        correct_answers_team = player.correct_answers_actual_round + opponent.correct_answers_actual_round
        
        return{
            "combined_payoff_team": combined_payoff_team,
            "correct_answers_team": correct_answers_team
        }

# ******************************************************************************************************************** #
# *** MANAGEMENT STAGE
# ******************************************************************************************************************** #
#stage_1_sequence = [Consent, Control1, Stage1Questions]
stage_1_sequence = [Consent, SubstractNumbers, ResultsWaitPage, PartialResults]
stage_2_sequence = []
stage_3_sequence = []

page_sequence = stage_1_sequence + stage_2_sequence + stage_3_sequence

