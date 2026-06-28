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


    """ NODI
    select distinct  art.ArtistId, art.Name 
from album a, track t, invoiceline il, invoice i , customer c, artist art
where a.AlbumId =t.AlbumId and t.TrackId =il.TrackId and il.InvoiceId =i.InvoiceId and c.CustomerId = i.CustomerId 
and c.Country = "Brazil" and a.ArtistId = art.ArtistId 
  
ARCHI
select  art1.artistid, art2.artistid, count(distinct i.InvoiceId) as peso
from artist art1, artist art2, invoiceline il1, invoiceline il2, invoice i, customer c, track t1, track t2, album a1, album a2
where c.CustomerId = i.CustomerId 
and il1.InvoiceId = i.InvoiceId and il1.InvoiceLineId <> il2.InvoiceLineId 
and il2.InvoiceId =i.InvoiceId  
and il1.TrackId =t1.TrackId  
and t2.TrackId =il2.TrackId 
and a1.AlbumId = t1.AlbumId and a2.AlbumId =t2.AlbumId and art1.artistid < art2.artistid 
and art1.artistid =a1.ArtistId and art2.artistid =a2.ArtistId and c.Country= "Brazil"
group by art1.artistid, art2.artistid


"""