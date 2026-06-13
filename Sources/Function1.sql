create or replace FUNCTION get_sal
 (id angajati.id_angajat%TYPE) RETURN NUMBER IS
  sal angajati.salariul%TYPE := 0;
BEGIN
  SELECT salariul
  INTO   sal
  FROM   angajati         
  WHERE  id_angajat = id;
  RETURN sal;
exception
when no_data_found then
    return 0;
END get_sal;
/
