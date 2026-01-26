from datetime import date

class Avaliacao:
    def __init__(self, id_crianca, peso, altura, data_avaliacao=None):
        self.id_crianca = id_crianca
        self.peso = float(peso)
        self.altura = float(altura)
        self.data_avaliacao = data_avaliacao or date.today().strftime("%d/%m/%Y")
        self.imc = self.calcular_imc()

    def calcular_imc(self):
        if self.altura <=0:
            raise ValueError("Altura deve ser maior que zero")
        
        return round(self.peso/(self.altura ** 2), 2)