--Exemplul 2 - User defined exceptions
--Se va crea o exceptie definita de utilizator care va verifica daca un departament exista in baza de date in urma operatiei de UPDATE
ACCEPT deptno PROMPT 'Please enter the department number:' 
ACCEPT name   PROMPT 'Please enter the department name:'

DECLARE
  invalid_department EXCEPTION;
  pragma exception_init(invalid_department, -20200);
  name VARCHAR2(20):='&name';
  deptno NUMBER :=&deptno;
  cod_eroare number;
  mes_eroare varchar2(255);
BEGIN
  UPDATE  departamente
  SET     denumire_departament = name --ITC
  WHERE   id_departament = deptno;--500
  IF SQL%NOTFOUND THEN
    RAISE_application_error(-20200, 'Nu exista departamentul cu ID-ul specificat!');
  END IF;
DBMS_OUTPUT.PUT_LINE('S-a actualizat departamentul!');
EXCEPTION
  WHEN invalid_department  THEN
    DBMS_OUTPUT.PUT_LINE('No such department id.');
    cod_eroare:=sqlcode;
    mes_eroare:=sqlerrm;
    INSERT INTO errors (e_user, e_date, error_code,   error_message) VALUES(USER,SYSDATE,cod_eroare, mes_eroare);
END;
/

select * from departamente where ID_DEPARTAMENT=500;

select * from errors;
commit;