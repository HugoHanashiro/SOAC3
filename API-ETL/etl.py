def main():
  bdsql_server, mycursor_server  = conectar_server()

  mycursor_server.execute("SELECT idEmpresa, cnpjEmpresa, nomeEmpresa, telefoneEmpresa FROM empresa")

  myresult = mycursor_server.fetchall()

  bdsql_docker, mycursor_docker = conectar_docker()

  for x in myresult:
    sql = "INSERT INTO empresa (idEmpresa, cnpjEmpresa, nomeEmpresa, telefoneEmpresa) VALUES (%s, %s, %s, %s)"
    val = (x[0], x[1], x[2], x[3], )
    mycursor_docker.execute(sql, val)
    bdsql_docker.commit()

  mycursor_server.execute("SELECT idAeroporto, fkEmpresa, nomeAeroporto, cepAeroporto, numeroAeroporto, ufAeroporto, cidadeAeroporto, bairroAeroporto, ruaAeroporto FROM aeroporto")

  myresult = mycursor_server.fetchall()

  for x in myresult:
    sql = "INSERT INTO aeroporto (idAeroporto, fkEmpresa, nomeAeroporto, cepAeroporto, numeroAeroporto, ufAeroporto, cidadeAeroporto, bairroAeroporto, ruaAeroporto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], )
    mycursor_docker.execute(sql, val)
    bdsql_docker.commit()

  mycursor_server.execute("SELECT idTorre, fkAeroporto FROM torre")

  myresult = mycursor_server.fetchall()

  for x in myresult:
    sql = "INSERT INTO torre (idTorre, fkAeroporto) VALUES (%s, %s)"
    val = (x[0], x[1], )
    mycursor_docker.execute(sql, val)
    bdsql_docker.commit()

  mycursor_server.execute("SELECT idServidor, fkTorre FROM servidor")

  myresult = mycursor_server.fetchall()

  for x in myresult:
    sql = "INSERT INTO servidor (idServidor, fkTorre) VALUES (%s, %s)"
    val = (x[0], x[1], )
    mycursor_docker.execute(sql, val)
    bdsql_docker.commit()

  mycursor_server.execute("SELECT idComponente, fkServidor, tipoComponente, nomeComponente, memoria, tipoMemoria FROM componente")

  myresult = mycursor_server.fetchall()

  for x in myresult:
    sql = "INSERT INTO componente (idComponente, fkServidor, tipoComponente, nomeComponente, memoria, tipoMemoria) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (x[0], x[1], x[2], x[3], x[4], x[5], )
    mycursor_docker.execute(sql, val)
    bdsql_docker.commit()

  mycursor_server.execute("SELECT idMetrica, nomeComponente, nomeMetrica, nomeView, comando, unidadeMedida, isTupla FROM metrica")

  myresult = mycursor_server.fetchall()

  for x in myresult:
    sql = "INSERT INTO metrica (idMetrica, nomeComponente, nomeMetrica, nomeView, comando, unidadeMedida, isTupla) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (x[0], x[1], x[2], x[3], x[4], x[5], x[6], )
    mycursor_docker.execute(sql, val)
    bdsql_docker.commit()

  mycursor_server.execute("SELECT fkMetrica, fkComponente_idComponente, fkComponente_fkServidor FROM parametro")

  myresult = mycursor_server.fetchall()

  for x in myresult:
    sql = "INSERT INTO parametro (fkMetrica, fkComponente_idComponente, fkComponente_fkServidor) VALUES (%s, %s, %s)"
    val = (x[0], x[1], x[2], )
    mycursor_docker.execute(sql, val)
    bdsql_docker.commit()

def conectar_docker():
  # pip install pymysql
  import mysql.connector

  bdsql = mysql.connector.connect(host="172.17.0.2", user="root", password="urubu100", database="airData")

  mycursor = bdsql.cursor()

  return bdsql, mycursor

def conectar_server():
  import pymssql 

  server = "airdataserver.database.windows.net"
  database = "airdata"
  user = "CloudSA9549f82c"
  password = "pi-airdata2022"

  bdsql_server = pymssql.connect(server, user, password, database)
  mycursor_server = bdsql_server.cursor()


  return bdsql_server, mycursor_server
  
if __name__ == "__main__":
  main()