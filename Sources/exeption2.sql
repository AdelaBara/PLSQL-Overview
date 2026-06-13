-- Ex1.1
-- 1. Scrieti un bloc PL/SQL care sa afiseze salariul unui angajat cu prenumele Ion.   
--    Daca exista mai multi angajati cu acest prenume, afisati un mesaj corespunzator.
--    Daca nu exista niciun angajat cu acest prenume, afisati un mesaj corespunzator.
set SERVEROUTPUT ON
declare 
rang angajati%rowtype;
begin
select * into rang from angajati where prenume='Ion';
dbms_output.put_line(rang.salariul);
EXCEPTION
     WHEN TOO_MANY_ROWS THEN
        DBMS_OUTPUT.PUT_LINE ('Sunt mai multi angajati cu acest prenume');
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE ('Nu exista angajatul cu prenumele precizat');
     WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE ('A aparut o exceptie!');  
end;
/