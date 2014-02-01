drop table if exists entries_test;
create table entries_test (
  id integer primary key autoincrement,
  text text not null,
  painting_id text not null
);
