--Sa se realizeze o functie care primeste ca parametru id_produs si returneaza cantitatea totala comandata din acest produs. Apelati functia dintr-o interogare SQL si dintr-un bloc PL/SQL. Tratați excepțiile apărute. 

create or replace function f_cantitate_comandata_produs (p_id_produs rand_comenzi.id_produs%type)
return number 
is
v_total number;
Begin
select sum(cantitate) into v_total from rand_comenzi where id_produs=p_id_produs;
return nvl(v_total,0);
end;
/

--Apel din SQL:

select distinct id_produs from rand_comenzi;
select id_produs, f_cantitate_comandata_produs(id_produs) from produse;
--Apel din PL/SQL:

declare
v_total number;
begin
v_total:=f_cantitate_comandata_produs(3);
dbms_output.put_line('Au fost comandate: '||v_total);
end;
/

