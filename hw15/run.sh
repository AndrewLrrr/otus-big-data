#!/usr/bin/env bash

ROOT_DIR=$(pwd)
HADOOP_ROOT_DIR=/tmp/hive
HIVE_SCRIPTS_DIR=$(pwd)/scripts
RED="\033[0;31m"
GREEN="\033[0;32m"
NC="\033[0m"

hadoop fs -test -d ${HADOOP_ROOT_DIR}

echo -e "${RED}Preparing hdfs...${NC}"
if [[ $? -eq 0 ]]; then
    hadoop fs -rm -r ${HADOOP_ROOT_DIR}
fi 

echo "${RED}Checking source file...${NC}"
if [[ ! -f ${ROOT_DIR}/Video_Games_Sales_as_at_22_Dec_2016.csv.zip ]]; then
    echo -e "${RED}Source file not found. Please download it by link https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings/downloads/Video_Games_Sales_as_at_22_Dec_2016.csv${NC}"
else
    echo -e "${GREEN}Task 1. Unpack and copy source file to hdfs.${NC}"
    unzip ${ROOT_DIR}/Video_Games_Sales_as_at_22_Dec_2016.csv.zip -d ${ROOT_DIR}
    hadoop fs -mkdir -p ${HADOOP_ROOT_DIR}/data
    hadoop fs -put ${ROOT_DIR}/Video_Games_Sales_as_at_22_Dec_2016.csv ${HADOOP_ROOT_DIR}/data
    hadoop fs -chmod 777 ${HADOOP_ROOT_DIR}
    rm ${ROOT_DIR}/Video_Games_Sales_as_at_22_Dec_2016.csv
fi

echo -e "${GREEN}Task 2. Create an external table in to the database `raw`.${NC}"

echo -e "${RED}Creating the database...${NC}"

hive -f ${HIVE_SCRIPTS_DIR}/create-db.sql

echo -e "${RED}Creating the table...${NC}"

hive -f ${HIVE_SCRIPTS_DIR}/create-external-table.sql

echo -e "${RED}Display first 10 entries from the table...${NC}"

hive -e 'SELECT * FROM raw.game_sales LIMIT 10'
