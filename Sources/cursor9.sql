set serveroutput on
declare 
cursor ccom is select cl.id_client, cl.nume_client, count(c.id_comanda) nr_comenzi, sum(rc.pret*rc.cantitate) total 
    from clienti cl, comenzi c, rand_comenzi rc
where c.id_client=cl.id_client
and c.id_comanda=rc.id_comanda
group by cl.id_client, cl.nume_client 
order by nr_comenzi desc;
begin
for r in ccom loop
    dbms_output.put_line('Clientul '||r.nume_client||' a incheiat '||r.nr_comenzi||' comenzi in valoare de: '||r.total);
    if r.nr_comenzi>3 then
        dbms_output.put_line('Bonus 5%: '||r.total*0.05);
    end if;
    exit when ccom%rowcount>20;
end loop;
end;
/