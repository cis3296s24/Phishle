-- Table for User Logins
CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(100) NOT NULL,
    PlayStreak INT DEFAULT 0,
    WinStreak INT DEFAULT 0,
    TotalWins INT DEFAULT 0,
    TotalLosses INT DEFAULT 0
);

-- Table for Groups
CREATE TABLE Groups (
    GroupID INT PRIMARY KEY AUTO_INCREMENT,
    GroupName VARCHAR(100) NOT NULL,
    AdminUserID INT NOT NULL,
    FOREIGN KEY (AdminUserID) REFERENCES Users(UserID)
);

-- Table for Group Memberships
CREATE TABLE GroupMembers (
    GroupID INT,
    UserID INT,
    PRIMARY KEY (GroupID, UserID),
    FOREIGN KEY (GroupID) REFERENCES Groups(GroupID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Table for Leaderboard Data
CREATE TABLE Leaderboard (
    GroupID INT,
    UserID INT,
    Wins INT DEFAULT 0,
    Losses INT DEFAULT 0,
    PRIMARY KEY (GroupID, UserID),
    FOREIGN KEY (GroupID) REFERENCES Groups(GroupID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
