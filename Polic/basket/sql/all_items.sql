select d.id_doc, d.doc_name, d.spec, t.date_visit from doctor d
join tametable t
on d.id_doc=t.id_doc