from tomlkit import table
from rich.table import Table
from rich.progress import track
from rich.markdown import Markdown
from rich.console import Console
import psycopg2
import time
import re


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


def strings_to_numbers(argument):
    switcher = {
        0: 'nothing',
        1: 'Book',
        2: 'DVD',
        3: 'Video',
        4: 'Music'
    }
    return switcher.get(argument, "nothing")


def confirm():
    text = input("Pressione enter para continuar consultando...\n\n")
    if text == "":
        return True
    else:
        return False


connection = Connection("database", "tp1-bd-2021-02",
                        "tp1-bd-2021-02", "tp1-bd-2021-02")

MAKRDOWN = """

# Escolha a conusulta que deseja fazer no Banco de Dados: 

1.  Os 5 comentários mais úteis e com maior avaliação
2.  Dado um produto, listar os produtos similares com maiores vendas do que ele
3.  Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada  
4.  Listar os 10 produtos líderes de venda em cada grupo de produtos
5.  Listar os 10 produtos com a maior média de avaliações úteis positivas por produto
6.  Listar as 5 categorias de produto com a maior média de avaliações úteis positivas por produto
7.  Listar os 10 clientes que mais fizeram comentários por grupo de produto

"""

while True:
    # titulo e coias a afim do usuario!!
    console = Console()
    md = Markdown(MAKRDOWN)
    console.print(md)

    # Escolha Opção do Usuario
    choice = int(input("\n\nEscolha a opção desejada: \n"))

    if(choice == 1):
        # consulta1 tem q inserir em uma dicionario
        id = int(input('\n\nInsira o id do produto:'))

        for i in track(range(5), description="Consultando..."):
            print(f"Buscando no Banco de Dados")
            time.sleep(0.5)

        products = connection.consult(f"""
            (SELECT pr.product_id, pr.review_id, r.user_id, r.rating, r.votes, r.helpful
            FROM products p, products_reviews pr, reviews r
            WHERE {id} = pr.product_id AND pr.review_id = r.id AND r.helpful > 0
            ORDER BY r.rating DESC, r.votes DESC, r.helpful DESC
            FETCH FIRST 5 ROW ONLY)
            UNION
            (SELECT pr.product_id, pr.review_id, r.user_id, r.rating, r.votes, r.helpful
            FROM products p, products_reviews pr, reviews r 
            WHERE {id} = pr.product_id AND pr.review_id = r.id AND r.helpful > 0
            ORDER BY r.rating ASC, r.votes DESC, r.helpful DESC
            FETCH FIRST 5 ROW ONLY)
            ORDER BY helpful DESC;
        """)

        table = Table(
            title=f"Os produtos similares com maiores vendas do que ele ({id})")

        table.add_column("title")
        table.add_column("asin")
        table.add_column("group")

        for x in products:
            table.add_row(f"{x[2]}", f"{x[1]}", f"{strings_to_numbers(x[3])}")

        console = Console()
        console.print("\n\n\n", table)

        if not confirm():
            break

    if(choice == 2):
        # consulta1 tem q inserir em uma dicionario
        id = int(input('\n\nInsira o id do produto:'))

        for i in track(range(5), description="Consultando..."):
            print(f"Buscando no Banco de Dados")
            time.sleep(0.5)

        products = connection.consult(f"""
            SELECT distinct products.* 
            FROM products_similars 
            JOIN (SELECT similars.asin 
                FROM products_similars 
                JOIN products 
                ON products.id = {id} 
                JOIN similars 
                ON similars.id = products_similars.similar_id
            ) AS asins 
            ON asins.asin = products_similars.similar_id 
            JOIN (SELECT * from products 
                WHERE id = {id}
            ) AS ok 
            ON products_similars.product_id = {id} 
            JOIN products 
            ON products.asin = asins.asin AND products.salesrank > ok.salesrank;
        """)

        table = Table(
            title=f"Os produtos similares com maiores vendas do que ele ({id})")

        table.add_column("title")
        table.add_column("asin")
        table.add_column("group")

        for x in products:
            table.add_row(f"{x[2]}", f"{x[1]}", f"{strings_to_numbers(x[3])}")

        console = Console()
        console.print("\n\n\n", table)

        if not confirm():
            break
    if(choice == 3):
        # consulta1 tem q inserir em uma dicionario
        id = int(input('\n\nInsira o id do produto:'))

        for i in track(range(5), description="Consultando..."):
            print(f"Buscando no Banco de Dados")
            time.sleep(0.5)

        products = connection.consult(f"""
            SELECT pr.product_id, r.review_data, ROUND(AVG(rating), 1) AS average_reviews
            FROM products p, products_reviews pr, reviews r
            WHERE {id} = pr.product_id AND pr.review_id = r.id
            GROUP BY product_id, r.review_data
            ORDER BY product_id;
        """)

        table = Table(
            title=f"Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada ({id})")

        table.add_column("id")
        table.add_column("date")
        table.add_column("rating")

        for x in products:
            table.add_row(f"{x[0]}", f"{x[1]}", f"{x[2]}")

        console = Console()
        console.print("\n\n\n", table)

        if not confirm():
            break
    if(choice == 4):
        # consulta1 tem q inserir em uma dicionario
        # id = int(input('\n\nInsira o id do produto:'))

        for i in track(range(5), description="Consultando..."):
            print(f"Buscando no Banco de Dados")
            time.sleep(0.5)

        products = connection.consult(f"""
            SELECT *
            FROM (SELECT id, title, salesrank, group_id
                FROM products
                WHERE group_id = 1
                ORDER BY salesrank DESC
                FETCH FIRST 3 ROW ONLY) AS book 
            UNION ALL
            SELECT *
            FROM  (SELECT id, title, salesrank, group_id
                FROM products
                WHERE group_id = 2
                ORDER BY salesrank DESC
                FETCH FIRST 3 ROW ONLY) AS dvd
            UNION ALL
            SELECT *
            FROM  (SELECT id, title, salesrank, group_id
                FROM products
                WHERE group_id = 3
                ORDER BY salesrank DESC
                FETCH FIRST 3 ROW ONLY) AS video
            UNION ALL
            SELECT *
            FROM  (SELECT id, title, salesrank, group_id
                FROM products
                WHERE group_id = 4
                ORDER BY salesrank DESC
                FETCH FIRST 3 ROW ONLY) AS music;
        """)

        table = Table(
            title=f"Os 10 produtos líderes de venda em cada grupo de produtos")

        table.add_column("id")
        table.add_column("title")
        table.add_column("salesrank")
        table.add_column("group_id")
        for x in products:
            table.add_row(f"{x[0]}", f"{x[1]}", f"{x[2]}",
                          f"{strings_to_numbers(x[3])}")

        console = Console()
        console.print("\n\n\n", table)

        if not confirm():
            break
    if choice == 5:
        # consulta1 tem q inserir em uma dicionario
        # id = int(input('\n\nInsira o id do produto:'))

        for i in track(range(5), description="Consultando..."):
            print(f"Buscando no Banco de Dados")
            time.sleep(0.5)

        products = connection.consult(f"""
            SELECT * FROM (SELECT product_id, AVG(rating) AS media
                FROM products_reviews, reviews 
                WHERE products_reviews.id = reviews.id AND rating > 0 AND helpful > 0
                GROUP BY product_id
                ORDER BY media DESC
                FETCH FIRST 10 ROW ONLY) AS media_products JOIN products on products.id = media_products.product_id;
        """)
        table = Table(
            title=f"Os 10 produtos com a maior média de avaliações úteis positivas por produto")

        table.add_column("id")
        table.add_column("title")
        table.add_column("media")
        for x in products:
            table.add_row(f"{x[0]}", f"{x[4]}", f"{x[1]}")

        console = Console()
        console.print("\n\n\n", table)

        if not confirm():
            break
    if choice == 7:
        # consulta1 tem q inserir em uma dicionario
        # id = int(input('\n\nInsira o id do produto:'))

        for i in track(range(5), description="Consultando..."):
            print(f"Buscando no Banco de Dados")
            time.sleep(0.5)

        products = connection.consult(f"""
            SELECT *
            FROM (SELECT user_id, COUNT(user_id), group_id
                FROM products, products_reviews, reviews
                WHERE products.id = products_reviews.product_id AND products_reviews.id = reviews.id AND group_id = 1
                GROUP BY user_id, group_id
                ORDER BY count DESC 
                FETCH FIRST 10 ROW ONLY) as book
            UNION ALL
            SELECT *
            FROM (SELECT user_id, COUNT(user_id), group_id
                FROM products, products_reviews, reviews
                WHERE products.id = products_reviews.product_id AND products_reviews.id = reviews.id AND group_id = 2
                GROUP BY user_id, group_id
                ORDER BY count DESC 
                FETCH FIRST 10 ROW ONLY) as dvd
            UNION ALL
            SELECT *
            FROM (SELECT user_id, COUNT(user_id), group_id
                FROM products, products_reviews, reviews
                WHERE products.id = products_reviews.product_id AND products_reviews.id = reviews.id AND group_id = 3
                GROUP BY user_id, group_id
                ORDER BY count DESC
                FETCH FIRST 10 ROW ONLY) as video
            UNION ALL
            SELECT *
            FROM (SELECT user_id, COUNT(user_id), group_id
                FROM products, products_reviews, reviews
                WHERE products.id = products_reviews.product_id AND products_reviews.id = reviews.id AND group_id = 4
                GROUP BY user_id, group_id
                ORDER BY count DESC
                FETCH FIRST 10 ROW ONLY) as music;
        """)
        table = Table(
            title=f"Os 10 clientes que mais fizeram comentários por grupo de produto")

        table.add_column("user_id")
        table.add_column("number of comments")
        table.add_column("group_id")
        for x in products:
            table.add_row(f"{x[0]}", f"{x[1]}", f"{strings_to_numbers(x[2])}")

        console = Console()
        console.print("\n\n\n", table)

        if not confirm():
            break
