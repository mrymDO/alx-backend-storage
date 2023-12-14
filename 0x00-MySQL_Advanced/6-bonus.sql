-- a stored procedure AddBonus that adds a new correction for a student

DROP PROCEDURE IF EXISTS AddBonus;

DELIMITER $$

CREATE PROCEDURE AddBonus(
	user_id INT,
	project_name VARCHAR(255),
	score FLOAT
)
BEGIN
	DECLARE project_id INT DEFAULT 0;
	DECLARE project_count INT DEFAULT 0;

        -- Check if the project already exists
        SELECT id INTO project_id
        FROM projects
        WHERE name = project_name;

        -- If the project does not exist, create it
        SELECT COUNT(id) INTO project_count FROM projects
	WHERE name = project_name;
	IF project_count = 0 THEN
            INSERT INTO projects (name) VALUES (project_name);
            SET project_id = LAST_INSERT_ID();
        END IF;

	SELECT user_id, project_id, score;
	SELECT project_name, project_id;

	 INSERT INTO corrections (user_id, project_id, score)
        VALUES (
                user_id,
                project_id,
                score
        );
END $$

DELIMITER ;
