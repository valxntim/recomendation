DELIMITER //

CREATE PROCEDURE ContarAdmins()
BEGIN
  SELECT COUNT(*) AS NumAdmins FROM Estudante WHERE IsAdmin = 1;
END //

DELIMITER ;


CALL ContarAdmins();
