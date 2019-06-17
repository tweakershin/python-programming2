USE northwind;
-- Q. 런던에 위치 공급자(Supplier)가 
-- 생산한 상품 목록 조회 
-- : 도시명, 공급자명, 상품명, 상품가격
select S.city, S.companyName , 
	   P.productname, p.unitPrice 
from products P, suppliers S
where P.supplierid = S.supplierid
and S.city = 'London';

SELECT city, companyName, 
		productName, unitPrice
from products P
join suppliers S
on P.supplierID = S.supplierID
where S.city = 'london';


-- Q. 분류가 Seafood 인 상품 목록 (모든 컬럼 조회) : 분류, 상품 모든 컬럼


select C.categoryname, P.* 
from categories as C, products as P
where C.categoryid = P.categoryid
and C.categoryname = 'Seafood';


-- Q. 공급자(Supplier) 국가별, 
-- 카테고리 별 상품 개수, 평균가격 
-- : 국가명, 카테고리명, 상품개수, 평균가격
select S.country, C.categoryname, 
	   COUNT(P.unitPrice) as prod_num, 
       AVG(P.unitPrice) as avg_price
from suppliers S, categories C, products P
where S.supplierid = P.supplierid
and C.categoryid = P.categoryid
group by S.country, C.categoryname;

-- 2번째 방법
select S.country, C.categoryname, 
		COUNT(P.unitPrice) as prod_num, 
		AVG(P.unitPrice) as avg_price
from suppliers S
join products P
on S.supplierid = P.supplierid
join categories C
on C.categoryid = P.categoryid
group by S.country, C.categoryName;


-- Q. 상품 카테고리별, 국가별, 도시별 
-- 주문수량 2개 이상인 목록 
-- : 카테고리명, 국가명, 도시명, 주문건수
select C.categoryname, CU.country, 
		CU.city, 
        SUM(D.quantity) as 'order_total'
from products P, categories C, 
	customers CU, orders O, orderdetails D
where P.productid = D.productid
and P.categoryid = C.categoryid
and CU.customerid = O.customerid
and O.orderid = D.orderid
group by C.categoryname, CU.country, CU.city
Having SUM(D.quantity) > 2;


-- Q. 주문자, 주문정보, 직원정보, 배송자정보 통합 조회 : 고객컬럼 전체, 주문정보 컬럼 전체, 배송자 정보 컬럼 전체 (4개 테이블 조인)
select * 
from customers C, orders O, 
	 employees E, shippers S
where C.customerid = O.customerid
and E.employeeid = O.employeeid
and S.shipperid = O.shipVia;
desc orders;

-- 다른 방법 ( join)
select * 
from customers C
join orders O
on C.customerId = O.customerid
join employees E
on E.employeeid = O.employeeid
join  Shippers S
on S.shipperid = O.shipVia;

-- Q. 판매량(Quantity) 상위 TOP 3 공급자(supplier) 목록 : 공급자 명, 판매량, 판매금액
select S.companyName , SUM(D.quantity) as total_sell , SUM(D.quantity*P.unitPrice) as total_money
from products P, orders O, orderdetails D, suppliers S
where p.productid = D.productid
and O.orderid = D.orderid
and P.supplierid = S.supplierid
group by S.companyName
order by total_sell desc
limit 3;



-- Q. 상품(Product) 분류(Category)별, 고객 지역별(City) 판매량 순위 : 순위, 카테고리명, 고객지역명, 판매량
select Cgr.CategoryName , C.City , sum(OD.Quantity) as total_sell
from Products P, Categories Cgr, Customers C, Orders O, OrderDetails OD
where P.CategoryID = Cgr.CategoryID
and C.CustomerID = O.CustomerID 
and O.OrderID = OD.OrderID 
and OD.ProductID = P.ProductID
group by CategoryName, C.City
order by sum(OD.Quantity) desc;




-- Q. 고객 국가가 USA이고, 상품별 판매량(Quantity 수량 합계) 순위( : 국가명, 상품명, 판매량, 판매금액
select C.Country , P.ProductName , 
	  SUM(OD.Quantity) total_sell, SUM(OD.Quantity * P.unitPrice) total_money
from Customers C, Orders O, OrderDetails OD, Products P
where C.CustomerID = O.CustomerID
and O.OrderID = OD.OrderID
and OD.ProductID = P.ProductID
and C.Country = 'USA'
group by C.Country, P.ProductName
Order by total_sell DESC;





-- Q. Supplier의 국가가 Germany인 상품 카테고리별 상품 수 : 국가명, 카테고리명, 상품수
select S.Country, C.CategoryName, COUNT(*) product_num
from suppliers S, Products P, Categories C
where S.supplierID =  P.supplierID
and P.CategoryID = C.CategoryID
and S.Country ='Germany'
group by S.Country, C.CategoryName;





-- Q. 월별 판매량 및 판매금액 : 연도, 월, 판매량, 판매금액
SELECT YEAR(orderDate), MONTH(orderDate), sum(quantity), sum(Unitprice*quantity)
from orders O, orderdetails OD
where O.OrderID = OD.OrderID
group by YEAR(orderDate), MONTH(orderDate);







      
