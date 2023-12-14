-- creates a function SafeDiv that divides (and returns) the first by the second number
-- or returns 0 if the second number is equal to 0.

DROP FUNCTION IF IT EXISTS SafeDiv;

DELIMITER $$

CREATE DUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
	DECLARE result FLOAT DEFAULT 0;
	IF b == 0 THEN
		RETURN 0;
	ELSE
		RETURN a / b;
	END IF;
END $$

DELIMITER ;
