CREATE TABLE IF NOT EXISTS statusCodes(
   ID INT NOT NULL PRIMARY KEY,
   name VARCHAR(255) NOT NULL
);

REPLACE INTO statusCodes
  (ID, name) 
VALUES 
	(0, "success"),
	(1, "fail - generic"),
  (2, "fail - name resolution"),
  (3, "fail - timeout");

CREATE TABLE IF NOT EXISTS targets(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255),
	host VARCHAR(255) NOT NULL,
	port int NOT NULL,
	enabled BOOLEAN NOT NULL DEFAULT FALSE,
	inter int NOT NULL DEFAULT 5,
  retentionVal int NOT NULL DEFAULT 7,
  retentionUnit VARCHAR(255) NOT NULL DEFAULT 'DAY'
);

REPLACE INTO targets
  (ID, name, host, port, enabled, inter, retentionVal, retentionUnit) 
VALUES 
	(1, "target1", "192.168.1.1", 22, false, 5, 2, 'MINUTE'),
	(2, "target2", "google.com", 443, True, 2, 1, 'HOUR');


CREATE TABLE IF NOT EXISTS connResults(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	timestamp DATETIME NOT NULL,
	targetID INT NOT NULL,
	statusID INT NOT NULL,
	FOREIGN KEY (statusID)
    REFERENCES statusCodes (ID)
    ON DELETE CASCADE,
	FOREIGN KEY (targetID)
    REFERENCES targets (ID)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users(
   ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   username VARCHAR(255) UNIQUE NOT NULL,
   password VARCHAR(255),
   salt VARCHAR(255),
   enabled BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS userSessions(
   ID VARCHAR(255) UNIQUE,
   userID INT NOT NULL,
   started DATETIME NOT NULL,
   expires DATETIME NOT NULL,
   PRIMARY KEY (userID, ID),
   FOREIGN KEY (userID)
    REFERENCES users (ID)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sysConfig(
   ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(255) UNIQUE NOT NULL,
	 value VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS migrations(
   ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   migNo INT NOT NULL,
	 timestamp DATETIME NOT NULL
);

INSERT INTO migrations
  (migNo, timestamp) 
VALUES 
	(1, CURRENT_TIMESTAMP());