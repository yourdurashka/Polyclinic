select v.name_doc, count(id_visit) from visit v
where year(v.date_visit)='$Byear' and month(v.date_visit)='$Bmonth' and v.name_doc='$Dname'
