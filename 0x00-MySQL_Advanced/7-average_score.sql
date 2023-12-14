--  a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)

BEGIN
	DECLARE total_score FLOAT;
	DECLARE total_projects INT;

	SET total_score = 0;
	SET total_projects = 0;

	SELECT SUM(score) INTO total_score
	FROM corrections
        WHERE user_id = user_id;

        SELECT COUNT(*) INTO total_projects
        FROM corrections
        WHERE user_id = user_id;

	IF total_projects > 0 THEN
		UPDATE users
		SET average_score = total_score / total_projects
		WHERE id = user_id;
	END IF;
END $$

DELIMITER ;
