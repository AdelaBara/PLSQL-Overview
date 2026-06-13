-- Realizati un trigger pe tabela Angajati care se declanseaza la actualizarea functiei unui angajat si adauga in tabela istoric_functii functia detinuta anterior de acesta. 
create or replace trigger t_istoric
after update of id_functie on angajati
for each row
begin
insert into istoric_functii values (:old.id_angajat, :old.data_angajare, sysdate, :old.id_functie, :old.id_departament);
end;
/

-- TESTARE
select * from istoric_functii where id_angajat=103;
select * from angajati where id_angajat=103;

update angajati
set id_functie='SA_REP'
where id_angajat=103;

select * from istoric_functii where id_angajat=103;

rollback;
