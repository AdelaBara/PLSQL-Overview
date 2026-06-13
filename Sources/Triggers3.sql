--Realizati un trigger pe tabela CLIENTI care sa nu permita diminuarea limitei de credit sub 10.

create or replace trigger T_limita_credit_clienti
before update of limita_credit on clienti
for each row
when (new.limita_credit<10)
begin
raise_application_error (-20200, 'Nu puteti diminua limita de credit!');
end;
/

-- TESTARE
select * from clienti
where id_client=478;

update clienti
set limita_credit=5 where id_client=478;
