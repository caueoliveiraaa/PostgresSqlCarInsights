-- Return the sum of car prices
select sum(price), brand
from Car
group by brand;