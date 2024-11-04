create table if not exists filme(
  id integer primary key AUTOINCREMENT,
  nome text not null,
  autor text not null,
  descricao text not null
)