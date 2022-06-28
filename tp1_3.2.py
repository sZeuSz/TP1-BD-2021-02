from tomlkit import table
from rich.table import Table
from rich.progress import track
from rich.markdown import Markdown
from rich.console import Console
import psycopg2
import time
import re

start = time.time()


class Connection(object):
    _db = None

    def __init__(self, mhost, db, usr, pwd):
        try:
            self._db = psycopg2.connect(
                host=mhost, database=db, user=usr,  password=pwd)
            print("êêêê conectou berg")
        except Exception as error:
            print(error)

    def manipulate(self, sql, id_similar=None):
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            id = cur.fetchall()
            cur.close()
            self._db.commit()
        except Exception as error:
            print(error)
            return False

        if(id):
            return id[0][0]
        else:
            return None

    def create(self, sql):
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except Exception as error:
            print(error)
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
categories = {}


def numbers_to_strings(argument):
    switcher = {
        'nothing': 0,
        'Book': 1,
        'DVD': 2,
        'Video': 3,
        'Music': 4
    }
    return switcher.get(argument, "nothing")


with open("entrada1.txt", "r") as arquivo:
    entrada = arquivo.readlines()
    entradaSemQuebra = [n.replace('\n', '')
                        for n in entrada]
    tam = len(entradaSemQuebra)
    for i in range(tam):
        propriedade = entradaSemQuebra[i].split(":")[0].strip()
        if propriedade == 'Id':
            if objeto.get('id') or i == tam - 1:
                lista.append(objeto)
                objeto = {}
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
            objeto['similar'] = objeto['similar'][1:]
        elif propriedade == 'categories':
            objeto['categories'] = set()
            for j in range(1, int(entradaSemQuebra[i].split(":")[1].strip())+1):
                allCategoriesLine = list(
                    filter(None, entradaSemQuebra[i + j].strip().split("|")))
                prev = []
                for k in range(len(allCategoriesLine)):
                    for l, pedaco in enumerate(re.findall(r'\[([^]]+)\]', allCategoriesLine[k])):
                        prev.append(pedaco)
                        if(k == 0):
                            objeto['categories'].add(
                                (allCategoriesLine[k], pedaco, 'null'))
                        else:
                            objeto['categories'].add(
                                (allCategoriesLine[k], pedaco, prev[l - 2]))
        elif propriedade == 'reviews':
            objeto['reviews'] = []
            for j in range(1, int(entradaSemQuebra[i].split(":")[3].split(' ')[1]) + 1):
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

# print(lista)

# seeds bd
# commands
# connection.manipular
# connection.consultar
# # connection.fechar
# for element in lista:
#     print(element.get('title'))


connection = Connection("database", "tp1-bd-2021-02",
                        "tp1-bd-2021-02", "tp1-bd-2021-02")

# creating tables

connection.create("""
    DROP TABLE IF EXISTS products, categories, product_categories, reviews, products_reviews, similars, products_similars, groups;
""")

connection.create("""
    CREATE TABLE IF NOT EXISTS "products" (
        id INTEGER unique,
        asin VARCHAR(10),
        title TEXT DEFAULT NULL,
        group_id INTEGER DEFAULT NULL,
        salesrank INTEGER DEFAULT NULL,
        CONSTRAINT "products_pk" PRIMARY KEY("id")
); """)

connection.create("""
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER DEFAULT NULL,
        title TEXT,
        parent_id INTEGER DEFAULT NULL,
        CONSTRAINT "categories_pk" PRIMARY KEY ("id")
);""")

connection.create("""
    CREATE TABLE IF NOT EXISTS product_categories(
        id SERIAL,
        product_id INTEGER,
        category_id INTEGER,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (category_id) REFERENCES categories(id),
        CONSTRAINT "product_categories_pk" PRIMARY KEY ("id")
);""")

connection.create("""
    CREATE TABLE IF NOT EXISTS reviews (
        id SERIAL,
        review_data DATE,
        user_id VARCHAR(14),
        rating INTEGER,
        votes INTEGER,
        helpful INTEGER,
        CONSTRAINT "reviews_pk" PRIMARY KEY ("id")
);
""")

connection.create("""
    CREATE TABLE IF NOT EXISTS products_reviews (
        id SERIAL,
        product_id INTEGER,
        review_id INTEGER,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (review_id) REFERENCES reviews(id),
        CONSTRAINT "products_reviews_pk" PRIMARY KEY ("id")
);""")

connection.create("""
    CREATE TABLE IF NOT EXISTS similars (
        id VARCHAR(10), 
        asin VARCHAR(10),
        CONSTRAINT "similars_pk" PRIMARY KEY ("id")
);
""")

connection.create("""
    CREATE TABLE IF NOT EXISTS products_similars (
        id SERIAL,
        product_id INTEGER,
        similar_id VARCHAR(10) ,
        FOREIGN KEY (similar_id) REFERENCES similars(id),
        FOREIGN KEY (product_id) REFERENCES products(id),
        CONSTRAINT "products_similars_pk" PRIMARY KEY ("id")
);
""")

connection.create("""
    CREATE TABLE IF NOT EXISTS groups (
        id SERIAL,
        title TEXT,
        CONSTRAINT "groups_pk" PRIMARY KEY ("id")
);
""")

connection.manipulate("""
    INSERT INTO groups (
            title
        )
    VALUES ('Book'), ('DVD'), ('Video'), ('Music')
    ON CONFLICT DO NOTHING;
""")
for element in lista:
    # print(element)
    id = element.get('id')
    asin = element.get('asin')
    title = element.get('title')
    group_id = element.get('group_id')
    salesrank = element.get('salesrank')
    similar = element.get('similar')
    categories = element.get('categories')
    reviews = element.get('reviews')
    # print("groupp", group_id)
    id_product = connection.manipulate(f"""
            INSERT INTO products (
                id,
                asin,
                title,
                group_id,
                salesrank
            )
            VALUES (
                {id if id else 'null'},
               '{asin if asin else 'null'}',
               '{title.replace("'", '') if title else 'null'}',
                {group_id if group_id else 'null'},
                {salesrank if salesrank else 'null'}
            ) ON CONFLICT DO NOTHING RETURNING ID;
        """)
    # print(id_product)
    if similar:
        for s in similar:
            # print(s)
            id_similar = connection.manipulate(f"""
                INSERT INTO similars (
                    id,
                    asin
                )
                VALUES (
                    '{s}',
                    '{s}'
                ) ON CONFLICT DO NOTHING RETURNING ID;
            """)
            id_similar = s
            connection.manipulate(f"""
                INSERT INTO products_similars (
                    product_id, 
                    similar_id
                ) 
                VALUES (
                    '{id_product}',
                    '{id_similar}'
                ) ON CONFLICT DO NOTHING RETURNING ID;
            """)
    if categories:
        for category in categories:
            # print(category)
            id_category = connection.manipulate(f"""
                INSERT INTO categories (
                    id, 
                    title, 
                    parent_id
                ) 
                VALUES (
                    '{category[1]}',
                    '{category[0].replace("'", '')}',
                    '{0 if category[2] == 'null' else category[2]}'
                ) ON CONFLICT DO NOTHING RETURNING ID;
            """)
            id_category = category[1]
            connection.manipulate(f"""
                INSERT INTO product_categories (
                    product_id, 
                    category_id
                ) 
                VALUES (
                    {id_product}, 
                    {id_category}
                ) ON CONFLICT DO NOTHING;
            """)
    if(reviews):
        for review in reviews:
            # print(review['helpful'])
            id_review = connection.manipulate(f"""
                INSERT INTO reviews (
                    review_data, 
                    user_id, 
                    rating, 
                    votes, 
                    helpful
                ) 
                VALUES (
                    '{review['date']}', 
                    '{review['customer']}', 
                    {review['rating']}, 
                    {review['votes']}, 
                    {review['helpful']}
                )ON CONFLICT DO NOTHING RETURNING ID;
            """)
            # print(id_product)
            # print(review)
            # print(id_review)
            connection.manipulate(f"""
                INSERT INTO products_reviews (
                    product_id, 
                    review_id
                ) 
                VALUES (
                    {id_product}, 
                    {id_review}
                )RETURNING ID;
            """)
