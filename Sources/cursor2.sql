set serveroutput on
declare
pid_dep number:=20;
cursor cang is select * from angajati where id_departament=pid_dep;
--rang cang%rowtype;
begin
dbms_output.put_line('______Departamentul '||pid_dep);
for rang in cang loop
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
end loop;
pid_dep:=50;
dbms_output.put_line('______Departamentul '||pid_dep);
for rang in cang loop
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
end loop;
end;
/