-- INSERÇÕES  AVANÇADAS
-- Turma
LOAD DATA INFILE '/var/lib/mysql-files/turmas_2023-1.csv'
INTO TABLE Turma
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Turma, Periodo, Nome_Professor, Horario, Vagas_ocupadas, @Total_vagas, Local, Disciplina_Codigo_disc, Departamento_Codigo_dep)
SET Total_vagas = NULLIF(@Total_vagas, '');
-- Departamento

LOAD DATA INFILE '/var/lib/mysql-files/departamentos_2023-1.csv' 
INTO TABLE Departamento FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Disciplina
LOAD DATA INFILE '/var/lib/mysql-files/disciplinas_2023-1.csv' 
INTO TABLE Disciplina 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

-- Professor
LOAD DATA INFILE '/var/lib/mysql-files/professor.csv'
INTO TABLE Professor
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Departamento_Codigo_dep, Turma_Nome_Professor);

-- INSERÇÕES BÁSICAS

-- Inserção de dados na tabela Estudante
INSERT INTO `mydb`.`Estudante` (`Matricula`, `Senha`, `Login`, `Email`, `Curso`, `Imagem`, `IsAdmin`) VALUES
(123456789, 'senha123', 'usuario1', 'usuario1@email.com', 'Ciência da Computação', NULL, 0),
(987654321, 'senha456', 'usuario2', 'usuario2@email.com', 'Engenharia Civil', NULL, 0),
(543216789, 'senha789', 'usuario3', 'usuario3@email.com', 'Administração', NULL, 1);

-- Inserção de dados na tabela Departamento
INSERT INTO `mydb`.`Departamento` (`Codigo_dep`, `Nome_dep`) VALUES
(1, 'Departamento de Ciência da Computação'),
(2, 'Departamento de Engenharia Civil'),
(3, 'Departamento de Administração');

-- Inserção de dados na tabela Disciplina
INSERT INTO `mydb`.`Disciplina` (`Codigo_disc`, `Nome_disc`, `Departamento_Codigo_dep`) VALUES
('DSC001', 'Introdução à Programação', 1),
('DSC002', 'Banco de Dados', 2),
('DSC003', 'Engenharia de Software', 1);

-- Inserção de dados na tabela Turma
INSERT INTO `mydb`.`Turma` (`Id_Turma`, `Turma`, `Periodo`, `Nome_Professor`, `Horario`, `Vagas_ocupadas`, `Total_vagas`, `Local`, `Disciplina_Codigo_disc`, `Departamento_Codigo_dep`) VALUES
(1, 1, '2023/1', 'Professor A', '08:00 - 10:00', 25, 30, 'Sala 101', 'DSC001', 1),
(2, 1, '2023/1', 'Professor B', '10:00 - 12:00', 15, 20, 'Sala 102', 'DSC001', 1),
(3, 2, '2023/1', 'Professor C', '14:00 - 16:00', 10, 30, 'Sala 103', 'DSC002', 2);

-- Inserção de dados na tabela Professor
INSERT INTO `mydb`.`Professor` (`Id_Professor`, `Departamento_Codigo_dep`, `Turma_Nome_Professor`) VALUES
(1, 1, 'Professor A'),
(2, 1, 'Professor B'),
(3, 2, 'Professor C');

-- Inserção de dados na tabela AvaliaTurma
INSERT INTO `mydb`.`AvaliaTurma` (`Id_aval`, `Estudante_Matricula`, `Turma_Id_Turma`, `Texto`, `Score`, `DataHora`) VALUES
(1, 123456789, 1, 'Excelente turma!', 5, NOW()),
(2, 987654321, 2, 'Ótimo professor!', 4, NOW()),
(3, 543216789, 3, 'Turma bem organizada', 4, NOW());


-- Inserção de dados na tabela DenunciaAvTurma
INSERT INTO `mydb`.`DenunciaAvTurma` (`idDenunciaAvTurma`, `AvaliaTurma_Id_aval`, `Estudante_Matricula`) VALUES
(1, 1, 543216789),
(2, 2, 123456789),
(3, 3, 987654321);

-- Inserção de dados na tabela AvaliaProf
INSERT INTO `mydb`.`AvaliaProf` (`idAvaliaProf`, `Estudante_Matricula`, `Professor_Id_Professor`, `Texto`, `Score`, `DataHora`) VALUES
(1, 543216789, 1, 'Ótimo professor!', 5, NOW()),
(2, 123456789, 2, 'Professor atencioso', 4, NOW()),
(3, 987654321, 3, 'Professor experiente', 4, NOW());

-- Inserção de dados na tabela DenunciaAvProf
INSERT INTO `mydb`.`DenunciaAvProf` (`idDenunciaAvProf`, `AvaliaProf_idAvaliaProf`, `Estudante_Matricula`) VALUES
(1, 1, 987654321),
(2, 2, 543216789),
(3, 3, 123456789);

-- Exclusão de dados da tabela Estudante
DELETE FROM Estudante WHERE Matricula IN (123456789, 987654321, 543216789);

-- Exclusão de dados da tabela Departamento
DELETE FROM Departamento WHERE Codigo_dep IN (1, 2, 3);

-- Exclusão de dados da tabela Disciplina
DELETE FROM Disciplina WHERE Codigo_disc IN ('DSC001', 'DSC002', 'DSC003');

-- Exclusão de dados da tabela Turma
DELETE FROM Turma WHERE Id_Turma IN (1, 2, 3);

-- Exclusão de dados da tabela Professor
DELETE FROM Professor WHERE Id_Professor IN (1, 2, 3);

-- Exclusão de dados da tabela AvaliaTurma
DELETE FROM AvaliaTurma WHERE Id_aval IN (1, 2, 3);

-- Exclusão de dados da tabela DenunciaAvTurma
DELETE FROM DenunciaAvTurma WHERE idDenunciaAvTurma IN (1, 2, 3);

-- Exclusão de dados da tabela AvaliaProf
DELETE FROM AvaliaProf WHERE idAvaliaProf IN (1, 2, 3);

-- Exclusão de dados da tabela DenunciaAvProf
DELETE FROM DenunciaAvProf WHERE idDenunciaAvProf IN (1, 2, 3);
