CREATE or REPLACE DATABASE SAMPLE_DB;

USE DATABASE SAMPLE_DB;

CREATE OR REPLACE SCHEMA RAW_DATA;

CREATE OR REPLACE TABLE CurrencyExchange (
    Date STRING,
    FromCurrency STRING,
    ToCurrency STRING,
    Exchange STRING
);

CREATE OR REPLACE TABLE Customer (
    CustomerKey      INT,
    GeoAreaKey       INT,
    StartDT          STRING,       -- Will convert to DATE in Power BI
    EndDT            STRING,       -- Will convert to DATE in Power BI
    Continent        STRING,
    Gender           STRING,
    Title            STRING,
    GivenName        STRING,
    MiddleInitial    STRING,
    Surname          STRING,
    StreetAddress    STRING,
    City             STRING,
    State            STRING,
    StateFull        STRING,
    ZipCode          STRING,       -- Keep as string to preserve leading 0s
    Country          STRING,
    CountryFull      STRING,
    Birthday         STRING,       -- Convert to DATE in Power BI
    Age              INT,
    Occupation       STRING,
    Company          STRING,
    Vehicle          STRING,
    Latitude         FLOAT,
    Longitude        FLOAT
);


CREATE OR REPLACE TABLE Date (
    Date               STRING,     -- Can be converted to DATE in Power BI
    DateKey            INT,
    Year               INT,
    YearQuarter        STRING,
    YearQuarterNumber  INT,
    Quarter            STRING,
    YearMonth          STRING,
    YearMonthShort     STRING,
    YearMonthNumber    INT,
    Month              STRING,
    MonthShort         STRING,
    MonthNumber        INT,
    DayofWeek          STRING,
    DayofWeekShort     STRING,
    DayofWeekNumber    INT,
    WorkingDay         INT,
    WorkingDayNumber   INT
);


CREATE OR REPLACE TABLE OrderRows (
    OrderKey     INT,
    LineNumber   INT,
    ProductKey   INT,
    Quantity     INT,
    UnitPrice    FLOAT,
    NetPrice     FLOAT,
    UnitCost     FLOAT
);


CREATE OR REPLACE TABLE Orders (
    OrderKey       INT,
    CustomerKey    INT,
    StoreKey       INT,
    OrderDate      STRING,   -- Convert to DATE in Power BI
    DeliveryDate   STRING,   -- Convert to DATE in Power BI
    CurrencyCode   STRING
);


CREATE OR REPLACE TABLE Product (
    ProductKey        INT,
    ProductCode       INT,
    ProductName       STRING,
    Manufacturer      STRING,
    Brand             STRING,
    Color             STRING,
    WeightUnit        STRING,
    Weight            FLOAT,
    Cost              FLOAT,
    Price             FLOAT,
    CategoryKey       INT,
    CategoryName      STRING,
    SubCategoryKey    INT,
    SubCategoryName   STRING
);


CREATE OR REPLACE TABLE Sales (
    OrderKey       INT,
    LineNumber     INT,
    OrderDate      STRING,   -- Will convert to DATE in Power BI
    DeliveryDate   STRING,   -- Will convert to DATE in Power BI
    CustomerKey    INT,
    StoreKey       INT,
    ProductKey     INT,
    Quantity       INT,
    UnitPrice      FLOAT,
    NetPrice       FLOAT,
    UnitCost       FLOAT,
    CurrencyCode   STRING,
    ExchangeRate   FLOAT
);

CREATE OR REPLACE TABLE Store (
    StoreKey       INT,
    StoreCode      INT,
    GeoAreaKey     INT,
    CountryCode    STRING,
    CountryName    STRING,
    State          STRING,
    OpenDate       STRING,   -- Convert to DATE in Power BI
    CloseDate      STRING,   -- Convert to DATE in Power BI
    Description    STRING,
    SquareMeters   FLOAT,
    Status         STRING
);

