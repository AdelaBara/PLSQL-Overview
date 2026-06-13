create or replace package p_manag_angajati
is
v_total_salarii number;
function caut_angajat(p_id_angajat angajati.id_angajat%type) return angajati.nume%type;
function caut_angajat(p_nume angajati.nume%type, p_id_dep departamente.id_departament%type) return angajati.salariul%type;
function venit_angajat(p_id_angajat angajati.id_angajat%type) return  number;
function venit_angajat(p_salariul angajati.salariul%type, p_com angajati.comision%type) return  number;
procedure calc_venit_dep(p_id_dep departamente.id_departament%type, nr_angajati out number, total_venit out number);
end;
/


create or replace package body p_manag_angajati
is
function caut_angajat(p_id_angajat angajati.id_angajat%type) return angajati.nume%type
is
v_nume angajati.nume%type;
begin
select nume into v_nume from angajati where id_angajat =p_id_angajat;
return v_nume;
exception
when no_data_found then
return null;
when too_many_rows then
v_nume:='Mai multi angajati';
return v_nume;
end caut_angajat;

function caut_angajat(p_nume angajati.nume%type, p_id_dep departamente.id_departament%type) return angajati.salariul%type
is
v_sal angajati.salariul%type;
begin
select salariul into v_sal from angajati where nume=p_nume and id_departament=p_id_dep;
return v_sal;
exception
when no_data_found or too_many_rows then
return null;
end caut_angajat;

function venit_angajat(p_id_angajat angajati.id_angajat%type) return  number
is
v_com angajati.comision%type;
v_sal angajati.salariul%type;
begin
select salariul, comision into v_sal, v_com from angajati where id_angajat=p_id_angajat;
return v_sal*(1+nvl(v_com,0));
exception
when no_data_found then
return null;
end venit_angajat;

function venit_angajat(p_salariul angajati.salariul%type, p_com angajati.comision%type) return  number
is
begin
return p_salariul*(1+nvl(p_com,0));
end venit_angajat;

procedure calc_venit_dep(p_id_dep departamente.id_departament%type, nr_angajati out number, total_venit out number)
is 
begin
select count(id_angajat), sum(venit_angajat(salariul, comision)) into nr_angajati,total_venit
from angajati
where id_departament=p_id_dep;
v_total_salarii:=v_total_salarii+total_venit;
exception
when no_data_found then 
dbms_output.put_line('Nu exista departament cu acest id!');
end calc_venit_dep;

begin
v_total_salarii:=0;
end;
/

-- apel

select * from angajati;
set serveroutput on


declare
v_sal number;
v_nr number;
v_sal_tot number;
begin
v_sal:=p_manag_angajati.caut_angajat('&nume','&dep');
dbms_output.put_line('Angajatul are salariul '||v_sal);
dbms_output.put_line('Salariul departamentelor este '||p_manag_angajati.v_total_salarii);
P_MANAG_ANGAJATI.CALC_VENIT_DEP(90, v_nr, v_sal_tot);
dbms_output.put_line('In departamentul 90 sunt '||v_nr || ' angajati si au sal '||v_sal_tot);
dbms_output.put_line('Salariul departamentelor este '||p_manag_angajati.v_total_salarii);
P_MANAG_ANGAJATI.CALC_VENIT_DEP(50, v_nr, v_sal_tot);
dbms_output.put_line('In departamentul 50 sunt '||v_nr || ' angajati si au sal '||v_sal_tot);
dbms_output.put_line('Salariul departamentelor parcurse pana in prezent este '||p_manag_angajati.v_total_salarii);
end;
/