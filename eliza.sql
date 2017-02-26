CREATE TABLE eUser(
username VARCHAR(14),
password VARCHAR(256)
email VARCHAR(50),
validated BOOLEAN,
key VARCHAR(256),
PRIMARY KEY(username)
);

CREATE TABLE uSession(
cookieID TEXT,
username VARCHAR(14),
PRIMARY KEY(cookieID),
FOREIGN KEY(username) REFERENCES eUser(username)
);

CREATE TABLE conversation(
convID SERIAL,
PRIMARY KEY (convID)
);

CREATE TABLE message(
messageID SERIAL,
content TEXT,
mDate TIMESTAMP,
convID INT,
PRIMARY KEY(messageID),
FOREIGN KEY(convID) REFERENCES conversation(convID)
);


