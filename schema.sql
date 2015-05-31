drop table if exists todo;
create table todo (
  id integer primary key autoincrement,
  todo text not null
);
