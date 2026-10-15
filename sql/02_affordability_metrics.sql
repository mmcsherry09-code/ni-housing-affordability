SELECT e.Year, e."Full-time" AS annual_earnings, h.house_price, r.annual_rent, ROUND(h.house_price / e."Full-time", 2) AS house_price_to_earnings, ROUND((r.annual_rent / e."Full-time") * 100, 2) AS rent_burden_percent

FROM earnings AS e 

INNER JOIN house_prices AS h ON e.Year = h.Year

INNER JOIN rents AS r ON e.Year = r.Year

ORDER BY e.Year; 