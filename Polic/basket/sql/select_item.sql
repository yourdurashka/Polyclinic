select doc_name, spec, date_visit from doctor d
join tametable t on d.id_doc=t.id_doc
where d.id_doc = '$id_doc'