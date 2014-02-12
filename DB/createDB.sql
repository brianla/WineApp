SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`UserInfo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`UserInfo` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`UserInfo` (
  `userID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `emailAddress` VARCHAR(255) NOT NULL ,
  `password` VARCHAR(255) NOT NULL ,
  `name` VARCHAR(255) NULL ,
  `location` VARCHAR(255) NULL ,
  `dateOfBirth` DATE NULL ,
  `imagePath` VARCHAR(255) NULL ,
  PRIMARY KEY (`userID`) ,
  UNIQUE INDEX `useID_UNIQUE` (`userID` ASC) ,
  UNIQUE INDEX `emailAddress_UNIQUE` (`emailAddress` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`LocationMap`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`LocationMap` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`LocationMap` (
  `locationID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `lm_userID` INT UNSIGNED NOT NULL ,
  `locationName` VARCHAR(255) NOT NULL ,
  `timeCreated` TIMESTAMP NOT NULL ,
  `imagePath` VARCHAR(255) NULL ,
  PRIMARY KEY (`locationID`) ,
  UNIQUE INDEX `locationID_UNIQUE` (`locationID` ASC) ,
  INDEX `userID_idx` (`lm_userID` ASC) ,
  CONSTRAINT `lm_userID`
    FOREIGN KEY (`lm_userID` )
    REFERENCES `mydb`.`UserInfo` (`userID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Wines`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Wines` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`Wines` (
  `wineID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `wineName` VARCHAR(255) NOT NULL ,
  `varietal` VARCHAR(255) NOT NULL ,
  `winery` VARCHAR(255) NULL ,
  `wineType` VARCHAR(255) NULL ,
  `vintage` YEAR NULL ,
  `region` VARCHAR(255) NULL ,
  `clusterID` INT NULL ,
  `CSO` TINYINT(1) NULL ,
  `tags` VARCHAR(1024) NULL ,
  `description` VARCHAR(4096) NULL ,
  `averageStarRating` FLOAT NULL ,
  `imagePath` VARCHAR(255) NULL ,
  `barcode` VARCHAR(255) NULL ,
  `bitter` FLOAT NULL ,
  `sweet` FLOAT NULL ,
  `sour` FLOAT NULL ,
  `salty` FLOAT NULL ,
  `chemical` FLOAT NULL ,
  `pungent` FLOAT NULL ,
  `oxidized` FLOAT NULL ,
  `microbiological` FLOAT NULL ,
  `floral` FLOAT NULL ,
  `spicy` FLOAT NULL ,
  `fruity` FLOAT NULL ,
  `vegetative` FLOAT NULL ,
  `nutty` FLOAT NULL ,
  `caramelized` FLOAT NULL ,
  `woody` FLOAT NULL ,
  `earthy` FLOAT NULL ,
  PRIMARY KEY (`wineID`) ,
  UNIQUE INDEX `wineID_UNIQUE` (`wineID` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`LocationInventory`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`LocationInventory` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`LocationInventory` (
  `li_index` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `li_locationID` INT UNSIGNED NOT NULL ,
  `li_wineID` INT UNSIGNED NOT NULL ,
  `quantity` INT UNSIGNED NOT NULL ,
  `tags` VARCHAR(1024) NULL ,
  `description` VARCHAR(4096) NULL ,
  `imagePath` VARCHAR(255) NULL ,
  `personalStarRating` INT NULL ,
  `isWishlist` TINYINT(1) NOT NULL ,
  `bitter` FLOAT NULL ,
  `sweet` FLOAT NULL ,
  `sour` FLOAT NULL ,
  `salty` FLOAT NULL ,
  `chemical` FLOAT NULL ,
  `pungent` FLOAT NULL ,
  `oxidized` FLOAT NULL ,
  `microbiological` FLOAT NULL ,
  `floral` FLOAT NULL ,
  `spicy` FLOAT NULL ,
  `fruity` FLOAT NULL ,
  `vegetative` FLOAT NULL ,
  `nutty` FLOAT NULL ,
  `caramelized` FLOAT NULL ,
  `woody` FLOAT NULL ,
  `earthy` FLOAT NULL ,
  INDEX `locationID_idx` (`li_locationID` ASC) ,
  INDEX `wineID_idx` (`li_wineID` ASC) ,
  UNIQUE INDEX `li_index_UNIQUE` (`li_index` ASC) ,
  CONSTRAINT `li_locationID`
    FOREIGN KEY (`li_locationID` )
    REFERENCES `mydb`.`LocationMap` (`locationID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `li_wineID`
    FOREIGN KEY (`li_wineID` )
    REFERENCES `mydb`.`Wines` (`wineID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`LocationHistory`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`LocationHistory` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`LocationHistory` (
  `lh_index` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `lh_locationID` INT UNSIGNED NOT NULL ,
  `lh_wineID` INT UNSIGNED NOT NULL ,
  `timestamp` TIMESTAMP NOT NULL ,
  `eventTag` VARCHAR(255) NOT NULL ,
  INDEX `locationID_idx` (`lh_locationID` ASC) ,
  INDEX `wineID_idx` (`lh_wineID` ASC) ,
  UNIQUE INDEX `lh_index_UNIQUE` (`lh_index` ASC) ,
  CONSTRAINT `lh_locationID`
    FOREIGN KEY (`lh_locationID` )
    REFERENCES `mydb`.`LocationMap` (`locationID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `lh_wineID`
    FOREIGN KEY (`lh_wineID` )
    REFERENCES `mydb`.`Wines` (`wineID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Recommenders`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Recommenders` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`Recommenders` (
  `recommenderID` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `r_userID` INT UNSIGNED NOT NULL ,
  `channelName` VARCHAR(255) NOT NULL ,
  `timeCreated` TIMESTAMP NOT NULL ,
  PRIMARY KEY (`recommenderID`) ,
  UNIQUE INDEX `channelID_UNIQUE` (`recommenderID` ASC) ,
  INDEX `userID_idx` (`r_userID` ASC) ,
  CONSTRAINT `r_userID`
    FOREIGN KEY (`r_userID` )
    REFERENCES `mydb`.`UserInfo` (`userID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`RecommenderHistory`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`RecommenderHistory` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`RecommenderHistory` (
  `rh_index` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `rh_recommenderID` INT UNSIGNED NOT NULL ,
  `rh_wineID` INT UNSIGNED NOT NULL ,
  `timestamp` TIMESTAMP NOT NULL ,
  `isSeedBottle` TINYINT(1) NOT NULL ,
  INDEX `channelID_idx` (`rh_recommenderID` ASC) ,
  INDEX `wineID_idx` (`rh_wineID` ASC) ,
  UNIQUE INDEX `rh_index_UNIQUE` (`rh_index` ASC) ,
  CONSTRAINT `rh_channelID`
    FOREIGN KEY (`rh_recommenderID` )
    REFERENCES `mydb`.`Recommenders` (`recommenderID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `rh_wineID`
    FOREIGN KEY (`rh_wineID` )
    REFERENCES `mydb`.`Wines` (`wineID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `mydb` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
