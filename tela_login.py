'''
Tela de autenticação para login do usuário
'''

import sqlite3
import hashlib
import tkinter as tk

import tela_principal

from datetime import datetime
from tkinter import messagebox


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title('Autenticação')
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


        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack()
        self.botao_logar = tk.Button(self.frame_botoes, text='ENTRAR', command=self.logar, bg='#00FF00', font=('Arial', 12, 'bold'))
        self.botao_logar.pack(side='right', padx=10, pady=10)
        self.botao_sair = tk.Button(self.frame_botoes, text='SAIR', command=self.root.destroy, bg='#FF0000', font=('Arial', 12, 'bold'))
        self.botao_sair.pack(side='left', padx=10, ipadx=10)

        self.frame_adicional = tk.Frame(self.root)
        self.frame_adicional.pack(fill='x')
        self.label_criador = tk.Label(self.frame_adicional, text='Criado por: Natan C. Louzada', bg='Gray', fg='white')
        self.label_criador.pack(side='right')

    def conecta_db(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS acessos (login text, data text, hora text, tipo text)')
        return con, cur

    # Os usuários "Admin" possuem privilégios para manutenção do programa
    def logar(self):
        con, cur = self.conecta_db()
        self.login = self.entrada_login.get().strip().upper()
        self.senha = hashlib.md5(bytes(str(self.entrada_senha.get()), encoding='utf-8')).hexdigest()
        self.data = datetime.today().strftime('%d/%m/%Y')
        self.hora = datetime.today().strftime('%H:%M:%S')
        self.usuario = list(cur.execute('SELECT login, senha, tipo FROM usuarios WHERE login = "' + self.login + '"'))
        if self.usuario == []:
            messagebox.showerror('Erro de login', 'Usuário não cadastrado')
        elif self.senha != self.usuario[0][1]:
            messagebox.showerror('Erro de senha', 'Senha incorreta')
        else:
            self.tipo = self.usuario[0][2]

            cur.execute('INSERT INTO acessos VALUES (?, ?, ?, ?)',(self.login, self.data, self.hora, self.tipo))
            con.commit()
            con.close()

            self.root.destroy()
            if self.tipo == 'ADMIN':
                self.tela_admin = tela_principal.Requisicao_admin(tk.Tk())
            else:
                self.tela_usuario = tela_principal.Requisicao_padrao(tk.Tk())


if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()