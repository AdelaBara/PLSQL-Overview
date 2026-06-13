-- 1. Scrieti un bloc PL/SQL care sa adauge un departament in tabela departamente. Tratati exceptiile
-- corespunzatoare. Daca se incearca adaugarea unui departament fara denumire, afisati un mesaj corespunzator

declare
insert_exc EXCEPTION;
PRAGMA EXCEPTION_INIT(insert_exc, -02290);
error_code      NUMBER;
error_message   VARCHAR2(255);
begin
insert into departamente (id_departament, denumire_departament) values (290, null);
EXCEPTION
WHEN insert_exc then
DBMS_OUTPUT.PUT_LINE('Nu se poate adauga un departament fara denumire!');
error_code := SQLCODE ;
error_message := SQLERRM ;
INSERT INTO errors (e_user, e_date, error_code,   error_message) VALUES(USER,SYSDATE,error_code, error_message);

end;
/
commit;
--ROLLBACK;
select * from errors;