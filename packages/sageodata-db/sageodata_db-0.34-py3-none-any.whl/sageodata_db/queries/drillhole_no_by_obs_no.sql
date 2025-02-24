SELECT drillhole_no AS dh_no,                                     --col
       unit_no      AS unit_long,                                 --col
       (Trim(To_char(obs_well_plan_code))
              || Trim(To_char(obs_well_seq_no, '000'))) AS obs_no --col
FROM   dhdb.dd_drillhole_vw
WHERE  (
              Trim(To_char(obs_well_plan_code))
                     || Trim(To_char(obs_well_seq_no, '000'))) IN {OBS_NO} --arg OBS_NO (sequence of str): observation well IDs in six-character format e.g. 'YAT053'
AND deletion_ind = 'N'