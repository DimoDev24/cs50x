-- 11. Titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated
SELECT m.title FROM movies m
JOIN ratings r ON r.movie_id = m.id
JOIN stars s ON s.movie_id = m.id
JOIN people p ON s.person_id = p.id
WHERE p.name LIKE 'Chadwick Boseman'
ORDER BY r.rating DESC LIMIT 5;
