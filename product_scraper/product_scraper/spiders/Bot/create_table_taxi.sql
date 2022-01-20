
CREATE TABLE `clients` (
    `id_telegram` INT NOT NULL,
    `phone` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`id_telegram`),
    UNIQUE KEY (`phone`)
    );


CREATE TABLE `addresses` (
    `id_address` INT NOT NULL AUTO_INCREMENT,
    `city` VARCHAR(64) NOT NULL,
    `street` VARCHAR(64) NOT NULL DEFAULT '',
    `house` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id_address`),
    UNIQUE KEY (`city`, `street`, `house`)
    );


CREATE TABLE `venues` (
    `id_venue` INT NOT NULL AUTO_INCREMENT,
    `id_telegram` INT NOT NULL,
    `id_address` INT NOT NULL,
    `title` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id_venue`),
    FOREIGN KEY (`id_telegram`)
        REFERENCES `clients`(`id_telegram`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (`id_address`)
        REFERENCES `addresses`(`id_address`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );


CREATE TABLE `orders`(
    `id_order` INT NOT NULL AUTO_INCREMENT,
    `id_telegram` INT NOT NULL,
    `adr_from` INT NOT NULL,
    `adr_where` INT NOT NULL,
    `ya_num` INT NOT NULL,
    `ya_id` CHAR(32) NOT NULL,
    `datetime` TIMESTAMP NOT NULL,
    `amount` INT NULL,
    UNIQUE KEY (`ya_id`),
    PRIMARY KEY (`id_order`),
    FOREIGN KEY (`id_telegram`)
        REFERENCES `clients` (`id_telegram`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (`adr_from`)
        REFERENCES `addresses` (`id_address`)
        ON UPDATE CASCADE,
    FOREIGN KEY (`adr_where`)
        REFERENCES `addresses` (`id_address`)
        ON UPDATE CASCADE
    );


CREATE TABLE `currents`(
    `id_telegram` INT NOT NULL,
    `ya_id` CHAR(32) NOT NULL,
    `status` INT NOT NULL,
    `id_gps` INT NULL,
    PRIMARY KEY (`id_telegram`),
    FOREIGN KEY (`id_telegram`)
        REFERENCES `clients` (`id_telegram`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (`ya_id`)
        REFERENCES `orders` (`ya_id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );
