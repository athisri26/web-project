
create schema event
use event

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Insert your admin user
INSERT INTO admin (username, password) VALUES ('pjh', '123');

CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    image VARCHAR(255),
    description TEXT,
    chief_guest VARCHAR(255)
);