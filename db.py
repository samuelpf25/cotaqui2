import sqlite3

#with sqlite3.connect('consulta.db') as conn, conn.cursor() as c:
def carregar():
    conn=sqlite3.connect('consulta.db')
    c=conn.cursor()
    return conn,c

def cadastro(base,lista):
    conn,c=carregar()
    #base=materiais(cod_material,nome,unidade)
    #complemento=(?,?,?)
    caract=base.count(',')
    value='?'
    for i in range(caract):
        value=value+',?'

    c.execute('INSERT INTO '+base+' VALUES ('+value+')',lista)
    conn.commit()
    conn.close()
    
def contagem(tabela):
    conn, c = carregar()
    print('SELECT * FROM ' + tabela)
    cur=c.execute('SELECT * FROM ' + tabela)
    n1 = len(cur.fetchall())
    conn.close()
    return n1

def consulta(tabela,onde,dado):
    conn, c = carregar()
    c.execute('SELECT * FROM ' + tabela + ' WHERE ' + onde + ' = "' + dado + '"')
    data = c.fetchall()
    conn.close()
    return data

def consulta_todos(tabela):
    conn, c = carregar()
    c.execute('SELECT * FROM ' + tabela)
    data = c.fetchall()
    conn.close()
    return data

"""def consulta_cotacao(tabela,onde,dado):
    conn, c = carregar()
    c.execute('SELECT * FROM ' + tabela + ' WHERE ' + onde + ' = "' + dado + '"')
    data = c.fetchall()
    return data
"""
def pesquisando(tabela,onde,dado):
    conn, c = carregar()
    c.execute('SELECT * FROM ' + tabela + ' WHERE ' + onde + ' LIKE "%' + dado + '%"')
    data = c.fetchall()
    conn.close()
    return data

def atualizar(task,base,set,onde,dado):
    #set cod_material =?,nome=?,unidade=?
    conn, c = carregar()
    sql = 'UPDATE '+ base + ' SET ' + set + ' WHERE ' + onde + ' = "' + dado + '"'
    print(sql)
    c.execute(sql, task)
    conn.commit()
    conn.close()

def precos(cod_material,var):
    conn, c = carregar()
    sql = 'SELECT '+var+'(CAST(preco as REAL)),cod_empresa,data FROM cotacao WHERE cod_material = "' + cod_material + '"'
    menor = c.execute(sql)
    menor=menor.fetchall() #a
    print(str(menor))
    conn.close()
    return menor

