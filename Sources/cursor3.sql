set serveroutput on
declare
pid_dep number:=80;
cursor cang is select * from angajati where id_departament=pid_dep order by salariul asc;
--rang cang%rowtype;
begin
dbms_output.put_line('Departamentul '||pid_dep);
for rang in cang loop
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
    exit when cang%rowcount>10;
end loop;
pid_dep:=50;
dbms_output.put_line('Departamentul '||pid_dep);
for rang in cang loop
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
    exit when cang%rowcount>10;
end loop;
end;
/