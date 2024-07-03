from database.DB_connect import DBConnect
from model.Gene import Gene


class DAO:

    @staticmethod
    def getAllGenes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                   FROM genes"""

        cursor.execute(query)

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllChromosomes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT(Chromosome)
                   FROM genes g
                   WHERE Chromosome > 0"""

        cursor.execute(query)

        for row in cursor:
            result.append(row['Chromosome'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnessioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT g1.GeneID as Gene1, g2.GeneID as Gene2, i.Expression_Corr
                   FROM genes g1, genes g2, interactions i
                   WHERE g1.GeneID = i.GeneID1 and g2.GeneID = i.GeneID2
                   AND g1.Chromosome != g2.Chromosome
                   AND g1.Chromosome > 0
                   AND g2.Chromosome > 0
                   GROUP BY g1.GeneID, g2.GeneID """

        cursor.execute(query)

        for row in cursor:
            result.append((row['Gene1'], row['Gene2'], row['Expression_Corr']))

        cursor.close()
        conn.close()
        return result

