'''
Tela para cadastrar um novo usuário
'''

import sqlite3
import tkinter as tk

import tela_principal

from datetime import datetime
from tkinter import messagebox


# Só um administrador pode fazer o cadastro de um novo usuário
class Cadastro_user:
    def __init__(self, root):
        self.root = root
        self.root.title('Cadastrar Usuário')
        self.root.iconbitmap('Logo-Uniaves_2020.ico')
        self.root.resizable(width=False, height=False)

        self.frame_login = tk.Frame(self.root)
        self.frame_login.pack(fill='x')
        self.entrada_login = tk.Entry(self.frame_login, font=('Calibri', 12))
        self.entrada_login.pack(side='right', padx=10, pady=5)
        self.label_login = tk.Label(self.frame_login, text='Login:', font=('Arial', 12, 'bold'))
        self.label_login.pack(side='right')
        
        self.frame_senha = tk.Frame(self.root)
        self.frame_senha.pack(fill='x')
        self.entrada_senha = tk.Entry(self.frame_senha, font=('Calibri', 12), show='*')
        self.entrada_senha.pack(side='right', padx=10, pady=5)
        self.label_senha = tk.Label(self.frame_senha, text='Senha:', font=('Arial', 12, 'bold'))
        self.label_senha.pack(side='right')

        self.frame_confirmsenha = tk.Frame(self.root)
        self.frame_confirmsenha.pack(fill='x')
        self.entrada_confirmsenha = tk.Entry(self.frame_confirmsenha, font=('Calibri', 12), show='*')
        self.entrada_confirmsenha.pack(side='right', padx=10, pady=5)
        self.label_confirmsenha = tk.Label(self.frame_confirmsenha, text='Confirmar Senha:', font=('Arial', 12, 'bold'))
        self.label_confirmsenha.pack(side='right')

        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack()
        self.botao_logar = tk.Button(self.frame_botoes, text='CADASTRAR', command=self.cadastrar, bg='#99FF99', font=('Arial', 12, 'bold'))
        self.botao_logar.pack(side='right', padx=10, pady=10)
        self.botao_sair = tk.Button(self.frame_botoes, text='SAIR', command=self.root.destroy, bg='#FF9999', font=('Arial', 12, 'bold'))
        self.botao_sair.pack(side='left', padx=10, ipadx=10)

        self.frame_adicional = tk.Frame(self.root)
        self.frame_adicional.pack(fill='x')
        self.var = tk.IntVar()
        self.check_admin = tk.Checkbutton(self.frame_adicional, text='Admin?', variable=self.var)
        self.check_admin.pack(side='left')

    def conecta_db(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS usuarios (login TEXT, senha TEXT, tipo TEXT, UNIQUE(login))')
        return con, cur

    def cadastrar(self):
        con, cur = self.conecta_db()
        self.login = self.entrada_login.get().upper()
        self.senha = self.entrada_senha.get()
        self.confirmsenha = self.entrada_confirmsenha.get()
        if self.senha == self.confirmsenha:
            if self.var.get() == 1:
                self.tipo = 'ADMIN'
            else:
                self.tipo = 'USUARIO'
            
            if self.login != '' and self.senha != '':
                import hashlib
                self.senha = hashlib.md5(bytes(str(self.senha), encoding='utf-8')).hexdigest()
                try:
                    cur.execute('INSERT INTO usuarios VALUES (?, ?, ?)',(self.login, self.senha, self.tipo))
                    con.commit()
                    self.entrada_login.delete(0, 'end')
                    self.entrada_senha.delete(0, 'end')
                    self.entrada_confirmsenha.delete(0, 'end')
                except (sqlite3.IntegrityError, sqlite3.OperationalError) as SQL_Error:
                    messagebox.showerror('Erro de Login', 'Usuário já cadastrado')
                con.close()
            else:
                con.close()
            


        else:

            messagebox.showerror('Erro de Senha', 'As Senhas não são iguais, digite novamente!')

            self.entrada_senha.delete(0, 'end')
            self.entrada_confirmsenha.delete(0, 'end')


def gerar_tela():
    root = tk.Tk()
    app = Cadastro_user(root)
    root.mainloop()

if __name__ == "__main__":
    gerar_tela()
