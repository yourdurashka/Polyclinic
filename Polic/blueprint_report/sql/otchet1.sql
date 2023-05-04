select pac_name, passport, address, birth, data_card from paclent
JOIN visit
ON pacient=id_pac
where name_doc="$input_name"