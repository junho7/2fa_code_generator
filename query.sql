-- avalaai.2fa_code definition
CREATE TABLE `2fa_code` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `decimal` bigint unsigned DEFAULT NULL,
  `hexadecimal` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `is_sent` tinyint(1) DEFAULT NULL,
  `is_blocked` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Populate the table with dummy numbers to generate the `id` up to 16**8
-- 1 billion rows per an execution
INSERT INTO `2fa_code_sql` (`decimal`, `hexadecimal`, `is_sent`, `is_blocked`)
SELECT 1, lpad(hex(0), 8, 0), 0, 0
  FROM
(
select a.N + b.N * 10 + c.N * 100 + d.N * 1000 + e.N * 10000 + f.N * 100000 + g.N * 1000000 + h.N * 10000000 + i.N * 1000000000 + 1 N
from (select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) a
      , (select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) b
      , (select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) c
      , (select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) d
      , (select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) e
      , (select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) f
      , (select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) g
      , (select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) h      
      , (select 0 as N union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) i      
) t
;

-- Update `decimal`, `hexadecimal` with sequential number from `id`
CREATE DEFINER=`root`@`localhost` PROCEDURE `BatchUpdate`(
    start_id BIGINT UNSIGNED,
    end_id BIGINT UNSIGNED,
    batch_size INT
)
BEGIN
   DECLARE batch_start_id BIGINT UNSIGNED DEFAULT start_id;
    DECLARE batch_end_id BIGINT UNSIGNED DEFAULT start_id + batch_size - 1;    

 	WHILE batch_end_id <= end_id DO
 
         SELECT CONCAT('UPDATING FROM ', batch_start_id, ' TO: ', batch_end_id) as log;
         UPDATE 2fa_code_sql SET `decimal` = `id` - 1, `hexadecimal` = lpad(hex(`id`-1), 8, 0) WHERE id BETWEEN batch_start_id and batch_end_id;
 
         SET batch_start_id = batch_start_id + batch_size;
         SET batch_end_id = batch_end_id + batch_size;         
	END WHILE;
END