from database.DB_connect import DBConnect
from model.team import Team


class DAO:
    @staticmethod
    def get_year():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT t.year as year
                    FROM team t 
                    WHERE year >= 1980"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_team_by_year(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.id, t.team_code, t.name 
                   from team t
                   where t.`year` = %s
                """

        cursor.execute(query, (year,))

        for row in cursor:
            team = Team(row["id"], row["team_code"], row["name"])
            result.append(team)
            #result è una lista di oggetti team hashable

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def calcola_peso(nodo1: Team, nodo2: Team):
        conn = DBConnect.get_connection()
        result = 0

        id1 = int(nodo1.id)
        id2 = int(nodo2.id)
        cursor = conn.cursor(dictionary=True)
        query = """select SUM(s.salary) as salario 
                   from salary s , team t 
                   where t.id in (%s, %s) and t.id = s.team_id"""

        cursor.execute(query, (id1, id2))

        for row in cursor:
            result = row["salario"]

        cursor.close()
        conn.close()
        return result




