create or replace PROCEDURE query_dep
 (id     IN  departamente.id_departament%TYPE,
  tot_salary OUT angajati.salariul%TYPE) IS
BEGIN
  SELECT   sum(salariul) INTO tot_salary    FROM    angajati
   WHERE   id_departament = id;
END query_dep;
/
--Apel:
set serveroutput on
declare 
nume angajati.nume%type;
salariul angajati.salariul%type;
begin
query_emp(120, nume, salariul);
dbms_output.put_line('Angajatul '||nume||' are salariul '||salariul);
end;
/
