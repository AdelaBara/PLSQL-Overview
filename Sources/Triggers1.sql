--Realizati un trigger care sa verifice existenta stocului pentru produsele comandate (se va crea tabela STOCURI). In cazul in care stocul este insuficient, cantitatea comandata se va micsora pana la limita stocului. 
-- Triggerul va actualiza automat tabela STOCURI dupa preluarea comenzii.

--Pas 1: In SQL Developer se creaza tabela stocuri:
Drop table stocuri;
create table stocuri as select id_produs from produse;
alter table stocuri
add stoc number (3);
UPDATE STOCURI
SET STOC=15;
Commit;

--Pas 2: Se creaza Triggerul
create or replace trigger t_verif_stoc
before insert on rand_comenzi
for each row
declare
v_stoc stocuri.stoc%type;
begin
select stoc into v_stoc from stocuri where id_produs=:new.id_produs;
if :new.cantitate > v_stoc then
:new.cantitate:=v_stoc;
end if;
update stocuri
set stoc=stoc-:new.cantitate
where id_produs=:new.id_produs;
end;
/

--Pas 3: se testeaza executia triggerului in SQL Developer
select * from stocuri;
insert into rand_comenzi values(2392, 3110, 7, 20);
select * from rand_comenzi where id_comanda=2392;
select * from stocuri where id_produs=3110;
rollback;

--Modificati triggerul astfel incat sa apeleze o procedura stocata care sa actualizeze stocul si sa calculeze necesarul de aprovizionat.

--Pas 1: Adaugam in tabela Stocuri 2 coloane: NECESAR number si DATA date.
alter table stocuri
add (necesar number(3), data date);
select * from stocuri;


-- Pas 2: Creati o procedura:
create or replace procedure p_necesar_aprovizionare(p_id_produs number, p_cant in out number,  p_data date)
is
v_stoc stocuri.stoc%type;
begin
select stoc into v_stoc from stocuri where id_produs=p_id_produs;
if p_cant >v_stoc then
update stocuri
set stoc=0, necesar=necesar+p_cant- v_stoc, data=p_data
where id_produs=p_id_produs;
p_cant:=v_stoc;

else 
update stocuri
set stoc=v_stoc-p_cant
where id_produs=p_id_produs;
end if;
end;
/

-- Pas 3: Modificati triggerul astfel incat sa apeleze procedura:

create or replace trigger t_verif_stoc
before insert on rand_comenzi
for each row
declare
begin
p_necesar_aprovizionare(:new.id_produs,:new.cantitate, sysdate);
end;
/

-- Sau in varianta cu call:
create or replace trigger t_verif_stoc
before insert on rand_comenzi
for each row
call p_necesar_aprovizionare(:new.id_produs,:new.cantitate, sysdate)


--Pas 4: Testarea triggerului:
select * from stocuri;
update stocuri
set necesar=0;
insert into rand_comenzi values(2392, 3110, 7, 20);
select * from rand_comenzi where id_comanda=2392;
select * from stocuri where id_produs=3110;
rollback;
