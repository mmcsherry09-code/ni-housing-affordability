WITH annual_mortgage_rates AS (SELECT CAST(substr(Date, 1, 4) AS INTEGER) AS Year, AVG(mortgage_rate_75_ltv) AS rate_75_ltv, AVG(mortgage_rate_90_ltv) AS rate_90_ltv, AVG(mortgage_rate_95_ltv) AS rate_95_ltv FROM mortgage_rates GROUP BY CAST(substr(Date, 1, 4) AS INTEGER))

SELECT e.Year, e."Full-time" AS annual_earnings, h.house_price, ROUND(m.rate_75_ltv, 2) AS rate_75_ltv, ROUND(m.rate_90_ltv, 2) AS rate_90_ltv, ROUND(m.rate_95_ltv, 2) AS rate_95_ltv FROM earnings AS e

INNER JOIN house_prices AS h ON e.Year = h.Year

INNER JOIN annual_mortgage_rates AS m ON e.Year = m.Year

ORDER BY e.Year
