SELECT d.doc_name, d.spec, t.date_visit, t.id_cab from tametable t
JOIN doctor d
ON t.id_doc=d.id_doc
