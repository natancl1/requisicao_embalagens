'''
Exportador de tabelas do banco de dados.
'''


import sqlite3
from tkinter import filedialog

from openpyxl import Workbook



def exportar(nome_tabela):
    con = sqlite3.connect('database.db')
    cur = con.execute('SELECT * FROM ' + nome_tabela)
    cabecalho = tuple(i[0] for i in cur.description)
    dados = list(cur)
    dados.insert(0, cabecalho)
    con.close()
    
    
    wb = Workbook()
    ws = wb.active
    ws.title = nome_tabela
    
    for linha in range(len(dados)):
        for coluna in range(len(dados[linha])):
            ws.cell(row=linha+1, column=coluna+1, value=dados[linha][coluna])

    pasta = filedialog.askdirectory()
    wb.save(pasta + '/' + nome_tabela + '.xlsx')
