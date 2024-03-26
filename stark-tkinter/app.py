import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tarefa_model import Tarefa
from tarefa_data import TarefaData
import datetime

class App:
    def __init__(self):
        self.db = TarefaData()

        self.janela = tk.Tk()
        self.janela.title('Stark Industries')

        # Label
        self.label_id = tk.Label(self.janela, text="Id",
                                     font="Tahoma 14 bold", fg="red")
        self.label_id.grid(row=0, column=0)

        # Entry
        self.txt_id = tk.Entry(self.janela, font="Tahoma 14",
                                   width=27, state=tk.DISABLED)
        self.txt_id.grid(row=0, column=1)

        # Label
        self.label_nome = tk.Label(self.janela, text="Nome",
                                font="Tahoma 14 bold", fg="red")
        self.label_nome.grid(row=1, column=0)

        # Entry
        self.txt_nome = tk.Entry(self.janela, font="Tahoma 14",
                              width=27)
        self.txt_nome.grid(row=1, column=1)

        # Label
        self.label_descricao = tk.Label(self.janela, text="Descrição",
                                 font="Tahoma 14 bold", fg="red")
        self.label_descricao.grid(row=2, column=0)

        # Entry
        self.txt_descricao = tk.Entry(self.janela, font="Tahoma 14",
                               width=27)
        self.txt_descricao.grid(row=2, column=1)

        # Label
        self.label_status = tk.Label(self.janela, text="Status",
                                 font="Tahoma 14 bold", fg="red")
        self.label_status.grid(row=3, column=0)

        self.status = ['A fazer', 'Em andamento', 'Concluído']
        self.cb_status = ttk.Combobox(self.janela, values=self.status, width=28,
                                      font="Tahoma 12")
        self.cb_status.grid(row=3, column=1)
        self.cb_status.set('A fazer')
        self.cb_status['state'] = 'disabled'


        # botões
        self.button_adicionar = tk.Button(self.janela, font="Tahoma 12 bold", width=7,
                                       text="Adicionar", fg="red",
                                       command=self.adicionarTarefa)
        self.button_adicionar.grid(row=5, column=0)

        self.button_editar = tk.Button(self.janela, font="Tahoma 12 bold", width=7,
                                    text="Editar", fg="red",
                                    command=self.editarTarefa)
        self.button_editar.grid(row=5, column=1)

        # botões
        self.button_deletar = tk.Button(self.janela, font="Tahoma 12 bold", width=7,
                                     text="Deletar", fg="red",
                                     command=self.deletarTarefa)
        self.button_deletar.grid(row=5, column=2)

        # frame
        self.frame = tk.Frame(self.janela)
        self.frame.grid(row=6, column=0, columnspan=3)

        self.colunas = ['ID' ,'Nome', 'Descrição', 'Status', 'Data-início', 'Data-términio']
        self.tabela = ttk.Treeview(self.frame, columns=self.colunas, show='headings')
        for coluna in self.colunas:
            self.tabela.heading(coluna, text=coluna)
        self.tabela.pack()
        self.tabela.bind('<ButtonRelease-1>', self.selecionarTarefa)

        self.atualizarTabela()
        self.janela.mainloop()

    def limparCampos(self):
        self.txt_id.config(state=tk.NORMAL)
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state=tk.DISABLED)
        self.txt_nome.delete(0, tk.END)
        self.txt_descricao.delete(0, tk.END)
        self.cb_status.set("")
        



    def selecionarTarefa(self, event):
        if 'A fazer' in self.cb_status['values']:
            self.status.remove("A fazer")
            self.cb_status['values'] = self.status
            
        self.cb_status['state'] = 'normal'
        
        linha_selecionada = self.tabela.selection()[0]
        item = self.tabela.item(linha_selecionada)['values']
        self.limparCampos()
        self.txt_id.config(state=tk.NORMAL)
        self.txt_id.insert(0, item[0])
        self.txt_id.config(state=tk.DISABLED)
        self.txt_nome.insert(0, item[1])
        self.txt_descricao.insert(0, item[2])
        self.cb_status.set(item[3])
      

    def atualizarTabela(self):
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        tarefas = self.db.select()
        for tarefa in tarefas:
            if tarefa['dt_inicio'] == None:
                tarefa_inicio = 'Não iniciado' 
            else:
                tarefa_inicio = tarefa['dt_inicio']
            if tarefa['dt_terminio'] == None:
                tarefa_terminio = '-'
            else:
                tarefa_terminio = tarefa['dt_terminio']
            self.tabela.insert("", tk.END, values=(tarefa['tarefa_id'],
                                                        tarefa['nome'],
                                                        tarefa['descricao'],
                                                        tarefa['status_tarefa'],
                                                        tarefa_inicio,
                                                        tarefa_terminio))
    
    def criarTarefa(self):
        nome = self.txt_nome.get()
        descricao = self.txt_descricao.get()
        status = self.cb_status.get()
        return Tarefa(nome, descricao, status)

    def adicionarTarefa(self):
        tarefa = self.criarTarefa()
        self.db.insert(tarefa)
        self.limparCampos()
        self.atualizarTabela()
        self.cb_status.set('A fazer')
        messagebox.showinfo("Sucesso!", "Tarefa adicionada com sucesso!")

    def checkStatus(self, tarefa, status, inicio):
        if status == 'A fazer':
            tarefa.data_inicio = datetime.datetime.now()
            return
        if status == 'Em andamento':
            tarefa.data_inicio = inicio
            tarefa.data_terminio = datetime.datetime.now()
            return
    
    def editarTarefa(self):
        tarefa = self.criarTarefa()
        tarefa.id = self.txt_id.get()
        status = self.tabela.item(self.tabela.selection()[0])['values'][3]
        inicio = self.tabela.item(self.tabela.selection()[0])['values'][4]
        self.checkStatus(tarefa, status, inicio)
        
        opcao = messagebox.askyesno("Tem certeza?","Deseja alterar os dados?")
        if opcao:
            self.db.update(tarefa)
            self.limparCampos()
            self.atualizarTabela()
            messagebox.showinfo("Sucesso!", "Tarefa alterada com sucesso!")
            
            if 'A fazer' not in self.cb_status['values']:
                self.status.insert(0, "A fazer")
                self.cb_status['values'] = self.status
                self.cb_status.set('A fazer')
                self.cb_status['state'] = 'disabled'


    def deletarTarefa(self):
        id = self.txt_id.get()
        opcao = messagebox.askyesno("Tem certeza?","Deseja remover a tarefa?")
        if opcao:
            self.db.delete(id)
            self.limparCampos()
            self.atualizarTabela()
            messagebox.showinfo("Sucesso", "Tarefa removida com sucesso!")
    
if __name__ == "__main__":
    App()