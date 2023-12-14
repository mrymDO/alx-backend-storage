-- a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.


DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id_param INT)

BEGIN
    DECLARE total_weighted_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;
    
    SELECT SUM(c.score * p.weight) INTO total_weighted_score
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id_param;
    
    SELECT SUM(weight) INTO total_weight
    FROM projects;
    
    UPDATE users
    SET average_score = total_weighted_score / total_weight
    WHERE id = user_id_param;
END $$

DELIMITER ;
