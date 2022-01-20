CREATE TABLE `publics` (
    `owner_id` INT NOT NULL,
    `domain` VARCHAR(32)  NOT NULL,
    PRIMARY KEY (`owner_id`)
    );
    
CREATE TABLE `posts` (
    `post_id` INT NOT NULL,
    `owner_id` INT NOT NULL,
    `type` ENUM ('text', 'photo', 'video', 'audio', 'doc', 'graffiti', 'link', 'note', 'app', 'poll',
        'page', 'album', 'photos_list', 'market', 'market_album', 'sticker') NOT NULL,
    `unixtime_create` INT NOT NULL,
    FOREIGN KEY (`owner_id`)
        REFERENCES `publics`(`owner_id`),
    PRIMARY KEY (`post_id`, `owner_id`)
    );

CREATE TABLE `statist` (
    `post_id` INT NOT NULL,
    `likes` INT NOT NULL,
    `reposts` INT NOT NULL,
    `views` INT NOT NULL,
    `unixtime` INT NOT NULL,
    FOREIGN KEY (`post_id`)
        REFERENCES `posts`(`post_id`)
    );


CREATE TABLE `statist2` (
    `owner_id` INT NOT NULL,
    `members` INT NOT NULL,
    `unixtime` INT NOT NULL,
    FOREIGN KEY (`owner_id`)
        REFERENCES `publics`(`owner_id`)
    );


     INSERT INTO `statist` (`owner_id`, `post_id`, `likes`, `reposts`, `views`, `unixtime`)
        VALUES (2, 2, 1, 1, 1, 123);
    
CREATE TABLE `drivers` (
    `id_driver` INT NOT NULL AUTO_INCREMENT,
    `id_yataxi` CHAR(32) NOT NULL,
    `first_name` VARCHAR(64) NOT NULL,
    `last_name` VARCHAR(64) NOT NULL,
    `surname` VARCHAR(64) NOT NULL DEFAULT '',
    `passport` VARCHAR(16) NULL,
    `issued_by` VARCHAR(64) NULL,
    `when_issued` DATE NULL,
    `depart_code` VARCHAR(16) NULL,
    `birth_date` DATE NULL,
    `birth_place` VARCHAR(16) NULL,
    `address_reg` VARCHAR(128) NULL,
    `address_fact` VARCHAR(128) NULL,
    `tin` VARCHAR(16) NULL,
    `driver_license` VARCHAR(32) NULL,
    `license_date_of` DATE NULL,
    `license_date_end` DATE NULL,
    `status` ENUM ('уволен', 'работает', 'оформлен') DEFAULT 'уволен',
    PRIMARY KEY (`id_driver`),
    UNIQUE KEY (`id_yataxi`)
    ) ENGINE = InnoDB;

CREATE TABLE `phones`(
    `id_phone` INT NOT NULL AUTO_INCREMENT,
    `id_driver` INT NOT NULL,
    `phone` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`id_phone`),
    FOREIGN KEY (`id_driver`)
        REFERENCES `drivers`(`id_driver`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    UNIQUE KEY (`phone`)
    ) ENGINE = InnoDB;


CREATE TABLE telegrams (
    id_driver INT NULL,
    id_telegram INT NOT NULL,
    PRIMARY KEY (id_telegram),
    FOREIGN KEY (id_driver)
        REFERENCES drivers(id_driver)
        ON UPDATE CASCADE
        ON DELETE SET NULL
    ) ENGINE = InnoDB;


CREATE TABLE zp_alfa (
    id_driver INT NOT NULL,
    id_alfa VARCHAR(10) NOT NULL,
    account_number VARCHAR(20) NOT NULL,
    status_card VARCHAR(32) NOT NULL,
    active_to VARCHAR(5) NOT NULL,
    PRIMARY KEY (id_driver),
    FOREIGN KEY (id_driver)
        REFERENCES drivers(id_driver)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    UNIQUE KEY (id_alfa),
    UNIQUE KEY (account_number)
    ) ENGINE = InnoDB;

CREATE TABLE `payments`(
    `id_payment` INT NOT NULL AUTO_INCREMENT,
    `id_driver` INT NOT NULL,
    `amount` INT NOT NULL,
    `date_payment` DATE NOT NULL,
    PRIMARY KEY (`id_payment`),
    FOREIGN KEY (`id_driver`)
        REFERENCES `drivers`(`id_driver`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    ) ENGINE = InnoDB;


SELECT drivers.last_name, drivers.first_name, drivers.surname,
    zp_alfa.account_number, payments.amount, payments.id_payment, drivers.id_yataxi
FROM drivers, payments, zp_alfa
WHERE payments.date_payment = '2017-12-22'
    AND payments.id_driver = zp_alfa.id_driver
    AND payments.id_driver = drivers.id_driver
ORDER by payments.id_payment;

