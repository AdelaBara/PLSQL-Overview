--Realizati o procedura check_jobs_avgsal (pjob_id functii.id_functie%type, pnr out number, psum out number) prin care sa verificati daca angajatii cu această funcție (pjob_id) au salariile mai mari decât salariul mediu corespunzător funcției respective. Returnați numărul angajaților si suma salariilor ce depaseste aceasta medie. 
--a.	declarati o variabila de tip record pentru a afisa informatiile referitoare la functia primita ca parametru;
--b.	declarati un cursor pentru a returna toti angajatii care au aceasta functie;
--c.	declarati o exceptie definita de utilizator prin care sa tratati cazul in care exista salariati cu salariul null;
--d.	in sectiunea executabila realizati urmatoarele:
--	afisati informatiile referitoare la functia primita ca parametru, inclusiv salariul mediu pentru aceasta functie;
--	deschideti cursorul, parcurgeti angajatii si afisati diferenta dintre salariul fiecarui angajat si salariul mediu;
--	actualizati numarul total de angajati  (pnr ) si suma totala a salariilor ce depaseste media (psum).
--	Declansati si tratati exceptia definita de utilizator (salariu null) precum si alte erori aparute. 
--Apelati procedura dintr-un bloc PL/SQL.


create or replace procedure check_jobs_avgsal
(p_id_functie functii.id_functie%type, pnr out number, psum out number)
is
cursor c_emp is select * from angajati where id_functie=p_id_functie;
rec_functie functii%rowtype;
vavg number(7,2);
--exceptie definita de utilizator pt salariul null
salariu_null exception;
pragma exception_init(salariu_null, -20900);
begin
psum:=0;
pnr:=0;
--salariul mediu aferent functiei primite ca parametru
select * into rec_functie from functii where id_functie=p_id_functie;
vavg:=round((rec_functie.salariu_max+rec_functie.salariu_min)/2,2);
dbms_output.put_line('Pentru functia: '||rec_functie.id_functie||' '||rec_functie.denumire_functie||' avem salariul minim: '||rec_functie.salariu_min||' si salariul maxim: '||rec_functie.salariu_max);
dbms_output.put_line('Media este: '||vavg);
for vr_emp in c_emp loop
if vr_emp.salariul <=vavg then
   dbms_output.put_line('Salariatul: '||vr_emp.id_angajat||' '||vr_emp.nume||' are salariul '||vr_emp.salariul||' si este mai mic decat media cu '||to_char(vavg-vr_emp.salariul));
elsif vr_emp.salariul >vavg then
   dbms_output.put_line('Salariatul: '||vr_emp.id_angajat||' '||vr_emp.nume||' are salariul '||vr_emp.salariul||' si este mai mare decat media cu '||to_char(vr_emp.salariul-vavg));
   psum:=psum+vr_emp.salariul-vavg;
   pnr:=pnr+1;
else
    raise_application_error(-20900, 'Salariatul are salariul null');
end if;
end loop;
exception
when no_data_found then
     dbms_output.put_line('Nu exista functie cu acest id!');
when salariu_null then
     dbms_output.put_line('Exista salariati cu salariul neprecizat! Nu se poate realiza corect statistica!');
when others then
     dbms_output.put_line('A aparut o eroare:)!');
end check_jobs_avgsal;
/
--Apel
select * from functii;
--apel pt functia cu id_ul 'SA_REP'
declare
v_nr number;
v_sum number;
begin
check_jobs_avgsal('SA_REP', v_nr, v_sum);
dbms_output.put_line ('Numarul de angajati este: '||v_nr||' iar diferenta este: '||v_sum);
end;
/
