import psycopg2


class Connection(object):
    _db = None

    def __init__(self, mhost, db, usr, pwd):
        self._db = psycopg2.connect(
            host=mhost, database=db, user=usr,  password=pwd)

    def manipulate(self, sql):
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except:
            return False

        return True

    def consult(self, sql):
        rs = None
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            rs = cur.fetchall()
        except:
            return None
        return rs

    def fechar(self):
        self._db.close()


connection = Connection("localhost", "amazon", "postgres", "123456")

print(connection._db.cursor())
# print(connection.manipular("insert into cidade values (default,'Rio Paulo','RP')"))
print(connection.consultar("select * from cidade;"))
# connection.fechar()
answer = connection.consultar("select * from cidade;")

print(answer[0][1])
