from database.DB_connect import DBConnect
from model.arco import Arco
from model.artist import Artist



class DAO():

    @staticmethod
    def getCountry():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.Country
                    from customer c """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(country):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct  art.ArtistId, art.Name 
                    from album a, track t, invoiceline il, invoice i , customer c, artist art
                    where a.AlbumId =t.AlbumId and t.TrackId =il.TrackId and il.InvoiceId =i.InvoiceId and c.CustomerId = i.CustomerId 
                    and c.Country = %s and a.ArtistId = art.ArtistId
                    order by art.Name asc"""

        cursor.execute(query, (country, ))

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(country, idMapA):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select  art1.artistid as id1, art2.artistid as id2, count(distinct i.InvoiceId) as peso
                    from artist art1, artist art2, invoiceline il1, invoiceline il2, invoice i, customer c, track t1, track t2, album a1, album a2
                    where c.CustomerId = i.CustomerId 
                    and il1.InvoiceId = i.InvoiceId
                    and il2.InvoiceId =i.InvoiceId  
                    and il1.TrackId =t1.TrackId  
                    and t2.TrackId =il2.TrackId 
                    and a1.AlbumId = t1.AlbumId and a2.AlbumId =t2.AlbumId and art1.artistid > art2.artistid 
                    and art1.artistid =a1.ArtistId and art2.artistid =a2.ArtistId and c.Country=%s
                    group by art1.artistid, art2.artistid
                    order by peso desc"""

        cursor.execute(query, (country, ))

        for row in cursor:
            results.append(Arco(idMapA[row["id1"]], idMapA[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results


"""
TRACCIA ALTERNATIVA
a. L'utente seleziona dal corrispondente menù a tendina un Paese di fatturazione (BillingCountry nella tabella Invoice).  
b. Premendo il pulsante "Crea grafo", l'applicazione costruisce un grafo orientato e pesato che rappresenta le relazioni di gerarchia
     e di performance di vendita tra gli impiegati.  
     I vertici sono tutti gli impiegati (Employee) presenti nel database.  
     Esiste un arco tra l'impiegato A e l'impiegato B se esiste un legame gerarchico diretto tra loro, ovvero sfruttando l'anello ReportsTo (A riporta a B, oppure B riporta ad A). 
     Il verso dell'arco va da A verso B se il fatturato totale (somma della colonna Total in Invoice per i clienti associati all'impiegato tramite SupportRepId) generato da A nel 
     Paese selezionato è maggiore del fatturato generato da B. 
     In caso in cui A e B abbiano lo stesso fatturato, aggiungere due archi in entrambi i versi.  
     Il peso dell'arco tra l'impiegato A e l'impiegato B è calcolato come la somma dei rispettivi fatturati nel Paese selezionato. 


NODI:
select distinct *
from employee e 


ARCHI:
SELECT e1.EmployeeId AS id1, e2.EmployeeId AS id2, (e1.fatturatoTotale + e2.fatturatoTotale) AS peso
FROM 
  (SELECT e.EmployeeId, e.ReportsTo, 
          COALESCE((SELECT SUM(i.Total) 
                    FROM customer c, invoice i 
                    WHERE c.CustomerId = i.CustomerId 
                      AND c.SupportRepId = e.EmployeeId 
                      AND i.BillingCountry = 'Brazil'), 0) AS fatturatoTotale
   FROM employee e) e1,
  (SELECT e.EmployeeId, e.ReportsTo, 
          COALESCE((SELECT SUM(i.Total) 
                    FROM customer c, invoice i 
                    WHERE c.CustomerId = i.CustomerId 
                      AND c.SupportRepId = e.EmployeeId 
                      AND i.BillingCountry = 'Brazil'), 0) AS fatturatoTotale
   FROM employee e) e2
WHERE (e1.ReportsTo = e2.EmployeeId OR e2.ReportsTo = e1.EmployeeId)
  AND e1.fatturatoTotale >= e2.fatturatoTotale
  AND e1.EmployeeId <> e2.EmployeeId

alternativa archi: 
SELECT e1.EmployeeId as id1, e2.EmployeeId as id2, (e1.fatturatoTotale + e2.fatturatoTotale) as peso
FROM
  (SELECT e.EmployeeId, e.ReportsTo, COALESCE(SUM(i.Total), 0) as fatturatoTotale
   FROM employee e
   LEFT JOIN customer c ON c.SupportRepId = e.EmployeeId
   LEFT JOIN invoice i ON i.CustomerId = c.CustomerId AND i.BillingCountry = 'Italy'
   GROUP BY e.EmployeeId, e.ReportsTo) e1,
  (SELECT e.EmployeeId, e.ReportsTo, COALESCE(SUM(i.Total), 0) as fatturatoTotale
   FROM employee e
   LEFT JOIN customer c ON c.SupportRepId = e.EmployeeId
   LEFT JOIN invoice i ON i.CustomerId = c.CustomerId AND i.BillingCountry = 'Italy'
   GROUP BY e.EmployeeId, e.ReportsTo) e2

WHERE
  (e1.ReportsTo = e2.EmployeeId OR e2.ReportsTo = e1.EmployeeId)
  AND e1.fatturatoTotale >= e2.fatturatoTotale
  AND e1.EmployeeId <> e2.EmployeeId;









"""
