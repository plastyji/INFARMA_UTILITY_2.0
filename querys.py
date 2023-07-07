import configparser
import pyodbc
import logging
from datetime import date,datetime
from tkinter import messagebox




def data_atual():
  """Retorna data atual"""
  return str(date.today().strftime("%d%m%y"))

def date_time():
  """Retorna data e hora atual"""
  return str(datetime.today().strftime("%d/%m/%Y  %H:%M:%S"))

log_format = '%(asctime)'
logging.basicConfig(filename='InfarmaUti'+data_atual()+'.log',filemode='a',level=logging.INFO)
logger=logging.getLogger('root')


cfg = configparser.ConfigParser()
cfg.read('infarma.ini')
cod_loja=cfg.getint('SERVIDOR', 'Loja')
hostName= cfg.get('SERVIDOR',   'Hostname')
dataBase = cfg.get('SERVIDOR', 'Database')
driveOdbc = '{SQL SERVER}'

class Querys():
    def connectBanco():
        try:

            conn = pyodbc.connect(f"DRIVER={driveOdbc};Server={hostName};DATABASE={dataBase};", timeout=5)
            return conn

            
        except Exception as e:
            logging.exception("Verifique as informações do banco de dados")
            
            logging.warning(date_time()+e)
    def closeday():
        try:
            conn = Querys.connectBanco()
            cursor = conn.cursor()
            
            cursor.execute(f"UPDATE LOJAS SET Par_DatUltFecDia=(SELECT CAST(CONVERT(date, DATEADD(DAY, -1, GETDATE()), 23) AS datetime) AS DataOntem) WHERE COD_LOJA={cod_loja}")
            cursor.commit()
            return
        except Exception as e:
            logging.exception("Algo deu errado!")
            
            logging.warning(date_time()+e)
    def ajustregsms():
        try:
            sql = ("UPDATE PRODU SET NUM_REGMS = REPLACE(REPLACE(NUM_REGMS, '.', ''), '-', '') WHERE NUM_REGMS LIKE '%.%' OR NUM_REGMS LIKE '%-%'")
            conn = Querys.connectBanco()
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.commit()
        except Exception as e:
            logging.exception("Algo deu errado!")
            
            logging.warning(date_time()+e)    
    
    def InsertAC(retorno):
        try: 
            conn = Querys.connectBanco()         
            cursor = conn.cursor()
            sql =  (f"UPDATE LOJAS SET Des_AssDigSat='{retorno}' WHERE COD_LOJA={cod_loja}")
            cursor.execute(sql)
            cursor.commit()  
                   
        except Exception as e:
            logging.exception('Erro ao Vincular chave AC!')
            logging.warning(date_time()+e)  

    def emitirnota():
        try:        
            conn = Querys.connectBanco()
            sql = (f"insert into FS_PARAM values ('NFE_HAB_TLS','I','1','Habilita TLS 1.2',{cod_loja},null,null)")
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.execute("insert into fs_param values('NFE_RSP_TEC','S','1','Habilita envio Resp. Técnico NFE/NFCe',1,NULL,NULL)")
            cursor.commit()
            return
        except Exception as e:
            logging.exception('Erro ao Inserir o TLS!')
            logging.warning(date_time()+e) 
    def alterar_database():
        conn =Querys.connectBanco()
        cursor = conn.cursor()
        cursor.execute("ALTER DATABASE VMD SET RECOVERY SIMPLE")
        conn.commit()
    def alterar_databasefull():
        conn = Querys.connectBanco()
        cursor = conn.cursor()
        cursor.execute("ALTER DATABASE VMD SET RECOVERY FULL")
        cursor.commit()
    def reduz_banco():
        try:
            conn = Querys.connectBanco()
            Querys.alterar_database()
            cursor = conn.cursor()
            cursor.execute("DBCC SHRINKFILE('VMD_LOG', TRUNCATEONLY)")
            cursor.commit()
            Querys.alterar_databasefull()
            conn.close()
        except Exception as e:
            logging.exception('Erro ao Reduzir o log!')
            logging.warning(date_time()+e)     
    def versaopdv2():
        try:       
        
            sql = (f"update lojas set par_pdvversao='2.0' where cod_loja={cod_loja}")            
            conn = Querys.connectBanco()
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.commit()
            return        
            
        except Exception as e:
            logging.exception('Erro ao alterar a versão do pdv!')
            logging.warning(date_time()+e)  
    #Alterar a versão do PDV para 1.0#
    def versaopdv1():
        try:          
            sql = (f"update lojas set par_pdvversao='1.0' where cod_loja={cod_loja}")
            conn = Querys.connectBanco()
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.commit()
            return           
        except Exception as e:
            logging.exception('Erro ao alterar a versão do pdv!')
            logging.warning(date_time()+e)
    def pdv_express():
        try:       
    
            sql = (f"update lojas set par_pdvversao='2.0' where cod_loja={cod_loja}")
            conn = Querys.connectBanco()
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.execute(f"UPDATE LOJAS SET Flg_PdvExp='1' WHERE COD_LOJA={cod_loja}")
            cursor.commit()
            return        
        except Exception as e:
            logging.exception('Erro ao alterar a versão do pdv!')
            logging.warning(date_time()+e)        
    def criausuario():
        try:  
            if ('conn = connectBanco()'):
                conn = Querys.connectBanco()          
                sql = (
                    f"if not exists (select * from master..syslogins where name = N'VMDApp')EXEC sp_addlogin N'VMDApp', N'VMD22041748', N'{dataBase}', N'Português'"  
                    "exec sp_addsrvrolemember N'VMDApp',"
                    "sysadmin "
                    "if not exists (select * from sysusers where name = N'VMDApp' and uid < 16382)   EXEC sp_grantdbaccess N'VMDApp', N'VMDApp'"
                        )
                                
                cursor = conn.cursor()
                cursor.execute(sql)
                cursor.commit()
                return
        except Exception as e:
            logging.exception('Erro ao alterar a versão do pdv!')
            logging.warning(date_time()+e) 