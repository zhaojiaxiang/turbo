--向下遍历organizations

drop function if exists getchildgrouplist;

create function `getchildgrouplist`(parentid int)
    returns varchar(1000)
begin
    declare stemp varchar(1000);
    declare stempchd varchar(1000);

    set stemp = '';
    set stempchd = cast(parentid as char);

    while stempchd is not null
        do
            set stemp = concat(stemp, ',', stempchd);
            select group_concat(id) into stempchd from organizations where find_in_set(parent_id, stempchd) > 0 and isgroup = '1';
        end while;
    return substring(stemp, 2);
end;

select getchildgrouplist(3)

drop function if exists getallchildlist;

create function `getallchildlist`(parentid int)
    returns varchar(1000)
begin
    declare stemp varchar(1000);
    declare stempchd varchar(1000);

    set stemp = '';
    set stempchd = cast(parentid as char);

    while stempchd is not null
        do
            set stemp = concat(stemp, ',', stempchd);
            select group_concat(id) into stempchd from organizations where find_in_set(parent_id, stempchd) > 0;
        end while;
    return substring(stemp, 2);
end;

select getallchildlist(3)