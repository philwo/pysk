#!/usr/bin/php
<?php
$mysqlpw = trim(file_get_contents("/opt/pysk/secret/mysqlpw"));
$link = new mysqli("localhost", "root", $mysqlpw);

if ($link->connect_error) {
    die("Unable to connect to the database: " . $link->connect_error);
}

$databases = $link->query("SHOW DATABASES") or die("Error on SHOW DATABASES");

while ($databases_rs = $databases->fetch_array())
{
    $dbname = $databases_rs["Database"];

    if ($dbname == "information_schema")
        continue;

    $link->select_db($dbname) or die("Unable to select database: " . $dbname);
    $tables = $link->query("SHOW TABLES") or die("Error on SHOW TABLES");

    while ($tables_rs = $tables->fetch_array())
    {
        $key = "Tables_in_" . $dbname;

        # REPAIR
        $sql = "REPAIR TABLE `" . $tables_rs[$key] . "`";
        $op = $link->query($sql) or die("Error on REPAIR TABLE ($sql)");
        $op_rs = $op->fetch_array();
        if (!(
            ($op_rs["Msg_type"] == "status" && $op_rs["Msg_text"] == "OK") ||
            ($op_rs["Msg_type"] == "note" && $op_rs["Msg_text"] == "The storage engine for the table doesn't support repair")
        )) {
            echo $op_rs["Table"] . " | " . $op_rs["Op"] . " | " . $op_rs["Msg_type"] . " | " . $op_rs["Msg_text"] . "\n";
        }
        $op->close();

        # OPTIMIZE
        $sql = "OPTIMIZE TABLE `" . $tables_rs[$key] . "`";
        $op = $link->query($sql) or die("Error on OPTIMIZE TABLE ($sql)");
        $op_rs = $op->fetch_array();
        if (!(
            ($op_rs["Msg_type"] == "status" && $op_rs["Msg_text"] == "OK") ||
            ($op_rs["Msg_type"] == "note" && $op_rs["Msg_text"] == "The storage engine for the table doesn't support optimize") ||
            ($op_rs["Msg_type"] == "note" && $op_rs["Msg_text"] == "Table does not support optimize, doing recreate + analyze instead")
        )) {
            echo $op_rs["Table"] . " | " . $op_rs["Op"] . " | " . $op_rs["Msg_type"] . " | " . $op_rs["Msg_text"] . "\n";
        }
        $op->close();

        # Skip analyze, if optimize already did it
        if ($op_rs["Msg_type"] == "note" && $op_rs["Msg_text"] == "Table does not support optimize, doing recreate + analyze instead") {
            continue;
        }

        # ANALYZE
        $sql = "ANALYZE TABLE `" . $tables_rs[$key] . "`";
        $op = $link->query($sql) or die("Error on ANALYZE TABLE ($sql)");
        $op_rs = $op->fetch_array();
        if (!(
            ($op_rs["Msg_type"] == "status" && $op_rs["Msg_text"] == "OK") ||
            ($op_rs["Msg_type"] == "status" && $op_rs["Msg_text"] == "Table is already up to date") ||
            ($op_rs["Msg_type"] == "note" && $op_rs["Msg_text"] == "The storage engine for the table doesn't support analyze")
        )) {
            echo $op_rs["Table"] . " | " . $op_rs["Op"] . " | " . $op_rs["Msg_type"] . " | " . $op_rs["Msg_text"] . "\n";
        }
        $op->close();
    }

    $tables->close();
}

$databases->close();
$link->close();

?>
