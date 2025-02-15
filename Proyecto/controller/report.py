from config.app import *
import pandas as pd

def GenerateReportVentas(app:App):
    conn=app.bd.getConection()
    query="""
        SELECT 
            p.pais,
            v.product_id,
            v.quantity,
            v.price
        FROM 
            VENTAS v
        JOIN 
            POSTALCODE p
        ON 
            v.postal_code = p.code
    """
    df=pd.read_sql_query(query,conn)
    df['total_gastado'] = df['quantity'] * df['price']
    df_grouped = df.groupby('pais', as_index=False)['total_gastado'].sum()
    df_top = df_grouped.sort_values(by='total_gastado', ascending=False).head(1)
    fecha="14-02"
    path=f"/workspaces/ultimapractica-python-datux/Proyecto/files-{fecha}.csv"
    df_top.to_csv(path)
    sendMail(app,path)

def sendMail(app:App,data):

    app.mail.send_email('from@example.com','Reporte del país con mayor gasto en ventas', 'Adjunto el reporte del país que más gastó en ventas',data)