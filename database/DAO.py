from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getAlbums(nItems):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.*, count(*) as NumeroCanzoni
                    from itunes.album a, itunes.track t 
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId 
                    having count(*) > %s"""
        cursor.execute(query, (nItems, ))
        for row in cursor:
            result.append(Album(**row))
        cursor.close()
        conn.close()
        return result
