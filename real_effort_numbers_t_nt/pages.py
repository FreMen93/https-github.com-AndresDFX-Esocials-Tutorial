from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import *
import random

## De un jugador a una lista de atributos obtiene los valores acutales
def get_data(player, list_atrr):
    values = []
    for attr in list_atrr:
        values.append(getattr(player, attr))
    return values

# De un jugador una lista de atributos y unos valores, cambia esa lista de atributos con los nuevos valores
def set_data(player,list_atrr, values):
    for i,atrr in enumerate(list_atrr):
        setattr(player,atrr,values[i])
        
def get_and_set_data(self_player, player, list_atrr):
    values = get_data(self_player, list_atrr)
    set_data(player, list_atrr, values)
    
def get_and_set_data_one_atrr(self_player, player, list_atrr, round_index, self_atrr):
    atrr = list_atrr[round_index]
    value = getattr(self_player, self_atrr)
    setattr(player, atrr, value)
        




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
    timeout_seconds = 10 #tiempo en segundos
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

    timeout_seconds = 2
    timer_tex = "La siguiente ronda comenzara en "
    
    def is_displayed(self):
        if self.round_number <= Constants.num_sub_rounds_stage_1:
            return self.round_number == self.round_number
        

    def vars_for_template(self):
        player = self.player ## Jugador rona 2,3 o etc
        player_round1 = player.in_round(1) # Jugador en la ronda 1
        opponent = player.other_player()
        
        combined_pay_off_team = player.payment_actual_round + opponent.payment_actual_round
        correct_answers_team = player.correct_answers_actual_round + opponent.correct_answers_actual_round
        get_and_set_data_one_atrr(player, player_round1, Constants.list_attr, self.round_number-1, "correct_answers_actual_round")
        
        return{
            "combined_pay_off_team": combined_pay_off_team,
            "correct_answers_team": correct_answers_team
        }

class CombinedResults(Page):
    
    
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    def vars_for_template(self):
        player_round1 = self.player.in_round(1) #Devuelve mi jugaro en la ronda 1
        me_in_others_rounds = self.player.in_rounds(1, Constants.num_sub_rounds_stage_1) ##Devuelve la lista de mi jugador en las rondas especificas
        
        correct_answers_team = 0
        combined_pay_off_team = 0
        
        for player in me_in_others_rounds: ## [player(ronda1),Player(ronda2), etc]
            opponent = player.other_player()
            combined_pay_off_team = combined_pay_off_team + player.payment_actual_round + opponent.payment_actual_round
            correct_answers_team = correct_answers_team + player.correct_answers_actual_round + opponent.correct_answers_actual_round
            
        ### Para guardar la Data necesaria en la Ronda 1
            
        player_round1.payment_stage_1 = correct_answers_team * Constants.pay_per_correct_answer
        player_round1.correct_answers_stage_1 = correct_answers_team
        combined_pay_off_team = player_round1.payment_stage_1
        
        return {
            "combined_pay_off_team": combined_pay_off_team,
            "correct_answers_team": correct_answers_team
        }

class Stage2Instructions(Page):
    form_model = 'player'
    
    
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    
    
    



# ******************************************************************************************************************** #
# *** MANAGEMENT STAGE
# ******************************************************************************************************************** #
#stage_1_sequence = [Consent, Control1, Stage1Questions]
stage_1_sequence = [Consent, SubstractNumbers, ResultsWaitPage, PartialResults, CombinedResults ]
stage_2_sequence = []
stage_3_sequence = []

page_sequence = stage_1_sequence + stage_2_sequence + stage_3_sequence

