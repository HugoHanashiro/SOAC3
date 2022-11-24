# coding: utf-8
from time import sleep

# Váriaveis ambiente
#AMBIENTE_PRODUCAO = True
#AMBIENTE_PRODUCAO = False


def main():
    import hashlib
    bdsql_server, mycursor_server, bdsql_mysql, mycursor_mysql  = conectar()

    email = input("Email: ")
    senha = input("Senha: ")

    senha = hashlib.sha512(senha.encode()).hexdigest()

    query = ("SELECT emailUsuario, senhaUsuario, idTorre FROM vw_iniciarSessao WHERE emailUsuario = %s AND senhaUsuario = %s")

    params = (email, senha)

    mycursor_server.execute(query, params)

    resposta = mycursor_server.fetchall()

    if(len(resposta) > 0):
        print("Logado com sucesso!")
        sleep(2)

        selecionarServidor(resposta[0][2])
    else:
        print("Usuario não cadastrado, mande seu gestor cadastrar!")
        sleep(3)


def selecionarServidor(torre):
    from getmac import get_mac_address as mac

    bdsql_server, mycursor_server, bdsql_mysql, mycursor_mysql = conectar()
    
    query = ('SELECT * FROM servidor WHERE idServidor = %s')

    params = (mac(), )
    mycursor_server.execute(query, params)

    resposta = mycursor_server.fetchall()

    if(len(resposta) > 0):
        selecionarParametro(mac())
    else :
        cadastrarServidor(bdsql_server, mycursor_server, mac(), torre)

def cadastrarServidor(bdsql, cursor, mac, torre):
    print("Cadastrando servidor...")

    query = ("INSERT INTO servidor(idServidor, fkTorre) VALUES (%s, %s)")
    
    params = (mac, torre, )
    cursor.execute(query, params)

    bdsql.commit()
    sleep(2)
    print(f'Servidor cadastrado com sucesso!\n MAC: {mac}\n Torre: {torre}')
    selecionarParametro(mac)

def selecionarParametro(mac):
    bdsql_server, mycursor_server, bdsql_mysql, mycursor_mysql = conectar()
        
    query = ("SELECT * from parametro WHERE fkComponente_fkServidor = %s")

    params = (mac, )
    mycursor_server.execute(query, params)

    resposta = mycursor_server.fetchall()

    if(len(resposta) > 0):
        executarMonitoramento(resposta, mac, len(resposta))
    else:
        print("Nenhuma componente cadastrado para monitoramento, cadastre na sua dashboard!")
        sleep(3)
        selecionarParametro(mac)

def executarMonitoramento(resposta, mac, qtdParametros):
    print("Executando monitoramento...")
    isWorking = True
    while isWorking:
        script = """
import threading   
        """

        i=1
        for row in resposta:
            script += f"""
def executar_{i}(servidor, componente, metrica):
    import psutil
    from time import sleep

    bdsql_server, cursor_server, bdmysql, cursor_mysql = conectar()

    query1 = ("SELECT comando, isTupla FROM metrica WHERE idMetrica = %s")
    
    val = (metrica, )

    cursor_server.execute(query1, val) 

    resposta = cursor_server.fetchall() # resposta retorna isto [(comando, isTupla)]
    isTupla = resposta[0][1]

    comando = resposta[0][0] 
    leitura = eval(comando)

    if isTupla == 0:
        query = ("INSERT INTO leitura(fkMetrica, horario, valorLido, fkComponente_idComponente, fkComponente_fkServidor) VALUES(%s, DATEADD(HOUR, -3, GETDATE()), %s, %s, %s)")
        
        sleep(2)

        query2 = ("INSERT INTO leitura(fkMetrica, horario, valorLido, fkComponente_idComponente, fkComponente_fkServidor) VALUES(%s, now(), %s, %s, %s)")
            
        val = (metrica, leitura, componente, servidor, )
            
        cursor_server.execute(query, val)
        sleep(2)
        cursor_mysql.execute(query2, val)
        bdsql_server.commit()
        print(cursor_server.rowcount, "inseriu?")
        sleep(2)
        bdmysql.commit()

    else: 
        for row in leitura:
            query = ("INSERT INTO leitura(fkMetrica, horario, valorLido, fkComponente_idComponente, fkComponente_fkServidor) VALUES(%s, DATEADD(HOUR, -3, GETDATE()), %s, %s, %s)")   
        
            sleep(2)

            query2 = ("INSERT INTO leitura(fkMetrica, horario, valorLido, fkComponente_idComponente, fkComponente_fkServidor) VALUES(%s, now(), %s, %s, %s)")   

            val = (metrica, row, componente, servidor, ) 

            cursor_server.execute(query, val)
            sleep(2)
            cursor_mysql.execute(query2, val)
            bdsql_server.commit()
            sleep(2)
            bdmysql.commit()
            
threading.Thread(target=executar_{i}, args=('{row[2]}', {row[1]}, {row[0]},)).start()
    """
        i += 1
        if script != None:
            exec(script)

        sleep(5)
        print("Executando...")

        isWorking = verificarAtualizacaoParametros(mac, qtdParametros)

    selecionarParametro(mac)

def verificarAtualizacaoParametros(mac, qtdParametros):
    bdsql_server, cursor_server, bdmysql, cursor_mysql = conectar()

    query = ("SELECT * from parametro WHERE fkComponente_fkServidor = %s")

    params = (mac, )
    cursor_server.execute(query, params)

    resposta = cursor_server.fetchall()

    if(len(resposta) > qtdParametros):
        return False
    else:
        return True



def conectar():
    import pymssql 

    server = "airdataserver.database.windows.net"
    database = "airdata"
    user = "CloudSA9549f82c"
    password = "pi-airdata2022"

    bdsql_server = pymssql.connect(server, user, password, database)
    mycursor_server = bdsql_server.cursor()

    
    import mysql.connector

    bdmysql = mysql.connector.connect(host="172.17.0.2", user="root", password="urubu100", database="airData")
    mysqlcursor = bdmysql.cursor()

    return (bdsql_server, mycursor_server, bdmysql, mysqlcursor)


if __name__ == '__main__':
    main()
