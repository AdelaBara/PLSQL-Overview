create or replace FUNCTION dml_call_sql(sal NUMBER)
   RETURN NUMBER IS
BEGIN
  INSERT INTO angajati(id_angajat, nume, email, data_angajare, id_functie, salariul)
  VALUES(1, 'Frost', 'jfrost@company.com',SYSDATE, 'SA_MAN', sal);
  RETURN (sal + 100);
END;
/
