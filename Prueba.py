import pyodbc

host = '192.168.1.19'
db = 'saf'
user = 'ap_ventadigital'
password = 'cl4v32017**'

try:
    con = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + host + ';DATABASE=' + db + ';UID=' + user + ';PWD=' + password)
    print("Conexion Exitosa")

except Exception as e:

    print("Ocurrio un error", e)


def contratoSinPDFQurey1():
    cursor = con.cursor()
    sql = "select co.ContratoID from FOC_Contrato co " \
          "left join  VEN_ProcesoContratoDocumento pro on pro.ContratoID = co.ContratoID " \
          "where co.ContratoFechaIngreso > (getdate() - 90) and " \
          "(select count(1) from FOC_Movimiento mov where mov.ContratoID=co.ContratoID) > 0 " \
          "and co.ContratoDocumentoDigital = 1 group by co.ContratoID having count(1)=0;"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

def contratoSinPDFQuery2():
    cursor = con.cursor()
    sql = "select top 5 co.ContratoID,co.ContratoNumero,co.ContratoFechaIngreso,co.ContratoFechaVenta, co.ContratoDocumentoDigital," \
          "pro.ProcesoContratoDocumentoTipoProceso,pro.ProcesoContratoDocumentoEstado,pro.ProcesoContratoDocumentoResponse,"\
          "pro.*,co.* from FOC_Contrato co "\
          "left join (select dd.ContratoID, max(dd.ProcesoContratoDocumentoID) as ProcesoContratoDocumentoID from VEN_ProcesoContratoDocumento dd group by dd.ContratoID) max "\
          "on (max.ContratoID = co.ContratoID)"\
          "left join  VEN_ProcesoContratoDocumento pro on pro.ProcesoContratoDocumentoID = max.ProcesoContratoDocumentoID "\
          "where co.ContratoFechaIngreso > (getdate() - 90) "\
          "and (select count(1) from FOC_Movimiento mov where mov.ContratoID=co.ContratoID) > 0 "\
          "and (pro.ProcesoContratoDocumentoEstado <> 'TERMINADO' OR pro.ProcesoContratoDocumentoTipoProceso <> 'PROCESAR_FIRMA') "\
          "and co.ContratoDocumentoDigital = 1"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

print("Contratos Sin PDF",contratoSinPDFQuery2())
