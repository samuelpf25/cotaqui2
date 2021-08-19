import mysql.connector
import streamlit as st

#with mysql.connector.connect(user='ur4cz0bal9a1nwkk',password='s09ygCIVSwJ25ydgMIet', host='bwdczptcydolxiwwho4y-mysql.services.clever-cloud.com', port=3306,database='bwdczptcydolxiwwho4y') as conn:
    #with mysql.connector.connect(user='ur4cz0bal9a1nwkk',password='s09ygCIVSwJ25ydgMIet', host='bwdczptcydolxiwwho4y-mysql.services.clever-cloud.com', port=3306,database='bwdczptcydolxiwwho4y').cursor() as c:

#conn = mysql.connector.connect(user='ur4cz0bal9a1nwkk', password='s09ygCIVSwJ25ydgMIet',host='bwdczptcydolxiwwho4y-mysql.services.clever-cloud.com', port=3306,database='bwdczptcydolxiwwho4y')
#c = conn.cursor()

def carregar():
    #conn=sqlite3.connect('consulta.db')
    #user='id17287557_samuelpf25', password='#Sa747400027816', host='localhost:3306', database='id17287557_consulta'
    #host="localhost",user="root",password="",database="consulta_mysql"
    #user='296184',password='747400', host='cotaqui.orgfree.com', port=3306,database='296184'
    conn=mysql.connector.connect(user=st.secrets["user"],password=st.secrets["password"], host=st.secrets["host"], port=3306,database=st.secrets["database"])
    c=conn.cursor()
    #c.execute("CREATE TABLE cotacao (cod_material TEXT, cod_empresa TEXT, preco TEXT, data TEXT)")
    #c.execute("CREATE TABLE empresas (cod_empresa TEXT, nome TEXT, telefone TEXT, endereco TEXT)")
    #c.execute("CREATE TABLE materiais (cod_material TEXT, nome TEXT, unidade TEXT)")
    return conn,c

def cadastro(base,lista):
    conn,c=carregar()
    #base=materiais(cod_material,nome,unidade)
    #complemento=(?,?,?)
    caract=base.count(',')
    value='%s'
    for i in range(caract):
        value=value+',%s'

    c.execute('INSERT INTO '+base+' VALUES ('+value+')',lista)
    conn.commit()
    conn.close()

def contagem(tabela):
    conn, c = carregar()
    print('SELECT * FROM ' + tabela)
    c.execute('SELECT * FROM ' + tabela)
    n1 = len(c.fetchall())
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
    sql = 'UPDATE '+ base + ' SET ' + set + ' WHERE ' + onde + ' = ' + dado + ''
    print(sql)
    c.execute(sql, task)
    conn.commit()
    conn.close()

def precos(cod_material,var):
    conn, c = carregar()
    sql = 'SELECT '+var+'(CAST(preco as REAL)),cod_empresa,data FROM cotacao WHERE cod_material = "' + cod_material + '"'
    menor = c.execute(sql)
    try:
        menor=c.fetchall() #a
        print(str(menor))
    except:
        menor=''
    conn.close()
    return menor

def deleta_dado(tabela,onde,dado):
    conn,c = carregar()
    dado=(str(dado),)
    sql='DELETE FROM '+tabela+' WHERE '+onde+' = %s' #' + dado + ''
    print(sql)
    c.execute(sql,dado) #,(dado,)
    conn.commit()
    conn.close()
