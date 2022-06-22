import psycopg2
import time

start = time.time()


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


'''
connection = Connection("localhost", "amazon", "postgres", "123456")

print(connection._db.cursor())
# print(connection.manipular("insert into cidade values (default,'Rio Paulo','RP')"))
print(connection.consultar("select * from cidade;"))
# connection.fechar()
answer = connection.consultar("select * from cidade;")

print(answer[0][1])
'''
lista = []
objeto = {}


def numbers_to_strings(argument):
    switcher = {
        'Book': 1,
    }
    return switcher.get(argument, "nothing")


with open("amazon-meta.txt", "r") as arquivo:
    entrada = arquivo.readlines()
    entradaSemQuebra = [n.replace('\n', '')
                        for n in entrada]
    tam = len(entradaSemQuebra)
    # print(tam)
    for i in range(tam):
        propriedade = entradaSemQuebra[i].split(":")[0].strip()
        if propriedade == 'Id':
            if objeto.get('id') or i == tam - 1:
                # print('acabou o produto, vai comecar um novo')
                lista.append(objeto)
                objeto = {}
            # else:
                # print('ainda n')
            objeto['id'] = entradaSemQuebra[i].split(":")[1].strip()
        elif propriedade == 'ASIN':
            objeto['asin'] = entradaSemQuebra[i].split(':')[1].strip()
        elif propriedade == 'title':
            objeto['title'] = entradaSemQuebra[i].strip()[7:]
        elif propriedade == 'group':
            objeto['group_id'] = numbers_to_strings(
                entradaSemQuebra[i].split(":")[1].strip())
        elif propriedade == 'salesrank':
            objeto['salesrank'] = entradaSemQuebra[i].split(":")[1].strip()
        elif propriedade == 'similar':
            objeto['similar'] = entradaSemQuebra[i].split(
                ":")[1].strip().split('  ')
        elif propriedade == 'categories':
            objeto['categories'] = []
            for j in range(1, int(entradaSemQuebra[i].split(":")[1].strip())+1):
                objeto['categories'].append(
                    list(filter(None, entradaSemQuebra[i + j].strip().split("|"))))
        elif propriedade == 'reviews':
            objeto['reviews'] = []
            for j in range(1, int(entradaSemQuebra[i].split(":")[3].strip()[0] + entradaSemQuebra[i].split(":")[3].strip()[1]) + 1):
                novoReview = {
                    'date': entradaSemQuebra[i + j].strip().split(
                        "|")[0].split(':')[0].strip().split('  ')[0],  # pegando data de cada review
                    'customer': entradaSemQuebra[i + j].strip().split(
                        "|")[0].split(':')[1].strip().split('  ')[0],
                    'rating': entradaSemQuebra[i + j].strip().split(
                        "|")[0].split(':')[2].strip().split('  ')[0],
                    'votes': entradaSemQuebra[i + j].strip().split(
                        "|")[0].split(':')[3].strip().split('  ')[0],
                    'helpful': entradaSemQuebra[i + j].strip().split(
                        "|")[0].split(':')[4].strip().split('  ')[0]
                }
                objeto['reviews'].append(novoReview)
    lista.append(objeto)
    end = time.time()
    print(end - start)
tam = len(lista)
pos = -1
while True:
    while(pos < 0 or pos > tam):
        pos = int(input('qual posicao deseja checar?'))
    print(lista[pos])
    break
