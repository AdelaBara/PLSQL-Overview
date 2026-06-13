--Trigger pe tabele virtuale:
--Tabela virtuala V_TOTAL_COMENZI va contine id_client, nr_comanda, data, id_produs si valoarea acestuia.

--Pas 1: Crearea tabelei virtuale V_TOTAL_COMENZI
create or replace view v_total_comenzi
as select c.id_client, c.id_comanda, c.data, r.id_produs, r.cantitate*r.pret as valoare
from comenzi c, rand_comenzi r
where r.id_comanda=c.id_comanda;


--Pas 2: Realizarea triggerului care actualizeaza pretul produselor de pe o anumita comanda in cazul in care se actualizeaza valoarea comandata.

create or replace trigger t_v_total_comenzi
instead of update on v_total_comenzi
for each row
begin
update rand_comenzi
set pret=:new.valoare/cantitate
where id_comanda=:new.id_comanda
and id_produs=:new.id_produs;
end;
/

-- Pas 3: TESTARE

select * from v_total_comenzi where id_comanda=2458;

--preturi inainte de update
select * from rand_comenzi where id_comanda=2458; 

update v_total_comenzi
set valoare=valoare*1.2
where id_comanda=2458;

--preturi dupa update
select * from rand_comenzi where id_comanda=2458; 
rollback;
