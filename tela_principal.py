'''
Tela inicial do programa onde o usuário irá fazer a solicitação das embalagens.
'''

import tkinter as tk

from datetime import datetime

import atualiza_base_requisicoes
import tela_cadastro_usuario
import exportar_tabela


# Janela padrão para solicitação por usuário que não é administrador.
class Requisicao_padrao:
    def __init__(self, root):
        self.root = root
        self.root.title('Requisição de Embalagens')
        self.root.iconbitmap('Logo-Uniaves_2020.ico')
        self.root.resizable(width=False, height=False)

        self.frame_titulo_cod = tk.Frame(self.root)
        self.frame_titulo_cod.pack(fill='x')
        self.label_titulo = tk.Label(self.frame_titulo_cod, text='REQUISIÇÃO DE EMBALAGENS', font=('Arial', 20, 'bold'))
        self.label_titulo.pack()
        self.info_img = tk.PhotoImage(file='informacao.png').subsample(5,5)
        self.botao_info = tk.Button(self.frame_titulo_cod, image=self.info_img, command=self.info)
        self.botao_info.pack(pady=5)
        self.entrada_codigo = tk.Entry(self.frame_titulo_cod, font=('Calibri', 20))
        self.entrada_codigo.pack(side='right', padx=10)
        self.label_codigo = tk.Label(self.frame_titulo_cod, text='CÓDIGO', font=('Arial', 14))
        self.label_codigo.pack(side='right')
        

        self.frame_quantidade = tk.Frame(self.root)
        self.frame_quantidade.pack(fill='x')
        self.entrada_quantidade = tk.Entry(self.frame_quantidade, font=('Calibri', 20))
        self.entrada_quantidade.pack(side='right', padx=10)
        self.label_quantidade = tk.Label(self.frame_quantidade, text='QUANTIDADE', font=('Arial', 14))
        self.label_quantidade.pack(side='right')

        self.frame_lote = tk.Frame(self.root)
        self.frame_lote.pack(fill='x')
        self.entrada_lote = tk.Entry(self.frame_lote, font=('Calibri', 20))
        self.entrada_lote.pack(side='right', padx=10)
        self.label_lote = tk.Label(self.frame_lote, text='LOTE', font=('Arial', 14))
        self.label_lote.pack(side='right')


        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack()
        self.botao_imprime = tk.Button(self.frame_botoes, text='IMPRIMIR', command=self.imprimir, bg='#68FF01', font=('Arial', 14, 'bold'))
        self.botao_imprime.pack(side='right', padx=10, pady=10)
        self.botao_sair = tk.Button(self.frame_botoes, text='SAIR', command=self.root.destroy, bg='#FC7404', font=('Arial', 14, 'bold'))
        self.botao_sair.pack(side='left', padx=10, ipadx=10)

    def info(self):
        if not any(isinstance(x, tk.Toplevel) for x in self.root.winfo_children()):
            self.cod_embalagem = self.entrada_codigo.get().strip().upper()
            self.qtd_solicitada = 0 if self.entrada_quantidade.get() == '' else float(self.entrada_quantidade.get())
            self.data = datetime.today().strftime('%d/%m/%Y')
            self.informacoes = atualiza_base_requisicoes.get_info(self.cod_embalagem, self.qtd_solicitada, self.data)

            self.janela_dados = tk.Toplevel(self.root)
            self.janela_dados.iconbitmap('informacao.ico')
            self.janela_dados.title('Situação Atual')
            self.janela_dados.resizable(width=False, height=False)

            self.label_descricao = tk.Label(self.janela_dados, text='DESCRIÇÃO=> ' + self.informacoes[0], font=('Calibri', 11, 'bold'))
            self.label_descricao.pack()
            self.label_status = tk.Label(self.janela_dados, text='STATUS=> ' + self.informacoes[1], font=('Calibri', 11, 'bold'))
            self.label_status.pack()
            self.label_programado = tk.Label(self.janela_dados, text='PROGRAMADO=> ' + str(round(self.informacoes[2], 2)), font=('Calibri', 11, 'bold'))
            self.label_programado.pack()
            self.label_realizado = tk.Label(self.janela_dados, text='REALIZADO=> ' + str(self.informacoes[3]), font=('Calibri', 11, 'bold'))
            self.label_realizado.pack()
            self.label_saldo = tk.Label(self.janela_dados, text='SALDO=> ' + str(round(self.informacoes[4], 2)), font=('Calibri', 11, 'bold'))
            self.label_saldo.pack()
            self.label_percconsumo = tk.Label(self.janela_dados, text='% CONSUMO=> ' + str(round(self.informacoes[5]*100, 2)) + '%', font=('Calibri', 11, 'bold'))
            self.label_percconsumo.pack()

    def imprimir(self):
        self.cod_embalagem = self.entrada_codigo.get().strip().upper()
        self.qtd_solicitada = 0 if self.entrada_quantidade.get() == '' else float(self.entrada_quantidade.get())
        self.lote = self.entrada_lote.get()
        import sqlite3
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.requisitante = list(self.cur.execute('SELECT login FROM acessos'))[-1][0]
        atualiza_base_requisicoes.fim_requisicao(self.cod_embalagem, self.qtd_solicitada, self.lote, self.requisitante)
        self.entrada_codigo.delete(0, 'end')
        self.entrada_quantidade.delete(0, 'end')
        self.entrada_lote.delete(0, 'end')



# Janela do administrador
class Requisicao_admin(Requisicao_padrao):
    def __init__(self, root):
        super().__init__(root)
        self.frame_config = tk.Frame(self.root)
        self.frame_config.pack(fill='x')
        self.config_img = tk.PhotoImage(file='configuracao.png').subsample(15,15)
        self.botao_config = tk.Button(self.frame_config, image=self.config_img, command=self.configurar)
        self.botao_config.pack(side='left')
    
    def cadastrar_usuario(self):
        if not any(isinstance(x, tk.Toplevel) for x in self.janela_config.winfo_children()):
            self.janela_cadastro = tk.Toplevel(self.janela_config)
            app = tela_cadastro_usuario.Cadastro_user(self.janela_cadastro)

    def importar_ficha(self):
        import importar_ficha_tecnica

    def importar_prog(self):
        import importar_programacao
    
    def exportar_acessos(self):
        exportar_tabela.exportar('acessos')

    def exportar_ficha(self):
        exportar_tabela.exportar('ficha_tecnica')

    def exportar_programacao(self):
        exportar_tabela.exportar('programacao')

    def exportar_requisicoes(self):
        exportar_tabela.exportar('requisicoes')

    def exportar_usuarios(self):
        exportar_tabela.exportar('usuarios')

    def configurar(self):
        if not any(isinstance(x, tk.Toplevel) for x in self.root.winfo_children()):
            self.janela_config = tk.Toplevel(self.root)
            self.janela_config.iconbitmap('Logo-Uniaves_2020.ico')
            self.janela_config.title('Manutenção')
            self.janela_config.resizable(width=False, height=False)
            
            self.botao_cadastrar_usuario = tk.Button(self.janela_config, text='CADASTRAR USUÁRIO', command=self.cadastrar_usuario)
            self.botao_cadastrar_usuario.pack()
            self.botao_importar_ficha = tk.Button(self.janela_config, text='IMPORTAR FICHA TÉCNICA', command=self.importar_ficha)
            self.botao_importar_ficha.pack()
            self.botao_importar_programacao = tk.Button(self.janela_config, text='IMPORTAR PROGRAMAÇÃO DE PRODUÇÃO', command=self.importar_prog)
            self.botao_importar_programacao.pack()
            
            self.botao_exportar_acessos = tk.Button(self.janela_config, text='EXPORTAR TABELA ACESSOS', command=self.exportar_acessos)
            self.botao_exportar_acessos.pack()
            self.botao_exportar_ficha = tk.Button(self.janela_config, text='EXPORTAR TABELA FICHA TÉCNICA', command=self.exportar_ficha)
            self.botao_exportar_ficha.pack()
            self.botao_exportar_programacao = tk.Button(self.janela_config, text='EXPORTAR TABELA PROGRAMAÇÃO PRODUÇÃO', command=self.exportar_programacao)
            self.botao_exportar_programacao.pack()
            self.botao_exportar_requisicoes = tk.Button(self.janela_config, text='EXPORTAR TABELA REQUISIÇÕES', command=self.exportar_requisicoes)
            self.botao_exportar_requisicoes.pack()
            self.botao_exportar_usuarios = tk.Button(self.janela_config, text='EXPORTAR TABELA USUÁRIOS', command=self.exportar_usuarios)
            self.botao_exportar_usuarios.pack()


if __name__ == "__main__":
    escolha = input('Padrão ou Admin? ').upper()
    if escolha == 'PADRAO' or escolha == 'PADRÃO':
        root = tk.Tk()
        app = Requisicao_padrao(root)
    else:
        root = tk.Tk()
        app = Requisicao_admin(root)
    root.mainloop()