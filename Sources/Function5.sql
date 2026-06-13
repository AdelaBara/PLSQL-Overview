--a. Realizați o funcție care primește ca parametru data si returnează nr de luni de la plasarea comenzii cu aceasta data și până în prezent – funcția f_luni_comanda
create or replace function f_luni_comanda (p_data comenzi.data%type)
return number
is
begin
return round(months_between(sysdate, p_data),0) ;
end;
/

--b. Realizați o funcție care primeste parametru id_comanda si returneaza valoarea totala a acesteia  - funcția f_valoare_comanda;
create or replace function f_valoare_comanda (p_nr_comanda comenzi.id_comanda%type)
return number 
is
v_total number;
Begin
select sum(cantitate*pret) into v_total from rand_comenzi where id_comanda=p_nr_comanda;
return v_total;
end;
/

--c. Afișați, folosind un cursor urmatoarele: nr_comanda, nr de luni de la plasarea comenzii si valoarea totala pentru primele 3 comenzi cu valoarea cea mai mare.
select id_comanda, data, F_LUNI_COMANDA(data) as nr_luni, f_valoare_comanda(id_comanda) as total  from comenzi order by 3 desc;
-- ori
select id_comanda, data, f_luni_comanda(data) nr_luni, f_valoare_comanda(id_comanda) total_comanda
from comenzi
where f_valoare_comanda(id_comanda)>8000;
-- utilizand cursorul
declare
cursor c is select id_comanda, data, F_LUNI_COMANDA(data) as nr_luni, f_valoare_comanda(id_comanda) as total  from comenzi order by 4 desc;
begin
for r in c loop
dbms_output.put_line ('Comanda cu numarul:' ||r.id_comanda||' a fost plasata in urma cu '||r.nr_luni||' luni si are valoarea:'||r.total);
exit when c%rowcount>=3;
end loop;
end;
/
