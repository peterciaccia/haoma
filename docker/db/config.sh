#echo "Hello world"
#mysql --user="root" --password="${MYSQL_ROOT_PASSWORD}" --execute="CREATE DATABASE IF NOT EXISTS '${DATABASE}';"
#mysql --user="root" --password="${MYSQL_ROOT_PASSWORD}" --execute="CREATE USER IF NOT EXISTS '${MYSQL_NAME}'@'%' IDENTIFIED BY '${MYSQL_PASS}';"
#mysql --user="root" --password="${MYSQL_ROOT_PASSWORD}" --execute="GRANT ALL PRIVILEGES ON * . * TO '${MYSQL_NAME}'@'%';"

# OR

echo "** Creating default DB and users" >> config.log

MYSQL_EXEC_STR="${MYSQL_ROOT_PASSWORD} --execute \"CREATE DATABASE IF NOT EXISTS ${DATABASE}; \
GRANT ALL PRIVILEGES ON ${DATABASE} . * TO '${MYSQL_USER}'@'%';\""

MYSQL_EXEC_STR_DEFAULTS="--execute \"CREATE DATABASE IF NOT EXISTS ${DATABASE}; \
GRANT ALL PRIVILEGES ON ${DATABASE} . * TO '${MYSQL_USER}'@'%';\""

BASH_EXEC_STR_DEBUG="mysql -u root -p ${MYSQL_EXEC_STR}"

echo -e "** MYSQL_EXEC_STR:\n${MYSQL_EXEC_STR}" >> config.log
echo -e "** MYSQL_EXEC_STR_DEFAULTS:\n${MYSQL_EXEC_STR_DEFAULTS}" >> config.log
echo -e "** BASH_EXEC_STR_DEBUG:\n${BASH_EXEC_STR_DEBUG}" >> config.log
#mysql -u root -p "${MYSQL_EXEC_STR}"
#mysql --defaults-file="/root/.my.cnf" "${MYSQL_EXEC_STR_DEFAULTS}"
echo -e "** Finished creating default DB and users\n" >> config.log