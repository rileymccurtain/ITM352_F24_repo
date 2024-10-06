#Debugging exercise # 4
def get_element(list, index):
    if 0 <= index < len(list):  
        return list[index]
    else:
        return "Index out of range"  

my_list = [1, 2, 3, 4, 5]
print(get_element(my_list, 2))  
print(get_element(my_list, 5))