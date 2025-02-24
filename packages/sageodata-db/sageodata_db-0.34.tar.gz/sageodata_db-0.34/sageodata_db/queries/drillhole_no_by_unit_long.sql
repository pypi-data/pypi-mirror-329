SELECT drillhole_no AS dh_no,                                     --col
       unit_no      AS unit_long,                                 --col
       (Trim(To_char(obs_well_plan_code))
              || Trim(To_char(obs_well_seq_no, '000'))) AS obs_no --col
FROM   dhdb.dd_drillhole_vw
WHERE  unit_no IN {UNIT_LONG} --arg UNIT_LONG (sequence of int): unit numbers in nine-character integer format e.g. 653201234
AND deletion_ind = 'N'