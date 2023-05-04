SELECT t.id_cab, t.date_visit, d.doc_name, COUNT(CASE WHEN t.visit='+' THEN 1 ELSE NULL END), COUNT(t.visit)
FROM
tametable t
JOIN doctor d
ON t.id_doc=d.id_doc
WHERE date(t.date_visit) = '$input_data'