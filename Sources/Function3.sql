create or replace FUNCTION tax(value IN NUMBER, procent Number)
 RETURN NUMBER IS
BEGIN
   RETURN (value * procent);
END tax;
/
