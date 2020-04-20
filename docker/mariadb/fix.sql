-- This sqls fix error on cyrillic string in database.

ALTER TABLE `wrp_server_db`.`django_admin_log`
	CHANGE `object_repr` `object_repr` VARCHAR(255) CHARSET utf8 NOT NULL;

ALTER TABLE `wrp_server_db`.`django_admin_log`
	CHANGE `object_id` `object_id` longtext CHARSET utf8 NOT NULL;

ALTER TABLE `wrp_server_db`.`django_admin_log`
	CHANGE `change_message` `change_message` longtext CHARSET utf8 NOT NULL;