set serveroutput on
declare
pid_dep number:=20;
cursor cang is select * from angajati where id_departament=pid_dep;
rang cang%rowtype;
begin
open cang;
dbms_output.put_line('______Departamentul '||pid_dep);
loop
    fetch cang into rang;
    exit when cang%notfound;
    dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
end loop;
close cang;

pid_dep:=50;
dbms_output.put_line('______Departamentul '||pid_dep);
if not cang%isopen then
    open cang;
    loop
        fetch cang into rang;
        exit when cang%notfound;
        dbms_output.put_line('Angajatul '||rang.nume||' are salariul '||rang.salariul);
    end loop;
    close cang;
end if;
end;
/