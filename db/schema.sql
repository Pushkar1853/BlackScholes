CREATE TABLE BlackScholesInputs (
    CalculationId INT NOT NULL AUTO_INCREMENT,
    StockPrice DECIMAL(18,9) NOT NULL,
    StrikePrice DECIMAL(18,9) NOT NULL,
    InterestRate DECIMAL(18,9) NOT NULL,
    Volatility DECIMAL(18,9) NOT NULL,
    TimeToExpiry DECIMAL(18,9) NOT NULL,
    CallPurchasePrice DECIMAL(18,9),
    PutPurchasePrice DECIMAL(18,9),
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (CalculationId)
);

CREATE TABLE BlackScholesInputs(
    CalculationOutputId INT NOT NULL AUTO_INCREMENT,
    VolatilityIndex DECIMAL(18,9) NOT NULL,
    StockPriceShock DECIMAL(18,9) NOT NULL,
    OptionPrice DECIMAL(18,9) NOT NULL,
    IsCall TINYINT(1) NOT NULL,
    CalculationId INT NOT NULL,
    PRIMARY KEY (CalculationOutputId),
    INDEX idx_CalculationId (CalculationId),
    CONSTRAINT FK_CalculationId FOREIGN KEY (CalculationId) REFERENCES BlackScholesInputs(CalculationId) ON DELETE CASCADE ON UPDATE CASCADE
);