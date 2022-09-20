DROP TABLE IF EXISTS Stations;
CREATE TABLE Stations
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    VARCHAR(80),
    password    VARCHAR(80),
    ip          VARCHAR(255),
    uuid        VARCHAR(255),
    mac         VARCHAR(255),
    description TEXT,
    created     TIMESTAMP DEFAULT (datetime('now', 'localtime')),
    status      INTEGER   DEFAULT 0,
    src         VARCHAR(255),
    des         VARCHAR(255)
)