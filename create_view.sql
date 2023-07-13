CREATE VIEW ViewTurmasPorDepartamento AS
SELECT d.Nome_dep AS Departamento, COUNT(*) AS NumTurmas
FROM Turma t
JOIN Departamento d ON t.Departamento_Codigo_dep = d.Codigo_dep
GROUP BY d.Codigo_dep, d.Nome_dep;

SELECT * FROM ViewTurmasPorDepartamento;

-- Isso retornará o número de turmas por departamento, mostrando o nome do departamento e a quantidade de turmas em cada um.
