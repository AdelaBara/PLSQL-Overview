set serveroutput on
declare
cursor cang (pid_dep number) is select * from angajati where id_departament=pid_dep order by salariul asc;
begin
dbms_output.put_line('Departamentul 50');
for rang in cang(50) loop
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
    exit when cang%rowcount>10;
end loop;
dbms_output.put_line('Departamentul 80');
for rang in cang(80) loop
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
    exit when cang%rowcount>10;
end loop;
end;
/