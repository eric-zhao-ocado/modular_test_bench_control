def split_string(string):
    main_list = string.split(' ')
    if len(main_list) > 2:
        main_list[1] = main_list[1].replace('(','').replace(')','').split(',')
    return main_list

waypoint = "NAME (1,2,3,4) 80 40"
delay = "Delay 5"
vacuum = "Vacuum 1"
blowoff = "Blowoff"

main_list = []
main_list.append(split_string(waypoint))
main_list.append(split_string(delay))
main_list.append(split_string(vacuum))
main_list.append(split_string(blowoff))

print(main_list)