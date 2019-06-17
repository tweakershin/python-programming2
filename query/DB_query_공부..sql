SELECT *, price * quantity as total 
FROM sample34;

-- 수치연산
SELECT *, price * quantity as total
FROM sample34
WHERE price*quantity > 3000;

-- \
SELECT *,
CASE a
	WHEN 1 THEN '남자'
    WHEN 2 THEN '여자'
END AS '성별'
FROM sample37;

--
SELECT *
FROM sample41;

-- INSERT
DESC sample41;

INSERT INTO sample41 
VALUES(1, '안녕하세요.', '2019-05-05');

SELECT *
FROM sample41;

INSERT 
INTO sample41(no, a)
VALUES(2, '안녕히계세요.');

INSERT 
INTO sample41(a, no)
VALUES('SQL은 참 재미있어요.', 3);

INSERT 
INTO sample41(no, a, b)
VALUES(4, NULL, '2018-05-05');

SELECT *
FROM sample41;

-- USE <DATABASE>
SHOW DATABASES;
USE northwind;
USE sample;

SELECT *
FROM northwind.categories;
-- --------------


-- DELETE
SELECT *
FROM sample41;

DELETE 
FROM sample41
WHERE no=2;

SELECT *
FROM sample41;

DELETE 
FROM sample41;

SELECT *
FROM sample41;

-- INSERT 복습
DESC sample41;

INSERT 
INTO sample41(no, a)
VALUES (1, '시작하자.');

INSERT
INTO sample41
VALUES (2, "끝내자", '2018-05-05');

SELECT *
FROM sample41;

-- UPDATE문
UPDATE sample41
SET a="즐거운 SQL"
WHERE no=1;

SELECT *
FROM sample41;

UPDATE sample41
SET a=NULL
WHERE no=2;

SELECT *
FROM sample41;

UPDATE sample41
SET a='UPDATE', b='2019-06-25';

SELECT *
FROM sample41;

-- 집계함수
SELECT *
FROM sample51;

-- COUNT
SELECT COUNT(*)
FROM sample51;

SELECT COUNT(*)
FROM sample51
WHERE name='A';

SELECT *
FROM sample51;

SELECT 
	count(no), 
	COUNT(name), 
    COUNT(quantity)
FROM sample51;

SELECT DISTINCT name
FROM sample51;

SELECT count(distinct name)
FROM sample51;

SELECT *
FROM sample51;

SELECT SUM(quantity)
FROM sample51;

SELECT AVG(quantity)
FROM sample51;

SELECT MAX(quantity)
FROM sample51;

SELECT MIN(quantity)
FROM sample51;

SELECT *FROM sample51;

-- GROUP BY
SELECT *FROM sample51;

SELECT name, COUNT(name)
FROM sample51
GROUP BY name;

SELECT name, COUNT(name), SUM(quantity)
FROM sample51
GROUP BY name;

-- HAVING
SELECT name, COUNT(name), SUM(quantity)
FROM sample51
GROUP BY name
HAVING SUM(quantity)<5;

-- 서브쿼리
SELECT *
FROM sample54;

-- sample54의 min(a)를 가지는 row.
SELECT *
FROM sample54
WHERE a;

SELECT MIN(a)
FROM sample54;

SELECT *
FROM sample54
WHERE a = (
	SELECT MIN(a)
	FROM sample54
);

SELECT *
FROM sample54
WHERE a = (
	SELECT MAX(a)
	FROM sample54
);

UPDATE sample54
SET a = 1
WHERE a = (
	SELECT max(a)
    FROM sample54
);

SELECT *
FROM (
	SELECT *
    FROM sample54
) as s;


SELECT *
FROM sample54;


-- EXISTS
SELECT *
FROM sample551;

SELECT *
FROM sample552;


UPDATE sample551
SET a = "있음"
WHERE
EXISTS (
	SELECT * 
    FROM sample552
    WHERE no2=no
);

UPDATE sample551
SET a = "없음"
WHERE
NOT EXISTS (
	SELECT * 
    FROM sample552
    WHERE no2=no
);

SELECT *
FROM sample551
WHERE no IN (3, 5);

SELECT *
FROM sample551
WHERE no IN (
	SELECT no2
    FROM sample552
);

-- join, cartesian product
SELECT *
FROM sample72_x;

SELECT *
FROM sample72_y;

SELECT *
FROM sample72_x, sample72_y;


-- JOIN 
DESC `상품`;
SELECT *
FROM `상품`;

DESC `재고수`;
SELECT *
FROM `재고수`;


SELECT *
FROM `상품`;

SELECT *
FROM `재고수`;

SELECT *
FROM `상품`, `재고수`;

SELECT *
FROM `상품`, `재고수`
WHERE `상품`.`상품코드` = `재고수`.`상품코드`;

-- join
SELECT *
FROM `상품`
JOIN `재고수`
ON `상품`.`상품코드` = `재고수`.상품코드;


SELECT *
FROM sample72_x;

SELECT *
FROM sample72_y;



SELECT *
FROM sample551;

SELECT *
FROM sample552;


-- DDL
-- TABLE DEFINE
CREATE TABLE books(
	book_id INT NOT NULL,
    title VARCHAR(50),
    author_id INT
);

DESC books;

DROP TABLE books;

CREATE TABLE books(
	book_id INT NOT NULL,
    title VARCHAR(50),
    content TEXT DEFAULT '' NOT NULL,
    author_id INT,
    CONSTRAINT pkey_sample 
    PRIMARY KEY (book_id)
);
DESC BOoks;

ALTER TABLE books 
ADD published_at DATETIME;

ALTER TABLE books
MODIFY title VARCHAR(100);

ALTER TABLE books
DROP author_id;

DESC books;


CREATE INDEX BTREE ON books(title);

DESC books;

DROP INDEX BTREE on books;

DESC books;


-- View 
SELECT * FROM sample54;

CREATE VIEW sample_view67 
AS SELECT * FROM sample54;

SELECT * FROM sample_view67;

-- TRANSACTION
DESC books;
SELECT * 
FROM books;

START TRANSACTION;
INSERT INTO books 
values(1, '연금술사', 
"금을 찾아 떠나는 여행 with 히피",
NULL);
ROLLBACK;

INSERT INTO books 
values(2, '다크 메이지', 
"어두운 메이지", NULL);
INSERT INTO books 
values(3, '채식주의자', 
"육식은 싫어요.", NULL);

COMMIT;
