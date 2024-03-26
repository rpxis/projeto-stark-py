import datetime

class Tarefa:
    def __init__(self, nome, descricao, status):

        self.nome = nome
        self.descricao = descricao
        self.data_inicio = None
        self.data_terminio = None
        self.status = status
        if status == 'Em andamento':
            self.data_inicio = datetime.datetime.now()
        elif status == 'Concluído':
             self.data_terminio = datetime.datetime.now()
        

    
        
    def __repr__(self):
        return (f"Id: {self.id} \n"
                f"Nome: {self.nome} \n"
                f"Descrição: {self.descricao} \n"
                f"Data: {self.data_inicio} \n"
                f"Status: {self.status}")


if __name__ == "__main__":
    print("[ERRO] Este arquivo é um modúlo")
