create or replace PROCEDURE add_department(
    name VARCHAR2, mgr NUMBER, loc NUMBER) IS
BEGIN
  INSERT INTO departamente (id_departament, denumire_departament, id_manager, id_locatie)
  VALUES (DEPARTMENTS_SEQ.NEXTVAL, name, mgr, loc);
  DBMS_OUTPUT.PUT_LINE('Added Dept: '||name);
--EXCEPTION
-- WHEN OTHERS THEN
--  DBMS_OUTPUT.PUT_LINE('Err: adding dept: '||name);
END;
/
