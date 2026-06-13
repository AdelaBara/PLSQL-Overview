create or replace PROCEDURE query_emp
 (id     IN  angajati.id_angajat%TYPE,
  name   OUT angajati.nume%TYPE,
  salary OUT angajati.salariul%TYPE) IS
BEGIN
  SELECT   nume, salariul INTO name, salary    FROM    angajati
   WHERE   id_angajat = id;
END query_emp;
/
