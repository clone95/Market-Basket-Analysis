--#############
--# Paulo Trigo
--#############


----------
-- DB name
----------
\set dataBase db_e_commerce_sample
;

-----------------------
-- Remode and Create DB
-----------------------

\echo "Remove Data Base" :dataBase
;

DROP DATABASE IF EXISTS :dataBase
;


\echo "Create Data Base" :dataBase
;

------------------------------------------------------------------------
-- The database is created considering its template
-- if no template is desired just remove the "TEMPLATE = my_db" parameter
------------------------------------------------------------------------
-- CREATE DATABASE :dataBase TEMPLATE = my_db
CREATE DATABASE :dataBase
;


--#############
--# Paulo Trigo
--#############



--==============
-- DB connection
--==============
\set dataBase db_e_commerce_sample
;
\set userName postgres
;
\connect :dataBase :userName
;
--==========================
--==========================


-------------------------------
-- create the relational schema
-------------------------------
DROP TABLE IF EXISTS TRACK;
--------------------------------
CREATE TABLE TRACK
(
tracking_record_id BIGINT NOT NULL,
date_time          TIMESTAMP WITHOUT TIME ZONE NOT NULL,
user_gui           VARCHAR,
campaing_id		   VARCHAR,
product_gui        VARCHAR,
company 		   VARCHAR,
link 			   VARCHAR,
tracking_id        VARCHAR,
meio 			   VARCHAR,
ip				   VARCHAR,
browser			   VARCHAR,
session_id		   VARCHAR,
referer			   VARCHAR,
cookie_id		   VARCHAR
)
;

-------------------------------
-- entity integrity constraints
-- (primary key and unique)
-------------------------------

ALTER TABLE TRACK
ADD CONSTRAINT pk_TRACK
PRIMARY KEY(tracking_record_id)
;



----------------------------------------
-- referential integrity constraints
-- (foreign key)
----------------------------------------
-- ALTER TABLE track
-- ADD CONSTRAINT fk1_track
--    FOREIGN KEY( C1_R1 )
--    REFERENCES R1( C1 )
;


--#############
--# Paulo Trigo
--#############


--==============
-- DB connection
--==============
\set dataBase db_e_commerce_sample
;
\set userName postgres
;
\connect :dataBase :userName
;
--==========================
--==========================


-- additional information about "client_encoding" in:
-- http://www.postgresql.org/docs/9.3/static/multibyte.html
-- \encoding WIN1250
\encoding UTF8
;




---------------------------------
DELETE FROM TRACK;
---------------------------------
-- Important info about \copy (psql instruction) and copy (sql statement)
-- cf., http://www.postgresql.org/docs/9.3/static/sql-copy.html
-- Do not confuse COPY with the psql instruction \copy.
-- \copy invokes COPY FROM STDIN or COPY TO STDOUT, and then fetches/stores the data in a file accessible to the psql client.
-- Thus, file accessibility and access rights depend on the client rather than the server when \copy is used.
-- 
-- Therefore, given the above information we will use the ~copy psql instruction (no problems with client permissions
--
\COPY track FROM 'C:/Users/jack/Desktop/Project B/z_dataset_JAN.csv' WITH DELIMITER ',' CSV HEADER 



--========================
-- Testing the copyed data
--========================
-- SELECT * FROM TRACK
-- LIMIT 100
;


--#############
--# Paulo Trigo
--#############


--==============
-- DB connection
--==============
\set dataBase db_e_commerce_sample
;
\set userName postgres
;
\connect :dataBase :userName
--==========================
--==========================


-- additional information about "client_encoding" in:
-- http://www.postgresql.org/docs/9.6/static/multibyte.html
-- \encoding WIN1250
;



---------------------------------
DROP VIEW IF EXISTS v_export;
DROP VIEW IF EXISTS v_number_of_events_per_session_number_of_cookies;
DROP VIEW IF EXISTS v_number_of_cookies_number_of_sessions;
DROP VIEW IF EXISTS v_cookie_number_of_sessions;
DROP VIEW IF EXISTS v_cookie_session_number_of_events;
---------------------------------



--=============================================================================
-- total number of events (each tuple is an event)
--=============================================================================
CREATE VIEW total_events as 
SELECT COUNT(*) as total_events
FROM track
;



--=============================================================================
-- total number of distinct cookies (visitors)
--=============================================================================
CREATE VIEW n_distinct_cookies as 
SELECT COUNT(*) AS total_number_of_cookies
FROM (SELECT DISTINCT cookie_id FROM track) AS T
;



--=============================================================================
-- aggregate (group) cookies and sessions and get the total number of events
--=============================================================================
CREATE VIEW v_cookie_session_number_of_events( cookie_id, session_id, number_of_events_per_session )
 AS
 SELECT cookie_id, session_id, COUNT( * ) as number_of_events_per_session
 FROM track
GROUP BY track.session_id, track.cookie_id

;





--=============================================================================
-- aggregate cookie and get the total number of sessions (for each cookie)
-- and the total number of events for each session
--=============================================================================
CREATE VIEW v_cookie_number_of_sessions( cookie_id, number_of_sessions, number_of_events )
AS
SELECT cookie_id, COUNT(session_id), SUM(number_of_events_per_session) AS a FROM v_cookie_session_number_of_events
GROUP BY cookie_id
ORDER BY a DESC;
;





--=============================================================================
-- aggregate number of sessions and get total cookies (visitors) at each session
--=============================================================================
CREATE VIEW v_number_of_cookies_number_of_sessions( number_of_cookies, number_of_sessions ) AS
SELECT number_of_sessions, COUNT(cookie_id) FROM v_cookie_number_of_sessions
GROUP BY number_of_sessions
ORDER BY number_of_sessions;
;





--=============================================================================
-- aggregate the number of events per session and get the distribution of
-- the number of cookies (visitors)
--=============================================================================
CREATE VIEW v_number_of_events_per_session_number_of_cookies 
(number_of_events_per_session, number_of_cookies) 
AS SELECT number_of_events_per_session, count(cookie_id)
	FROM v_cookie_session_number_of_events
	GROUP BY number_of_events_per_session
	ORDER BY number_of_events_per_session DESC;





--=============================================================================
-- build a view for the data to be exported and to be transformed into a basket
-- this may be different depending on the basket you want to build
--=============================================================================
CREATE VIEW v_export( cookie_id, session_id, product_gui )
AS
SELECT T1.cookie_id, session_id, product_gui
FROM ( SELECT *
       FROM v_cookie_number_of_sessions
       WHERE number_of_sessions >= 5 and number_of_sessions <= 30 ) AS T1
     INNER JOIN
     track AS T2
     ON ( T1.cookie_id = T2.cookie_id )
WHERE product_gui NOT IN ( 'open', 'home' )
ORDER BY cookie_id, session_id, product_gui  -- commented for final dataset as this may be too resource consuming
;


-- SELECT *
-- FROM v_export
;






