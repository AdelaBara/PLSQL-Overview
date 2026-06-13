set serveroutput on
declare
cursor cang is select * from angajati where id_departament=20 for update nowait;
begin
dbms_output.put_line('inainte de modificare ');
for rang in cang loop
    if rang.salariul<8000 then
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
        update angajati
        set salariul=salariul +100
        where current of cang;
    end if;
end loop;

dbms_output.put_line('dupa modificare ');
for rang in cang loop
dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
end loop;

end;
/
rollback;