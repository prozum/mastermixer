drop table if exists Products;
drop table if exists Orders;

create table Products (
  Id integer primary key autoincrement,
  Title text not null,
  Text text not null,
  Stat1 integer DEFAULT 0,
  Stat2 integer DEFAULT 0,
  Stat3 integer DEFAULT 0,
  Rate integer DEFAULT 0
);

create table Orders (
  Id integer primary key autoincrement,
  P_Id integer not null,
  Client text not null
);

