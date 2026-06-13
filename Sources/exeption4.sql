
-- Exemplu exceptii
-- 1. Se va verifica daca produsul introdus exista in stocuri.
-- 2. Se va verifica daca stocul este suficient pentru a putea onora comanda.
-- 3. Se va verifica daca comanda introdusa exista in tabela rand_comenzi.
-- 4. Se va adauga cantitatea dorita in tabela rand_comenzi.  
-- 5. Se va adauga in tabela errors codul si mesajul erorii.
-- 6. Se va afisa mesajul corespunzator in functie de exceptia intalnita.

select * from rand_comenzi where id_produs in (select id_produs from stocuri);
select * from stocuri;


ACCEPT p_nr_comanda PROMPT 'Va rugam introduceti nr comenzii:' --2399
ACCEPT p_ID_produs   PROMPT 'Precizati produsul:' --2311
ACCEPT p_cantitate   PROMPT 'Cantitatea dorita:' --16
DECLARE
  --exceptie pentru stoc insuficient
  stoc_insuficient EXCEPTION;
  PRAGMA EXCEPTION_INIT (stoc_insuficient, -20201);
  --exceptie pt comanda inexistenta
  comanda_inexistenta EXCEPTION;
  PRAGMA EXCEPTION_INIT (comanda_inexistenta, -20200);
  --variabile locale
  p_nr_comanda NUMBER:= &p_nr_comanda;
  p_ID_produs NUMBER :=&p_ID_produs;
  p_cantitate NUMBER :=&p_cantitate;
  -- p_nr_comanda NUMBER:= 2399;
  -- p_ID_produs NUMBER :=2311;
  -- p_cantitate NUMBER :=20;
  cantitate_stoc number;
  --codul si mesajul erorii
  error_code number ;
  error_message varchar2(255);
  
BEGIN
  --returnam cantitatea disponibila in stoc pentru produsul introdus:
  select stoc into cantitate_stoc from stocuri where id_produs=p_id_produs;
  --verificam daca avem stoc suficient:
  if p_cantitate> cantitate_stoc then
    RAISE_APPLICATION_ERROR(-20201,'Stoc insuficient!');
  else 
      UPDATE  rand_comenzi
      SET     cantitate = cantitate + p_cantitate
      WHERE   id_comanda = p_nr_comanda and id_produs=p_id_produs;
      IF SQL%NOTFOUND THEN
        RAISE_APPLICATION_ERROR(-20200,'Comanda precizata nu exista!');
      END IF;
    end if;
EXCEPTION
  WHEN NO_DATA_FOUND THEN 
  --produsul introdus nu exista
    DBMS_OUTPUT.PUT_LINE('Nu exista produsul!');
    error_code := SQLCODE ;
    error_message := SQLERRM ;
    insert into errors values(user, sysdate, error_code, error_message);
  WHEN stoc_insuficient THEN
    DBMS_OUTPUT.PUT_LINE('Nu exista cantitate suficienta in stoc pentru produsul selectat');
    error_code := SQLCODE ;
    error_message := SQLERRM ;
    insert into errors values(user, sysdate, error_code, error_message);
  WHEN comanda_inexistenta  THEN
    DBMS_OUTPUT.PUT_LINE('Nu exista comanda precizata!');
    error_code := SQLCODE ;
    error_message := SQLERRM ;
    insert into errors values(user, sysdate, error_code, error_message);
END;
/

select * from errors;
commit;
