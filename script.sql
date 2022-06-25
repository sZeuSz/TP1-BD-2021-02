-- "SELECT a.*, b.* from `categories` as a left join `categories` as b on a.id = b.parent where a.parent = 0"

CREATE TABLE IF NOT EXISTS "products" (
    id INTEGER unique,
    asin VARCHAR(10),
    title TEXT DEFAULT NULL,
    group_id INTEGER DEFAULT NULL,
    salesrank INTEGER DEFAULT NULL,
    CONSTRAINT "products_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS categories(
    id INTEGER DEFAULT NULL,
    title TEXT,
    parent_id INTEGER INTEGER DEFAULT NULL ,
    CONSTRAINT "categories_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS product_categories(
    id SERIAL,
    product_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    CONSTRAINT "product_categories_pk" PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL,
    review_data DATE,
    user_id VARCHAR(14),
    rating INTEGER,
    votes INTEGER,
    helpful INTEGER,
    CONSTRAINT "reviews_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS products_reviews (
    id SERIAL,
    product_id INTEGER, 
    review_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (review_id) REFERENCES reviews(id),
    CONSTRAINT "products_reviews_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS similars (
    id VARCHAR(10), 
    asin VARCHAR(10),
    CONSTRAINT "similars_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS products_similars (
    id SERIAL,
    product_id INTEGER,
    similar_id VARCHAR(10) ,
    FOREIGN KEY (similar_id) REFERENCES similars(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT "products_similars_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS groups (
    id SERIAL,
    title TEXT,
    CONSTRAINT "groups_pk" PRIMARY KEY ("id")
);

INSERT INTO groups (title) VALUES ('Book'), ('DVD'), ('Video'), ('Music') ON CONFLICT DO NOTHING;


-- Inserção dos products com similars


INSERT INTO products (id, asin, title, group_id, salesrank) VALUES (1, '0827229534', 'Patterns of Preaching: A Sermon Sampler', 1, 396585) RETURNING ID;

-- pega o id de retorno do produto atual e mocka 


INSERT INTO similars (asin) VALUES ('0804215715') RETURNING ID;

-- pega o id de retorno do similar e mocka

-- adiciona a relação dos dois direto

INSERT INTO products_similars (product_id, similar_id) VALUES (1,1);

INSERT INTO similars (asin) VALUES ('156101074X') RETURNING ID;
INSERT INTO products_similars (product_id, similar_id) VALUES (1, 2);

INSERT INTO similars (asin) VALUES ('0687023955') RETURNING ID;
INSERT INTO products_similars (product_id, similar_id) VALUES (1, 3);

INSERT INTO similars (asin) VALUES ('0687074231') RETURNING ID;
INSERT INTO products_similars (product_id, similar_id) VALUES (1, 4);

INSERT INTO similars (asin) VALUES ('082721619X') RETURNING ID;
INSERT INTO products_similars (product_id, similar_id) VALUES (1, 5);

-- repete pra todos similares (similares finalizado)

-- Fazer get de similares de um produto dado o id de um produto

SELECT products.id, similars.asin FROM products_similars JOIN products ON products.id = products_similars.product_id JOIN similars ON similars.id = products_similars.similar_id;

-- Inserção em categories de um produto (posição no array)

-- insere retornando id e mocka id
INSERT INTO categories (id, title, parent_id) VALUES (12370,'Sermons[12370]', 12360) RETURNING id;
INSERT INTO product_categories (product_id, category_id) VALUES (1, 12370);
-- id retornado: 12370
-- insere a relação a cada categoria inserida e repete pra cada uma delas (categories finalizado)
INSERT INTO categories (id, title, parent_id) VALUES (12368,'Preaching[12368]', 12360) RETURNING ID;
INSERT INTO product_categories (product_id, category_id) VALUES (1, 12368);

-- get de categories dado o id de um produto

SELECT products.id, categories.title, categories.parent_id FROM product_categories JOIN products ON product_categories.product_id = products.id JOIN categories ON product_categories.category_id = categories.id;

-- Inserção de reviews de um produto (posição no array)

 -- insere retornando id e mocka o id
INSERT INTO reviews (review_data, user_id, rating, votes, helpful) VALUES ('2000-7-28', 'A2JW67OY8U6HHK', 5, 10, 9) RETURNING ID;
-- insere a relação products_reviews a cada inserção usando id atual do produto com o id retornado da inserção de review

INSERT INTO products_reviews (product_id, review_id) VALUES (1, 1);
-- repete pra todos os outros até o fim do array (reviews finalizado)

INSERT INTO reviews (review_data, user_id, rating, votes, helpful) VALUES ('2003-12-14', 'A2VE83MZF98ITY', 5, 6, 5) RETURNING ID;

INSERT INTO products_reviews (product_id, review_id) VALUES (1, 2);

-- get reviews do produto dado um id do produto

SELECT products.id as product_id, reviews.user_id, reviews.review_data, reviews.rating, reviews.votes, reviews.helpful    FROM products_reviews JOIN products ON products_reviews.product_id = products.id JOIN reviews ON products_reviews.review_id = reviews.id;

-- get varia de asin or id do produto (apenas trocar qual é a busca no select)


INSERT INTO products (id, asin) VALUES (0, '0827229534') RETURNING ID;



-- Querys Dashboard

SELECT reviews.* FROM products_reviews JOIN products ON products.id=products_reviews.product_id JOIN reviews ON reviews.id = products_reviews.review_id WHERE products.id = 307 ORDER BY reviews.helpful DESC, reviews.rating DESC LIMIT 5;

SELECT reviews.* FROM products_reviews JOIN products ON products.id=products_reviews.product_id JOIN reviews ON reviews.id = products_reviews.review_id WHERE products.id = 307 ORDER BY reviews.helpful DESC, reviews.rating LIMIT 5;