
class SaudacaoService:

    def saudar(self, newmember, leftmember):

        if newmember == 'jjarvis_bot' or newmember == 'garçom_b3':
            return

        if newmember != None and len(newmember) > 0:
            return 'Bem vindo(a) ' + newmember + ', que os deuses do Trade lhe tragam muitos GAINSSS!'
        
        if leftmember != None and len(leftmember) > 0:
            return 'Adeus ' + leftmember + ', Uma pena você ter saído!!! Espero que não tenha quebrado a conta!!!'

        return