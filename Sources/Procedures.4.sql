create or replace PROCEDURE create_departments (pid_loc departamente.id_locatie%type) IS
BEGIN
  add_department('Media', 100, pid_loc);
  add_department('Editing', 99, pid_loc);
  add_department('Advertising', 101, pid_loc);
  exception
  when others then
  DBMS_OUTPUT.PUT_LINE('A aparut o exceptie!');
END;
/
