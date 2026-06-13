--Poate fi utilizata in interogari pe tabela departamente fara jonctiune cu tabela angajati sau group by.
create or replace FUNCTION GROUP_DEP (PID_DEP DEPARTAMENTE.ID_DEPARTAMENT%TYPE) RETURN NUMBER
IS
VSUM NUMBER;
BEGIN
SELECT SUM(SALARIUL) INTO VSUM FROM ANGAJATI WHERE ID_DEPARTAMENT=PID_DEP;
RETURN nvl(VSUM,0);
END;
/
