set serveroutput on
declare
cursor cang (pid_dep number) is select * from angajati where id_departament=pid_dep;
rang cang%rowtype;
begin
open cang (20);
dbms_output.put_line('______Departamentul 20');
loop
    fetch cang into rang;
    exit when cang%notfound;
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
end loop;
close cang;

if not cang%isopen then
dbms_output.put_line('______Departamentul 30');
    open cang (30);
    loop
        fetch cang into rang;
        exit when cang%notfound;
        dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
    end loop;
    close cang;
end if;
end;
/