
DROP TABLE IF EXISTS `Artist_has_Song`;
DROP TABLE IF EXISTS `Album_has_Song`;
DROP TABLE IF EXISTS `Liked_has_Song`;
DROP TABLE IF EXISTS `History_of_played_has_Song`;
DROP TABLE IF EXISTS `Liked`;
DROP TABLE IF EXISTS `Currently_playing`;
DROP TABLE IF EXISTS `History_of_played`;
DROP TABLE IF EXISTS `Song_has_User_playlist`;
DROP TABLE IF EXISTS `User_playlist`;
DROP TABLE IF EXISTS `User`;
DROP TABLE IF EXISTS `Lyrics`;
DROP TABLE IF EXISTS `Song`;
DROP TABLE IF EXISTS `Album`;
DROP TABLE IF EXISTS `Artist`;
DROP TABLE IF EXISTS `Label`;

-- ========================================
-- CREATE TABLES
-- ========================================
CREATE TABLE `Label` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_label_name` (`name`),
  INDEX `idx_label_country` (`country`)
) ENGINE = InnoDB;

CREATE TABLE `Artist` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `in_playlist` TINYINT NOT NULL,
  `label_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_artist_name` (`name`),
  CONSTRAINT `fk_artist_label`
    FOREIGN KEY (`label_id`)
    REFERENCES `Label` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `Album` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `length` TIME NOT NULL,
  `year` DATE NOT NULL,
  `artist_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_album_name` (`name`),
  INDEX `idx_album_year` (`year`),
  CONSTRAINT `fk_album_artist`
    FOREIGN KEY (`artist_id`)
    REFERENCES `Artist` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `Song` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `length` TIME NOT NULL,
  `in_playlist` TINYINT NOT NULL,
  `year` DATE NOT NULL,
  `genre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_song_genre` (`genre`)
) ENGINE = InnoDB;

CREATE TABLE `Lyrics` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `lyric` TEXT NOT NULL,
  `songwriter` VARCHAR(45) NOT NULL,
  `song_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_lyrics_songwriter` (`songwriter`),
  CONSTRAINT `fk_lyrics_song`
    FOREIGN KEY (`song_id`)
    REFERENCES `Song` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `User` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `birthday` DATE NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_user_email` (`email`)
) ENGINE = InnoDB;

CREATE TABLE `User_playlist` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_user_playlist_user` (`user_id`),
  CONSTRAINT `fk_user_playlist_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `User` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `Song_has_User_playlist` (
  `song_id` INT NOT NULL,
  `user_playlist_id` INT NOT NULL,
  PRIMARY KEY (`song_id`, `user_playlist_id`),
  CONSTRAINT `fk_song_user_playlist_song`
    FOREIGN KEY (`song_id`)
    REFERENCES `Song` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_song_user_playlist_user_playlist`
    FOREIGN KEY (`user_playlist_id`)
    REFERENCES `User_playlist` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `History_of_played` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date_of_playing` DATE NOT NULL,
  `duration` TIME NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_history_of_played_user` (`user_id`),
  CONSTRAINT `fk_history_of_played_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `User` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `Currently_playing` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `is_played_now` VARCHAR(45) NOT NULL DEFAULT 'true',
  `timestamp` DATETIME NOT NULL,
  `device` VARCHAR(45) NOT NULL,
  `song_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_device` (`device`),
  INDEX `idx_currently_playing_timestamp` (`timestamp`),
  CONSTRAINT `fk_currently_playing_song`
    FOREIGN KEY (`song_id`)
    REFERENCES `Song` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `Liked` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `artist` VARCHAR(45) NOT NULL,
  `album` VARCHAR(45) NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_liked_artist` (`artist`),
  INDEX `idx_liked_album` (`album`),
  CONSTRAINT `fk_liked_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `User` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `Review` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `song_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `review_text` TEXT NOT NULL,
  `rating` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_review_song`
    FOREIGN KEY (`song_id`) REFERENCES `Song`(`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_review_user`
    FOREIGN KEY (`user_id`) REFERENCES `User`(`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE `History_of_played_has_Song` (
  `history_of_played_id` INT NOT NULL,
  `song_id` INT NOT NULL,
  PRIMARY KEY (`history_of_played_id`, `song_id`),
  CONSTRAINT `fk_history_of_played_song`
    FOREIGN KEY (`song_id`)
    REFERENCES `Song` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_history_of_played_has_song`
    FOREIGN KEY (`history_of_played_id`)
    REFERENCES `History_of_played`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `Liked_has_Song` (
  `liked_id` INT NOT NULL,
  `song_id` INT NOT NULL,
  PRIMARY KEY (`liked_id`, `song_id`),
  CONSTRAINT `fk_liked_song`
    FOREIGN KEY (`song_id`)
    REFERENCES `Song` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_liked_has_song_liked`
    FOREIGN KEY (`liked_id`)
    REFERENCES `Liked`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `Album_has_Song` (
  `album_id` INT NOT NULL,
  `song_id` INT NOT NULL,
  PRIMARY KEY (`album_id`, `song_id`),
  CONSTRAINT `fk_album_song`
    FOREIGN KEY (`song_id`)
    REFERENCES `Song` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_album_has_song_album`
    FOREIGN KEY (`album_id`)
    REFERENCES `Album`(`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE `Artist_has_Song` (
  `artist_id` INT NOT NULL,
  `song_id` INT NOT NULL,
  PRIMARY KEY (`artist_id`, `song_id`),
  CONSTRAINT `fk_artist_has_song_artist`
    FOREIGN KEY (`artist_id`)
    REFERENCES `Artist` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_artist_has_song_song`
    FOREIGN KEY (`song_id`)
    REFERENCES `Song` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;



-- ========================================
-- INSERT DATA
-- ========================================
INSERT INTO `Label` (`name`, `country`) VALUES
('Universal Music', 'USA'),
('Sony Music', 'Japan'),
('Warner Music', 'USA'),
('Atlantic Records', 'UK'),
('EMI', 'UK'),
('Columbia Records', 'USA'),
('Def Jam Recordings', 'USA'),
('Big Machine Records', 'USA'),
('Republic Records', 'USA'),
('Island Records', 'UK');

INSERT INTO `Artist` (`name`, `in_playlist`, `label_id`) VALUES
('Adele', 1, 1),
('Taylor Swift', 1, 8),
('Drake', 0, 7),
('BTS', 1, 2),
('The Beatles', 1, 5),
('Ed Sheeran', 1, 9),
('Kanye West', 0, 7),
('Coldplay', 1, 10),
('Billie Eilish', 1, 1),
('Imagine Dragons', 1, 4);

INSERT INTO `Album` (`name`, `length`, `year`, `artist_id`) VALUES
('25', '00:48:12', '2015-11-20', 1),
('1989', '00:48:41', '2014-10-27', 2),
('Scorpion', '01:21:13', '2018-06-29', 3),
('Map of the Soul: Persona', '00:42:12', '2019-04-12', 4),
('Abbey Road', '00:47:23', '1969-09-26', 5),
('Divide', '00:59:23', '2017-03-03', 6),
('Donda', '01:08:52', '2021-08-29', 7),
('Parachutes', '00:41:45', '2000-07-10', 8),
('Happier Than Ever', '00:43:22', '2021-07-30', 9),
('Evolve', '00:42:12', '2017-06-23', 10);

INSERT INTO `Song` (`name`, `length`, `in_playlist`, `year`, `genre`) VALUES
('Hello', '00:04:55', 1, '2015-10-23', 'Pop'),
('Rolling in the Deep', '00:03:48', 1, '2010-11-29', 'Pop'),
('Shake It Off', '00:03:39', 1, '2014-08-18', 'Pop'),
('Blank Space', '00:03:51', 1, '2014-11-10', 'Pop'),
('God\'s Plan', '00:03:19', 0, '2018-02-06', 'Hip-Hop'),
('Life Goes On', '00:03:27', 1, '2020-11-20', 'K-Pop'),
('Here Comes the Sun', '00:03:06', 1, '1969-09-26', 'Rock'),
('Perfect', '00:04:23', 1, '2017-09-26', 'Pop'),
('Happier Than Ever', '00:04:58', 1, '2021-07-30', 'Pop'),
('Believer', '00:03:37', 1, '2017-02-01', 'Rock');

INSERT INTO `Lyrics` (`lyric`, `songwriter`, `song_id`) VALUES
('Hello, it\'s me...', 'Adele Adkins', 1),
('We could have had it all...', 'Paul Epworth, Adele Adkins', 2),
('Cause the players gonna play...', 'Taylor Swift, Max Martin', 3),
('Wait, the worst is yet to come...', 'Taylor Swift, Shellback', 4),
('She said, "Do you love me?" I tell her...', 'Drake, 40', 5),
('Like an echo in the forest...', 'BTS', 6),
('Little darling, it\'s been a long cold...', 'George Harrison', 7),
('You look perfect tonight...', 'Ed Sheeran', 8),
('When I\'m away from you...', 'Billie Eilish, Finneas', 9),
('You made me a believer...', 'Imagine Dragons', 10);

INSERT INTO `User` (`name`, `surname`, `email`, `password`, `birthday`) VALUES
('John', 'Doe', 'john.doe@example.com', 'password123', '1990-01-15'),
('Jane', 'Smith', 'jane.smith@example.com', '123password', '1985-05-23'),
('Alice', 'Johnson', 'alice.j@example.com', 'alicePass', '1995-03-10'),
('Bob', 'Brown', 'bob.brown@example.com', 'bobbyB', '1982-07-18'),
('Charlie', 'Davis', 'charlie.d@example.com', 'charlieD', '1998-11-09'),
('Eve', 'Miller', 'eve.m@example.com', 'evePass', '1993-08-22'),
('Mike', 'Taylor', 'mike.t@example.com', 'password404', '1987-02-04'),
('Nancy', 'Wilson', 'nancy.w@example.com', 'nancyT', '2000-06-30'),
('Oscar', 'Moore', 'oscar.m@example.com', 'password606', '1989-04-18'),
('Patricia', 'Thomas', 'patricia.t@example.com', 'password707', '1997-06-06');

INSERT INTO `User_playlist` (`id`, `user_id`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO `Song_has_User_playlist` (`song_id`, `user_playlist_id`) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 2),
(5, 4),
(6, 3),
(7, 10),
(8, 5),
(9, 6),
(10, 10);

INSERT INTO `History_of_played` (`id`, `date_of_playing`, `duration`, `user_id`) VALUES
(1, '2024-11-18', '00:03:45', 1),
(2, '2024-11-18', '00:04:20', 2),
(3, '2024-11-18', '00:05:10', 3),
(4, '2024-11-18', '00:04:50', 4),
(5, '2024-11-18', '00:03:30', 5),
(6, '2024-11-18', '00:03:55', 6),
(7, '2024-11-18', '00:04:05', 7),
(8, '2024-11-18', '00:03:25', 8),
(9, '2024-11-18', '00:04:15', 9),
(10, '2024-11-18', '00:05:00', 10);

INSERT INTO `Currently_playing` (`id`, `is_played_now`, `timestamp`, `device`, `song_id`) VALUES
(1, 'true', '2024-11-20 10:00:00', 'iPhone 13', 1),
(2, 'true', '2024-11-20 10:05:00', 'Samsung Galaxy S21', 2),
(3, 'false', '2024-11-20 10:10:00', 'MacBook Pro', 3),
(4, 'true', '2024-11-20 10:15:00', 'Google Pixel 6', 4),
(5, 'false', '2024-11-20 10:20:00', 'Sony Xperia 1', 5),
(6, 'true', '2024-11-20 10:25:00', 'Dell XPS 13', 6),
(7, 'false', '2024-11-20 10:30:00', 'iPad Pro', 7),
(8, 'true', '2024-11-20 10:35:00', 'Huawei P40', 8),
(9, 'true', '2024-11-20 10:40:00', 'OnePlus 9', 9),
(10, 'false', '2024-11-20 10:45:00', 'Microsoft Surface', 10);

INSERT INTO `Liked` (`id`, `artist`, `album`, `user_id`) VALUES
(1, 'Adele', '25', 1),
(2, 'Taylor Swift', '1989', 2),
(3, 'Drake', 'Scorpion', 3),
(4, 'BTS', 'Map of the Soul: Persona', 4),
(5, 'The Beatles', 'Abbey Road', 5),
(6, 'Ed Sheeran', 'Divide', 6),
(7, 'Kanye West', 'Donda', 7),
(8, 'Coldplay', 'Parachutes', 8),
(9, 'Billie Eilish', 'Happier Than Ever', 9),
(10, 'Imagine Dragons', 'Evolve', 10);

INSERT INTO `History_of_played_has_Song` (`history_of_played_id`, `song_id`) VALUES
(1, 1),
(2, 3),
(3, 5),
(4, 7),
(5, 9),
(6, 2),
(7, 4),
(8, 6),
(9, 8),
(10, 10);

INSERT INTO `Liked_has_Song` (`liked_id`, `song_id`) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(3, 6),
(4, 7),
(4, 8),
(5, 9),
(5, 10);

INSERT INTO `Album_has_Song` (`album_id`, `song_id`) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(4, 6),
(5, 7),
(6, 8),
(7, 9),
(8, 10);

INSERT INTO `Artist_has_Song` (`artist_id`, `song_id`) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(4, 6),
(5, 7),
(6, 8),
(7, 9),
(8, 10);

ALTER TABLE `Song` ADD INDEX `idx_name` (`name`);
ALTER TABLE `Currently_playing` ADD INDEX `idx_song_device` (`song_id`, `device`);

