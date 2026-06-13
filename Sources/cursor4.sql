set serveroutput on

begin
for rang in (select * from angajati where id_departament=80) loop
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
end loop;

for rang in (select nume, salariul from angajati where id_departament=50) loop
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
end loop;
end;
/