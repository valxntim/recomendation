-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- Criação da tabela Estudante
CREATE TABLE IF NOT EXISTS `mydb`.`Estudante` (
  `Matricula` INT(9) NOT NULL,
  `Senha` VARCHAR(100) NOT NULL,
  `Login` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Curso` VARCHAR(45) NULL,
  `Imagem` MEDIUMBLOB NULL,
  `IsAdmin` TINYINT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Matricula`),
  UNIQUE INDEX `Login_UNIQUE` (`Login` ASC) VISIBLE,
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC) VISIBLE
) ENGINE = InnoDB;

-- Criação da tabela Departamento
CREATE TABLE IF NOT EXISTS `mydb`.`Departamento` (
  `Codigo_dep` INT NOT NULL,
  `Nome_dep` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`Codigo_dep`)
) ENGINE = InnoDB;

-- Criação da tabela Disciplina
CREATE TABLE IF NOT EXISTS `mydb`.`Disciplina` (
  `Codigo_disc` VARCHAR(20) NOT NULL,
  `Nome_disc` VARCHAR(100) NULL,
  `Departamento_Codigo_dep` INT NOT NULL,
  PRIMARY KEY (`Codigo_disc`),
  INDEX `fk_Disciplina_Departamento_idx` (`Departamento_Codigo_dep` ASC) VISIBLE,
  CONSTRAINT `fk_Disciplina_Departamento`
    FOREIGN KEY (`Departamento_Codigo_dep`)
    REFERENCES `mydb`.`Departamento` (`Codigo_dep`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Criação da tabela Turma
CREATE TABLE IF NOT EXISTS `mydb`.`Turma` (
  `Id_Turma` INT NOT NULL AUTO_INCREMENT,
  `Turma` INT NOT NULL,
  `Periodo` VARCHAR(10) NOT NULL,
  `Nome_Professor` VARCHAR(100) NOT NULL,
  `Horario` VARCHAR(100) NOT NULL,
  `Vagas_ocupadas` INT NULL,
  `Total_vagas` INT NULL,
  `Local` VARCHAR(90) NULL,
  `Disciplina_Codigo_disc` VARCHAR(20) NOT NULL,
  `Departamento_Codigo_dep` INT NOT NULL,
  PRIMARY KEY (`Id_Turma`, `Turma`, `Periodo`, `Nome_Professor`, `Horario`),
  INDEX `fk_Turma_Disciplina1_idx` (`Disciplina_Codigo_disc` ASC) VISIBLE,
  INDEX `fk_Turma_Departamento1_idx` (`Departamento_Codigo_dep` ASC) VISIBLE,
  INDEX `idx_Turma_Nome_Professor` (`Nome_Professor` ASC) VISIBLE, -- Adicionado o índice nesta linha
  CONSTRAINT `fk_Turma_Disciplina1`
    FOREIGN KEY (`Disciplina_Codigo_disc`)
    REFERENCES `mydb`.`Disciplina` (`Codigo_disc`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Turma_Departamento1`
    FOREIGN KEY (`Departamento_Codigo_dep`)
    REFERENCES `mydb`.`Departamento` (`Codigo_dep`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;


-- Criação da tabela AvaliaTurma
CREATE TABLE IF NOT EXISTS `mydb`.`AvaliaTurma` (
  `Id_aval` INT NOT NULL AUTO_INCREMENT,
  `Estudante_Matricula` INT(9) NOT NULL,
  `Turma_Id_Turma` INT NOT NULL,
  `Texto` VARCHAR(100) NOT NULL,
  `Score` INT NOT NULL,
  `DataHora` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id_aval`),
  INDEX `fk_AvaliaTurma_Estudante1_idx` (`Estudante_Matricula` ASC) VISIBLE,
  INDEX `fk_AvaliaTurma_Turma1_idx` (`Turma_Id_Turma` ASC) VISIBLE,
  CONSTRAINT `fk_AvaliaTurma_Estudante1`
    FOREIGN KEY (`Estudante_Matricula`)
    REFERENCES `mydb`.`Estudante` (`Matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_AvaliaTurma_Turma1`
    FOREIGN KEY (`Turma_Id_Turma`)
    REFERENCES `mydb`.`Turma` (`Id_Turma`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Criação da tabela Professor
CREATE TABLE IF NOT EXISTS `mydb`.`Professor` (
  `Id_Professor` INT NOT NULL AUTO_INCREMENT,
  `Departamento_Codigo_dep` INT NOT NULL,
  `Turma_Nome_Professor` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`Id_Professor`),
  INDEX `fk_Professor_Departamento1_idx` (`Departamento_Codigo_dep` ASC) VISIBLE,
  INDEX `fk_Professor_Turma1_idx` (`Turma_Nome_Professor` ASC) VISIBLE,
  CONSTRAINT `fk_Professor_Departamento1`
    FOREIGN KEY (`Departamento_Codigo_dep`)
    REFERENCES `mydb`.`Departamento` (`Codigo_dep`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Professor_Turma1`
    FOREIGN KEY (`Turma_Nome_Professor`)
    REFERENCES `mydb`.`Turma` (`Nome_Professor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Criação da tabela DenunciaAvTurma
CREATE TABLE IF NOT EXISTS `mydb`.`DenunciaAvTurma` (
  `idDenunciaAvTurma` INT NOT NULL AUTO_INCREMENT,
  `AvaliaTurma_Id_aval` INT NOT NULL,
  `Estudante_Matricula` INT(9) NOT NULL,
  PRIMARY KEY (`idDenunciaAvTurma`),
  INDEX `fk_DenunciaAvTurma_AvaliaTurma1_idx` (`AvaliaTurma_Id_aval` ASC) VISIBLE,
  INDEX `fk_DenunciaAvTurma_Estudante1_idx` (`Estudante_Matricula` ASC) VISIBLE,
  CONSTRAINT `fk_DenunciaAvTurma_AvaliaTurma1`
    FOREIGN KEY (`AvaliaTurma_Id_aval`)
    REFERENCES `mydb`.`AvaliaTurma` (`Id_aval`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DenunciaAvTurma_Estudante1`
    FOREIGN KEY (`Estudante_Matricula`)
    REFERENCES `mydb`.`Estudante` (`Matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Criação da tabela AvaliaProf
CREATE TABLE IF NOT EXISTS `mydb`.`AvaliaProf` (
  `idAvaliaProf` INT NOT NULL AUTO_INCREMENT,
  `Estudante_Matricula` INT(9) NOT NULL,
  `Professor_Id_Professor` INT NOT NULL,
  `Texto` VARCHAR(100) NOT NULL,
  `Score` INT NOT NULL,
  `DataHora` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idAvaliaProf`),
  INDEX `fk_AvaliaProf_Estudante1_idx` (`Estudante_Matricula` ASC) VISIBLE,
  INDEX `fk_AvaliaProf_Professor1_idx` (`Professor_Id_Professor` ASC) VISIBLE,
  CONSTRAINT `fk_AvaliaProf_Estudante1`
    FOREIGN KEY (`Estudante_Matricula`)
    REFERENCES `mydb`.`Estudante` (`Matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_AvaliaProf_Professor1`
    FOREIGN KEY (`Professor_Id_Professor`)
    REFERENCES `mydb`.`Professor` (`Id_Professor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Criação da tabela DenunciaAvProf
CREATE TABLE IF NOT EXISTS `mydb`.`DenunciaAvProf` (
  `idDenunciaAvProf` INT NOT NULL AUTO_INCREMENT,
  `AvaliaProf_idAvaliaProf` INT NOT NULL,
  `Estudante_Matricula` INT(9) NOT NULL,
  PRIMARY KEY (`idDenunciaAvProf`),
  INDEX `fk_DenunciaAvProf_AvaliaProf1_idx` (`AvaliaProf_idAvaliaProf` ASC) VISIBLE,
  INDEX `fk_DenunciaAvProf_Estudante1_idx` (`Estudante_Matricula` ASC) VISIBLE,
  CONSTRAINT `fk_DenunciaAvProf_AvaliaProf1`
    FOREIGN KEY (`AvaliaProf_idAvaliaProf`)
    REFERENCES `mydb`.`AvaliaProf` (`idAvaliaProf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DenunciaAvProf_Estudante1`
    FOREIGN KEY (`Estudante_Matricula`)
    REFERENCES `mydb`.`Estudante` (`Matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
