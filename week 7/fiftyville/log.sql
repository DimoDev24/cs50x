-- Keep a log of any SQL queries you execute as you solve the mystery.

-- I wanted to view more information about the incident
SELECT description FROM crime_scene_reports
WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';
-- The three witnesses mentioned the bakery ROBE 10:15 Littering? 16:36

-- I want to see the interviews from 7/28
SELECT transcript FROM interviews
WHERE year = 2025 AND month = 7 AND day = 28;
-- the thief exited the bakery at that hour. Someone he recognizes?? He was withdrawing money at the ATM before.
-- After bakery, call less than minute. Planning taking the earliest flight tomorrow (7/29). The other person bought the ticket...

-- This SELECT tells me the activity and the license plate of the cars that leave in the bakery
SELECT activity, license_plate FROM bakery_security_logs
WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10;
-- The list is: 5P2BI95 | 94KL13X | 6P58WS2 | 4328GD8 | G412CB7 | L93JTIZ | 322W7JE | 0NTHK55 | 1106N58

-- If the theft leave the bakery at 10, he might entered at 9... I want to check if any plate coincides.
SELECT activity, license_plate FROM bakery_security_logs
WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 9;
-- These are the plates that coincides... We can discard some but not all... 4328GD8 | 5P2BI95 | 6P58WS2 | G412CB7

-- The witness sayed that he was withdrawing money at Leggett Street
SELECT id, account_number, amount FROM atm_transactions
WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';
-- The list:
--+-----+----------------+--------+
--| id  | account_number | amount |
--+-----+----------------+--------+
--| 246 | 28500762       | 48     |
--| 264 | 28296815       | 20     |
--| 266 | 76054385       | 60     |
--| 267 | 49610011       | 50     |
--| 269 | 16153065       | 80     |
--| 288 | 25506511       | 20     |
--| 313 | 81061156       | 30     |
--| 336 | 26013199       | 35     |
--+-----+----------------+--------+

-- Okay we are going somewhere, now we will check the plates of the person that the bank_account matches with the transactions
SELECT license_plate FROM people p
JOIN bank_accounts b ON b.person_id = p.id
WHERE b.account_number = (
    SELECT account_number FROM atm_transactions
    WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
);
-- Bingo! We have the plate '4328GD8', and did you remember? It's the same that the one who exited the backery!

-- So we match the plate with the person associated...
SELECT name, phone_number, passport_number FROM people
WHERE license_plate = '4328GD8';
-- Okay we have the theft! the phone and the passport will be very usefull now.
--+------+----------------+-----------------+
--| name |  phone_number  | passport_number |
--+------+----------------+-----------------+
--| Luca | (389) 555-5198 | 8496433585      |
--+------+----------------+-----------------+

-- I put Luca's number in phone_calls
SELECT receiver FROM phone_calls
WHERE caller = '(389) 555-5198' AND year = 2025 AND month = 7
AND day = 28 AND duration <= 60;
-- But there's nothing... that's because Luca wasn't the caller?


-- Maybe he's the receiver...
SELECT caller FROM phone_calls
WHERE receiver = '(389) 555-5198' AND year = 2025 AND month = 7 AND day = 28 AND duration <= 60;
-- There is! The caller number is: (609) 555-5876

-- I just thought I can do a subconsult instead of hard-putting his number...
SELECT name, passport_number FROM people
WHERE phone_number = (
    SELECT caller FROM phone_calls
    WHERE receiver = '(389) 555-5198' AND year = 2025 AND month = 7 AND day = 28 AND duration <= 60
);
-- Yeah! The name of the accomplice is:
--+---------+-----------------+
--|  name   | passport_number |
--+---------+-----------------+
--| Kathryn | 6121106406      |
--+---------+-----------------+

-- I will try to see the flight_id of the fly that took Luca
SELECT flight_id, seat FROM passengers
WHERE passport_number = (
    SELECT passport_number FROM people
    WHERE license_plate = '4328GD8'
);
-- Mmmmph... There are 3 of them...
--+-----------+------+
--| flight_id | seat |
--+-----------+------+
--| 11        | 5D   |
--| 36        | 7B   |
--| 48        | 7C   |
--+-----------+------+

-- But if both Luca and Kathryn are in the same flight...
SELECT flight_id FROM passengers
WHERE passport_number IN ('6121106406','8496433585');
-- Strange... They weren't in the same flight?
--+-----------+
--| flight_id |
--+-----------+
--| 11        |
--| 34        |
--| 36        |
--| 48        |
--+-----------+

-- I will try to see the number of flights that matches with that...
SELECT id FROM flights
WHERE year = 2025 AND month = 7 AND day = 29;
-- I understand!! The accomplice didn't fly! She only bought the ticket to Luca because he's flight ID matches...
--+----+
--| id |
--+----+
--| 18 |
--| 23 |
--| 36 |
--| 43 |
--| 53 |
--+----+

-- Now I only must discover the destination airport that matches with the flight ID
SELECT full_name, city FROM airports
WHERE id = (
    SELECT destination_airport_id FROM flights
    WHERE id = 36
);
-- YES! I discover where Luca escaped!
--+-------------------+---------------+
--|     full_name     |     city      |
--+-------------------+---------------+
--| LaGuardia Airport | New York City |
--+-------------------+---------------+
