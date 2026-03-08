IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
BEGIN
    CREATE TABLE users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100),
        email NVARCHAR(100),
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO
