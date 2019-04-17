class BatteryInfo(object):
    def __init__(self):
        self.data_time = []
        self.end_time = []
        self.battery_percentage = []
        self.capacity = []
        self.computed = []
        self.computed_drain = []
        self.battery_actual_drain = []
        self.carried_out_what = []
        self.uid_item_info = []
        self.uid_detailed_info = []
        self.uid_detailed_num = []
        self.data_time_begin = []


'''operation
data_time_map, battery_percentage, capacity_map, computed_drain_map,
uid_detailed_info_map
'''

'''into excel
data_time_map, data_time_map_begin, battery_percentage, capacity_map, computed_drain_map,
battery_actual_drain_map, carried_out_what, uid_detailed_info_map, uid_detailed_num_map
'''
