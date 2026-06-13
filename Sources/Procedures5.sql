--Realizati o procedura care primeste p_id si p_sal ca parametrii de tip IN si p_code de tip OUT. 
--Procedura verifica daca noul salariul (p_sal) angajatului cu id-ul primit ca parametru (p_id) este cuprins intre limitele MIN_SALARY si MAX_ SALARY din tabela FUNCTII corespunzătoare funcției deținute de acest angajat.
--Dacă salariul este între limitele permise se actualizeaza salariul angajatului și se returnează p_code:=1 verificând execuția comenzii UPDATE cu ajutorul cursorului implicit (SQL%FOUND). 
--Daca salariul este in afara limitelor, se va declasa o exceptie si p_code =0.

create or replace procedure check_min_max_sal (p_sal angajati.salariul%type, p_id angajati.id_angajat%type, p_code OUT number)
is
v_min number;
v_max number;
sal_out_of_limits exception;
pragma EXCEPTION_INIT (sal_out_of_limits, -20200); --exceptie definita de utilizator
begin
-- returnam limitele min, max pt functia angajatului
select salariu_min, salariu_max into v_min, v_max from functii 
where id_functie = (select id_functie from angajati where id_angajat=p_id); 
--verificam limitele
if p_sal between v_min and v_max then
--actualizam salariul
    update angajati
    set salariul=p_sal
    where id_angajat=p_id;
    if sql%found then 
        p_code:=1;
    end if;
else
--declansam exceptia
    raise_application_error(-20200, 'Salariul este in afara limitelor permise de job_id');
end if;
exception
when sal_out_of_limits then
    p_code:=0;
end;
/

--Apelul procedurii pentru angajatul cu ID-ul 110:
select * from angajati where id_angajat=110;

set serveroutput on
declare
v_code number;
begin
check_min_max_sal(9000, 110,v_code);
dbms_output.put_line ('A fost actualizat '||v_code||' angajat');
end;
/

--Modificati exemplul de mai sus si tratati exceptia NO_DATA_FOUND:

create or replace procedure check_min_max_sal (p_sal angajati.salariul%type, p_id angajati.id_angajat%type, p_code OUT number)
is
v_min number;
v_max number;
sal_out_of_limits exception;
pragma EXCEPTION_INIT (sal_out_of_limits, -20200); --exceptie definita de utilizator
begin
-- returnam limitele min, max pt functia angajatului
select salariu_min, salariu_max into v_min, v_max from functii 
where id_functie = (select id_functie from angajati where id_angajat=p_id); 
--verificam limitele
if p_sal between v_min and v_max then
--actualizam salariul
    update angajati
    set salariul=p_sal
    where id_angajat=p_id;
    if sql%found then 
        p_code:=1;
    end if;
else
--declansam exceptia
    raise_application_error(-20200, 'Salariul este in afara limitelor permise de job_id');
end if;
exception
when sal_out_of_limits then
    p_code:=0;
when no_data_found then
    p_code:=-1;
end;
/
--Apelul procedurii:
declare
v_code number;
begin
check_min_max_sal(8900, 110,v_code);
if v_code=0 then
dbms_output.put_line ('Salariul este in afara limitelor!');
elsif v_code=-1 then
dbms_output.put_line ('Nu exista angajatul');
else
dbms_output.put_line ('A fost actualizat '||v_code||' angajat');
end if;
end;
/
