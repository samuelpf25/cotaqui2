from datetime import datetime

import streamlit as st

import pandas as pd

#funções db
from db import cadastro,contagem,consulta,atualizar,consulta_todos,pesquisando,precos

def main():
    #st.title('CotAqui')
    st.image(r'img/cotaqui.png', width=200)
    menu = ['Orçamento','Cadastrar Cotações','Cadastrar Materiais','Cadastrar Empresas','Consultar',]
    choice = st.sidebar.radio('Menu',menu)

    # PÁGINA DE CONSULTA
    if choice == 'Consultar':
        st.subheader('Consultar materiais')

        #col1,col2=st.beta_columns([3,1])
        #with col1:
        pesquisar=st.text_input(label='Nome do material')
        #with col2:
            #st.config(layout="wide")
            #st.text('')
        botao=st.button('Pesquisar')

        if (botao):
            consultar=pesquisando('materiais','nome',pesquisar)
            df = pd.DataFrame(consultar, columns=['Código', 'Nome', 'Unidade'])
            st.dataframe(df)


    # PÁGINA DE CADASTRO DE MATERIAIS
    elif choice == 'Cadastrar Materiais':
        st.subheader('Cadastrar materiais')
        #st.image(r'img/materiais.jpg', width=300)
        with st.beta_expander('Materiais Cadastrados'):
            todos=consulta_todos('materiais')
            df = pd.DataFrame(todos,columns=['Código','Nome','Unidade'])
            st.dataframe(df)
        nome = st.text_input(label='Nome do Material')
        unidade = st.selectbox('Unidade', ['m²', 'm³', 'kg', 'unid', 'kg/m'])
        if st.button('Cadastrar'):
            #fazer pesquisa para ver se existe
            resultado=consulta('materiais','nome',nome)
            try:
                id = resultado[0][0]
                pesquisa = resultado[0][1]
            except:
                pesquisa=''

            if (pesquisa==nome):
                #se já existe, atualizar
                with st.spinner('Material já existente no banco de dados...atualizando!'):
                    base='materiais'
                    set='nome=?,unidade=?'
                    onde='cod_material'
                    dado=id
                    task=[nome,unidade]
                    atualizar(task, base, set, onde, dado)
                st.success('Dado atualizado!')
            else:
                #se não existe, cadastrar novo
                with st.spinner('Cadastrando novo material...'):
                    n = contagem('materiais')
                    #n=0
                    cod_material=n+1
                    base='materiais(cod_material,nome,unidade)'
                    lista=[cod_material,nome,unidade]
                    cadastro(base,lista)
                st.success('Cadastro efetuado!')


    #PÁGINA DE CADASTRO DE EMPRESAS
    elif choice == 'Cadastrar Empresas':
        st.subheader('Cadastrar empresas')
        #st.image(r'img/empresas.jpg', width=300)
        with st.beta_expander('Empresas Cadastradas'):
            todos = consulta_todos('empresas')
            df = pd.DataFrame(todos, columns=['Código', 'Nome', 'Telefone','Endereço'])
            st.dataframe(df)
        nome = st.text_input(label='Nome da empresa')
        telefone = st.text_input(label='Telefone')
        endereco = st.text_input(label='Endereço')
        if st.button('Cadastrar'):
            # fazer pesquisa para ver se existe
            resultado = consulta('empresas', 'nome', nome)
            try:
                id = resultado[0][0]
                pesquisa = resultado[0][1]
            except:
                pesquisa=''

            if (pesquisa == nome):
                # se já existe, atualizar
                with st.spinner('Empresa já existente no banco de dados...atualizando!'):
                    base = 'empresas'
                    set = 'nome=?,telefone=?,endereco=?'
                    onde = 'cod_empresa'
                    dado = id
                    task = [nome, telefone,endereco]
                    atualizar(task, base, set, onde, dado)
                st.success('Dado atualizado!')
            else:
                # se não existe, cadastrar novo
                with st.spinner('Cadastrando novo material...'):
                    n = contagem('empresas')
                    # n=0
                    cod_empresa = n + 1
                    base='empresas(cod_empresa,nome,telefone,endereco)'
                    lista=[cod_empresa,nome,telefone,endereco]
                    cadastro(base,lista)
                st.success('Cadastro efetuado!')


    #PÁGINA DE CADASTRO DE COTAÇÕES
    elif choice == 'Cadastrar Cotações':
        st.subheader('Cotações')
        #st.image(r'img/cotacao.jpg', width=300)
        #carregando dados
        listar=consulta_todos('materiais')
        lista=[]

        for l in listar:
            lista.append(l[1])

        lista = list(dict.fromkeys(lista)) #removendo valores duplicados
        lista=sorted(lista) #ordenando lista de string

        nome = st.selectbox('Material',lista)

        dado=consulta('materiais','nome',nome)
        cod_material=dado[0][0]
        unidade = dado[0][2]

        listar1=consulta_todos('empresas')
        lista1=[]
        for l in listar1:
            lista1.append(l[1])

        lista1 = list(dict.fromkeys(lista1)) #removendo valores duplicados
        lista1=sorted(lista1) #ordenando lista de string

        empresa = st.selectbox('Empresa',lista1)

        dado=consulta('empresas','nome',empresa)
        cod_empresa=dado[0][0]

        valor=''
        data=datetime.today() #datetime.today()
        #resultado=['','','','']
        resultado = consulta('cotacao', 'cod_material', cod_material + '" and cod_empresa="' + cod_empresa)

        try:
            valor = resultado[0][2]
            data = resultado[0][3]
            print(data)
            d=datetime.strptime(data, '%Y-%m-%d') #, '%y-%m-%d'
            #print(d)
            #d=(d.year,d.month,d.day)
            data=d
            print('Encontrou na consulta!')
        except:
            print('erro')

        #st.text('Unidade: ' + unidade)
        preco=st.text_input('Preço por '+unidade+':',value=valor)

        #data=data.strftime("%d/%m/%Y")
        data = st.date_input('Data da cotação', value=data)
        dados=consulta('cotacao','cod_material',cod_material)
        df = pd.DataFrame(dados, columns=['Material', 'Empresa', 'Preço', 'Data'])

        #ajustando colunas dataframe
        listar=consulta_todos('materiais')
        valores={}
        for l in listar:
            valores[l[0]]=l[1]
        df['Material'] = df['Material'].map(valores)

        listar=consulta_todos('empresas')
        valores = {}
        for l in listar:
            valores[l[0]] = l[1]
        df['Empresa'] = df['Empresa'].map(valores)

        st.dataframe(df)

        if st.button('Cadastrar'):
            # fazer pesquisa para ver se existe
            resultado = consulta('cotacao', 'cod_material', cod_material+'" and cod_empresa="' + cod_empresa)
            try:
                id = resultado[0][0]
                pesquisa = resultado[0][1]
            except:
                pesquisa=''

            if (pesquisa !=''):
                # se já existe, atualizar
                with st.spinner('Cotação já existente no banco de dados...atualizando!'):
                    base = 'cotacao'
                    set = 'preco=?,data=?'
                    onde = 'cod_material'
                    dado = cod_material + '" and cod_empresa = "' + cod_empresa
                    task = [preco, data]
                    atualizar(task, base, set, onde, dado)
                st.success('Dado atualizado!')
            else:
                # se não existe, cadastrar novo
                with st.spinner('Cadastrando novo material...'):
                    base='cotacao(cod_material,cod_empresa,preco,data)'
                    lista=[cod_material,cod_empresa,preco,data]
                    cadastro(base,lista)
                st.success('Cadastro efetuado!')


    #PÁGINA DE ORÇAMENTO
    elif choice == 'Orçamento':
        valores = {'Material':'','Unidade':'','Quantidade':'','Preço Unitário':'','Total':''}
        st.subheader('Orçamento')
        mat = []
        un = []
        qt = []
        pu = []
        pt = []
        #imagee = Image.open(r'/img/orcamento.jpeg')

        #st.image(r'img/orcamento.jpeg',width=300)
        #carregando dados
        listar=consulta_todos('materiais')
        lista=[]

        for l in listar:
            lista.append(l[1])

        lista = list(dict.fromkeys(lista)) #removendo valores duplicados
        lista=sorted(lista) #ordenando lista de string

        material = st.selectbox('Material',lista)

        dado=consulta('materiais','nome',material)
        cod_material=dado[0][0]
        unidade = dado[0][2]

        menor=precos(cod_material,'MIN')
        preco=menor[0][0]
        empresa=menor[0][1]
        data=menor[0][2]
        telefone=''
        endereco=''
        try:
            resultado = consulta('empresas', 'cod_empresa', empresa)
            try:
                empresa = resultado[0][1]
                telefone = resultado[0][2]
                endereco = resultado[0][3]
            except:
                print('erro')

            media = precos(cod_material, 'AVG')

            st.text('Menor preço: ' + str(preco) + ' (média: ' + str(media[0][0])+')')
            st.text('Unidade: ' + str(unidade))
            st.text('Empresa: ' + str(empresa))
            st.text('Telefone: ' + str(telefone))
            st.text('Endereço: ' + str(endereco))
            st.text('Data da cotação: ' + str(data))

            qtd=0.0
            dado=st.text_input('Quantidade: ')
            if (dado!=''):
                qtd=dado
            total=float(qtd)*float(preco)
            st.text('Total: ' + str(total))
        except:
            print('erro1')
        # adicionar=st.button('Adicionar item')
        # if (adicionar):
        #     mat.append(material)
        #     un.append(unidade)
        #     qt.append(qtd)
        #     pu.append(preco)
        #     pt.append(total)
        #
        #     n=0
        #     for m in mat:
        #         valores['Material']=mat[n]
        #         valores['Unidade']=un[n]
        #         valores['Quantidade']=qt[n]
        #         valores['Preço Unitário']=str(pu[n])
        #         valores['Total']=pt[n]
        #         n=n+1
        #
        #     print(valores)
        #     st.text(str(mat))
        #     df = pd.DataFrame(list(valores.items()))
        #     st.dataframe(df)

# def login():
#     menu = ['Login',]
#     choice = st.sidebar.radio('Menu',menu)
#     v = ''
#     if choice=='Login':
#         st.image(r'img/cotaqui.png', width=200)
#         st.text('Login')
#         nome=st.text_input('usuário: ')
#         senha=st.text_input('senha: ', type="password")
#
#         btn=st.button('Entrar')
#         if btn:
#             if (nome=='sam' and senha=='456'):
#                 v='OK'
#                 st.text('Carregando...')
#             else:
#                 st.text('Login inválido!')
#     return v
if __name__ == '__main__':
    #t=login()
    #if t=='OK':
    #    st.empty()
    main()
