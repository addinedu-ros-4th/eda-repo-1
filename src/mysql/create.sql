CREATE TABLE flights(  
    항공사 VARCHAR(30) not null,
    출발시간 VARCHAR(20) not null,
    출발공항 VARCHAR(20) not null,
    도착시간 VARCHAR(20) not null,
    도착공항 VARCHAR(20) not null,
    비행방식 VARCHAR(10) not null,
    비행일자 VARCHAR(10) not null,
    소요시간 VARCHAR(20) not null,
    `편도/왕복` VARCHAR(10) not null,
    가격 INT not null,
    추출시간 DATE not null,
    편명 VARCHAR(30) not null,
    PRIMARY KEY (편명, 출발시간, 도착공항, 비행일자, 추출시간)
);