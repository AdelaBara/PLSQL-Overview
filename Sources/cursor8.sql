set serveroutput on
declare
cursor cd is select d.denumire_departament, d.id_departament, count(a.id_angajat) nr_angajati from departamente d, angajati a 
    where a.id_departament=d.id_departament
    group by d.denumire_departament, d.id_departament;
cursor ca (p_id_dep number) is select * from angajati where id_departament=p_id_dep order by salariul desc;
begin
for rd in cd loop
    dbms_output.put_line('In departamentul '||rd.denumire_departament||' lucreaza '||rd.nr_angajati||' angajati!');
    dbms_output.put_line('Lista angajatilor cu cele mai mari salarii:');
    for ra in ca(rd.id_departament) loop
        dbms_output.put_line('Angajatul '||ra.nume||' ' ||ra.prenume||' are salariul '||ra.salariul);
        exit when ca%rowcount>=5;
    end loop;
end loop;
end;
/
        


