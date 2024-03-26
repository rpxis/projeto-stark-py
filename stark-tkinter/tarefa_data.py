import pymysql.cursors
from tarefa_model import Tarefa

class TarefaData:
    def __init__(self):
        self.conexao = pymysql.connect(host='localhost',
                                       user='root',
                                       password='',
                                       database='stark',
                                       cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conexao.cursor()

    def insert(self, tarefa: Tarefa):
        try:
            sql = "INSERT INTO tarefas (nome, descricao, status_tarefa, dt_inicio, dt_terminio) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (tarefa.nome, tarefa.descricao, tarefa.status, tarefa.data_inicio, tarefa.data_terminio))
            self.conexao.commit()

        except Exception as error:
            print(f'Erro ao adicionar! Error: {error}')

    def update(self, tarefa: Tarefa):
        try:
            sql = "UPDATE tarefas SET nome = %s, descricao = %s, status_tarefa = %s, dt_inicio = %s, dt_terminio = %s WHERE tarefa_id = %s"
            self.cursor.execute(sql, (tarefa.nome, tarefa.descricao, tarefa.status, tarefa.data_inicio, tarefa.data_terminio, tarefa.id))
            self.conexao.commit()

        except Exception as error:
            print(f'Erro ao editar! Error: {error}')

    def delete(self, id_tarefa: str):
        try:
            sql = "DELETE FROM tarefas WHERE tarefa_id = %s"
            self.cursor.execute(sql, id_tarefa)
            self.conexao.commit()

        except Exception as error:
            print(f'Erro ao deletar! Error: {error}')

    def select(self):
        try:
            sql = "SELECT * FROM tarefas"
            self.cursor.execute(sql)
            tarefas = self.cursor.fetchall()
            return tarefas
        except Exception as error:
            print(f"Erro ao listar! Error: {error}")

if __name__ == "__main__":
    aluno = TarefaData()