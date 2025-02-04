

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from click import style

def criar_banco():
    conn = sqlite3.connect('ajustes_laminador.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ajustes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aco_atual TEXT NOT NULL,
            proximo_aco TEXT NOT NULL,
            bitola TEXT NOT NULL,
            observacao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def open_criar_ajuste(root):

    criar_window = tk.Toplevel(root)
    criar_window.title("Criar Ajuste")
    criar_window.geometry("400x300")
    

    # colunas da janela para que elas possam expandir 
    # igualmente. Isso é feito usando o método columnconfigure
    #Aqui, weight=1 faz com que ambas as colunas se expandam igualmente.

    criar_window.columnconfigure(0, weight=1)
    criar_window.columnconfigure(1, weight=1)

    #Titulo da pagina
    tk.Label(criar_window, text="Adicionar novo Ajuste", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    #Estilo dos nomes
    label_font = ("Helvetica", 10, "bold")

    tk.Label(criar_window, text="Aço Atual", font=label_font).grid(row=1, column=0, sticky="e", padx=10, pady=10)
    aco_atual_entry = tk.Entry(criar_window)
    aco_atual_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    tk.Label(criar_window, text="Próximo Aço", font=label_font).grid(row=2, column=0, sticky="e", padx=10, pady=10)
    proximo_aco_entry = tk.Entry(criar_window)
    proximo_aco_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    tk.Label(criar_window, text="Bitola", font=label_font).grid(row=3, column=0, sticky="e", padx=10, pady=10)
    bitola_entry = tk.Entry(criar_window)
    bitola_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

    tk.Label(criar_window, text="Observação", font=label_font).grid(row=4, column=0, sticky="e", padx=10, pady=10)

    # Caixa de texto para "Observação"
    observacao_entry = tk.Text(criar_window, height=5, width=30)
    observacao_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')

    def salvar_ajuste():
        aco_atual = aco_atual_entry.get()
        proximo_aco = proximo_aco_entry.get()
        bitola = bitola_entry.get()
        observacao = observacao_entry.get()
        observacao = observacao_entry.get("1.0", tk.END)  # Corrigido aqui


        conn = sqlite3.connect('ajustes_laminador.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ajustes (aco_atual, proximo_aco, bitola, observacao)
            VALUES (?, ?, ?, ?)
        ''', (aco_atual, proximo_aco, bitola, observacao))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Ajuste criado com sucesso!")
        criar_window.destroy()

    tk.Button(criar_window, text="Salvar", command=salvar_ajuste).grid(row=12, column=0, columnspan=2,  padx=10, pady=10)

def open_listar_ajustes(root):
    listar_window = tk.Toplevel(root)
    listar_window.title("Listar Ajustes")

    columns = ("Aço Atual", "Próximo Aço", "Bitola", "Observação", "Editar", "Excluir")
    tree = ttk.Treeview(listar_window, columns=columns, show="headings")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    

    col_widths = {
        "Aço Atual": 100,
        "Próximo Aço": 100,
        "Bitola": 80,
        "Observação": 250,
        "Editar": 50,
        "Excluir": 50
    }
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=col_widths[col])


    carregar_ajustes(tree, listar_window)

def carregar_ajustes(tree, root):
    for i in tree.get_children():
        tree.delete(i)
    
    conn = sqlite3.connect('ajustes_laminador.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, aco_atual, proximo_aco, bitola, observacao FROM ajustes")
    ajustes = cursor.fetchall()
    conn.close()

    

    for ajuste in ajustes:
        id, aco_atual, proximo_aco, bitola, observacao = ajuste
        tree.insert("", tk.END, text=id, values=(aco_atual, proximo_aco, bitola, observacao, "Editar", "Excluir"))

        # Aplicando tags apenas às colunas "Editar" e "Excluir"
        

    tree.bind("<Double-1>", lambda e: acao_ajuste(tree, e, root))

def acao_ajuste(tree, event, root):
    item = tree.selection()[0]
    id_ajuste = tree.item(item, "text")
    
    col = tree.identify_column(event.x)
    if col == "#5":  # Coluna de editar
        open_editar_ajuste(id_ajuste, root, tree)
    elif col == "#6":  # Coluna de excluir
        confirmar_exclusao(id_ajuste, root, tree)

def open_editar_ajuste(id_ajuste, root, tree):
    editar_window = tk.Toplevel(root)
    editar_window.title("Editar Ajuste")
    editar_window.geometry("400x240")
    

    # colunas da janela para que elas possam expandir 
    # igualmente. Isso é feito usando o método columnconfigure
    #Aqui, weight=1 faz com que ambas as colunas se expandam igualmente.

    editar_window.columnconfigure(0, weight=1)
    editar_window.columnconfigure(1, weight=1)

    conn = sqlite3.connect('ajustes_laminador.db')
    cursor = conn.cursor()
    cursor.execute("SELECT aco_atual, proximo_aco, bitola, observacao FROM ajustes WHERE id=?", (id_ajuste,))
    ajuste = cursor.fetchone()
    conn.close()

    aco_atual, proximo_aco, bitola, observacao = ajuste

    tk.Label(editar_window, text="Aço Atual").grid(row=0, column=0,pady=5)
    aco_atual_entry = tk.Entry(editar_window)
    aco_atual_entry.grid(row=0, column=1)
    aco_atual_entry.insert(0, aco_atual)

    tk.Label(editar_window, text="Próximo Aço").grid(row=1, column=0,pady=5)
    proximo_aco_entry = tk.Entry(editar_window)
    proximo_aco_entry.grid(row=1, column=1)
    proximo_aco_entry.insert(0, proximo_aco)

    tk.Label(editar_window, text="Bitola").grid(row=2, column=0,pady=5)
    bitola_entry = tk.Entry(editar_window)
    bitola_entry.grid(row=2, column=1)
    bitola_entry.insert(0, bitola)


    tk.Label(editar_window, text="Observação").grid(row=3, column=0, pady=5)
    observacao_entry = tk.Text(editar_window, height=6, width=38)  # Aumentei o tamanho da box
    observacao_entry.grid(row=3, column=1, pady=5)
    observacao_entry.insert("1.0", observacao)  # Inserir o texto inicial na Text box

    def salvar_alteracoes():
        novo_aco_atual = aco_atual_entry.get()
        novo_proximo_aco = proximo_aco_entry.get()
        nova_bitola = bitola_entry.get()
        nova_observacao = observacao_entry.get("1.0", tk.END)

        conn = sqlite3.connect('ajustes_laminador.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE ajustes
            SET aco_atual=?, proximo_aco=?, bitola=?, observacao=?
            WHERE id=?
        """, (novo_aco_atual, novo_proximo_aco, nova_bitola, nova_observacao, id_ajuste))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Ajuste atualizado com sucesso!")
        editar_window.destroy()
        carregar_ajustes(tree, root)

    tk.Button(editar_window, text="Salvar", command=salvar_alteracoes).grid(row=4, column=0, columnspan=2)

def confirmar_exclusao(id_ajuste, root, tree):
    resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este ajuste?")
    if resposta:
        excluir_ajuste(id_ajuste, root, tree)

def excluir_ajuste(id_ajuste, root, tree):
    conn = sqlite3.connect('ajustes_laminador.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ajustes WHERE id=?", (id_ajuste,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Ajuste excluído com sucesso!")
    carregar_ajustes(tree, root)

def open_consultar_ajuste(root):
    consulta_window = tk.Toplevel(root)
    consulta_window.title("Consultar Ajuste")
    consulta_window.geometry("400x370")


    # Configurar colunas para expandirem igualmente
    consulta_window.columnconfigure(0, weight=1)
    consulta_window.columnconfigure(1, weight=1)

    label_font = ("Helvetica", 10, "bold")

    # Título da página
    tk.Label(consulta_window, text="Consulta de Ajustes", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(consulta_window, text="Aço Atual:", font=label_font).grid(row=1, column=0, pady=10, sticky="e")
    entry_aco_atual = ttk.Combobox(consulta_window)
    entry_aco_atual.grid(row=1, column=1, pady=5, sticky="w")

    tk.Label(consulta_window, text="Próximo Aço:", font=label_font).grid(row=2, column=0, pady=10, sticky="e")
    entry_proximo_aco = ttk.Combobox(consulta_window)
    entry_proximo_aco.grid(row=2, column=1, pady=5, sticky="w")

    tk.Label(consulta_window, text="Bitola:",font=label_font).grid(row=3, column=0, pady=10, sticky="e")
    entry_bitola = ttk.Combobox(consulta_window)
    entry_bitola.grid(row=3, column=1, pady=5, sticky="w")


    btn_consultar = ttk.Button(consulta_window, text="Consultar", command=lambda: consultar_ajustes(entry_aco_atual.get(), entry_proximo_aco.get(), entry_bitola.get(), consulta_window, resultado_label, ajuste_label))
    btn_consultar.grid(row=4, column=0, columnspan=2, pady=10)

    resultado_label = tk.Label(consulta_window, text="", font=("Helvetica", 12))
    resultado_label.grid(row=5, column=0, columnspan=2, pady=10)

    ajuste_label = tk.Label(consulta_window, text="", font=("Helvetica", 12, "bold"))
    ajuste_label.grid(row=6, column=0, columnspan=2, pady=10)



    carregar_opcoes_combobox(entry_aco_atual, entry_proximo_aco, entry_bitola)

def carregar_opcoes_combobox(entry_aco_atual, entry_proximo_aco, entry_bitola):
    conn = sqlite3.connect('ajustes_laminador.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT aco_atual FROM ajustes")
    aco_atuals = [row[0] for row in cursor.fetchall()]
    entry_aco_atual['values'] = aco_atuals

    cursor.execute("SELECT DISTINCT proximo_aco FROM ajustes")
    proximo_acos = [row[0] for row in cursor.fetchall()]
    entry_proximo_aco['values'] = proximo_acos

    cursor.execute("SELECT DISTINCT bitola FROM ajustes")
    bitolas = [row[0] for row in cursor.fetchall()]
    entry_bitola['values'] = bitolas

    conn.close()

def consultar_ajustes(aco_atual, proximo_aco, bitola, consulta_window, resultado_label, ajuste_label):

    conn = sqlite3.connect('ajustes_laminador.db')
    cursor = conn.cursor()

    query = '''
    SELECT observacao FROM ajustes 
    WHERE aco_atual = ? AND proximo_aco = ? AND bitola = ?
    '''
    cursor.execute(query, (aco_atual, proximo_aco, bitola))
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        # Exibir o ajuste encontrado nos Labels
        observacao = resultado[0]
        resultado_label.config(text="Ajuste Recomendado", font=("Helvetica", 14, "bold"))
        ajuste_label.config(text=f"{observacao}", font=("Helvetica", 12))
    else:
        # Perguntar se deseja adicionar um novo ajuste
        resposta = messagebox.askyesno("Nenhum Ajuste Encontrado", "Nenhum ajuste encontrado para os critérios fornecidos. Deseja adicionar um novo ajuste?")
        if resposta:
            open_adicionar_ajuste(consulta_window)

def open_adicionar_ajuste(parent_window):

    label_font = ("Helvetica", 10, "bold")

    adicionar_window = tk.Toplevel(parent_window)
    adicionar_window.title("Adicionar Ajuste")
    adicionar_window.geometry('300x370')


    tk.Label(adicionar_window, text="Aço Atual:",font=label_font).pack(pady=5)
    entry_aco_atual = tk.Entry(adicionar_window)
    entry_aco_atual.pack(pady=5)

    tk.Label(adicionar_window, text="Próximo Aço:", font=label_font).pack(pady=5)
    entry_proximo_aco = tk.Entry(adicionar_window)
    entry_proximo_aco.pack(pady=5)

    tk.Label(adicionar_window, text="Bitola:", font=label_font).pack(pady=5)
    entry_bitola = tk.Entry(adicionar_window)
    entry_bitola.pack(pady=5)

    tk.Label(adicionar_window, text="Observação:", font=label_font).pack(pady=5)
    entry_observacao = tk.Text(adicionar_window, height=5, width=30)
    entry_observacao.pack(pady=5)

    btn_salvar = ttk.Button(adicionar_window, text="Salvar Ajuste", command=lambda: salvar_ajuste(entry_aco_atual.get(), entry_proximo_aco.get(), entry_bitola.get(), entry_observacao.get("1.0", tk.END)))
    btn_salvar.pack(pady=10)

def salvar_ajuste(aco_atual, proximo_aco, bitola, observacao):
    conn = sqlite3.connect('ajustes_laminador.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO ajustes (aco_atual, proximo_aco, bitola, observacao) 
    VALUES (?, ?, ?, ?)
    ''', (aco_atual, proximo_aco, bitola, observacao))

    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Ajuste adicionado com sucesso")


def main():
    root = tk.Tk()
    root.title("Sistema de Ajuste de Laminador")
    root.geometry('500x400')

    # Ajustar tamanho da tela
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Configurar a grade para expandir
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    

        # Cria um estilo para o botão
    style = ttk.Style()
    style.configure('Custom.TButton', font=("Helvetica", 10, 'bold'))

    # Aplica o estilo ao botão

    title_label = ttk.Label(main_frame, text="Controle de Ajuste", font=("Oswald", 16,'bold'))
    title_label.grid(row=0, column=0, pady=10)

    btn_ajuste = ttk.Button(main_frame, text="Adicionar Ajuste de Laminador", command=lambda: open_adicionar_ajuste(root), style='Custom.TButton')
    btn_ajuste.grid(row=1, column=0, pady=5, padx=10, ipadx=10, ipady=10)

    btn_consultar = ttk.Button(main_frame, text="Consultar Ajustes", command=lambda: open_consultar_ajuste(root),style='Custom.TButton')
    btn_consultar.grid(row=2, column=0, pady=5, padx=10, ipadx=10, ipady=10)

    btn_listar_ajustes = ttk.Button(main_frame, text="Listar Ajustes", command=lambda: open_listar_ajustes(root),style='Custom.TButton')
    btn_listar_ajustes.grid(row=3, column=0, padx=5, pady=5, ipadx=10, ipady=10)

    btn_sair = ttk.Button(main_frame, text="Sair", command=root.quit, style='Custom.TButton')
    btn_sair.grid(row=4, column=0, pady=20, ipadx=10, ipady=10)

    root.mainloop()

if __name__ == "__main__":
    criar_banco()
    main()