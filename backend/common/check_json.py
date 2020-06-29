# coding=utf-8
# auther：Liul5
# date：2019/5/30 9:48
# tools：PyCharm
# Python：3.7

data1 = [{"key1": "aa", "key2": "bb", "key3": [{"key31": "aa31"}, {"key32": "bb33"}]}]
data2 = [{"key1": "", "key2": "bb", "key3": [{"key31": "aa31"}, {"key32": "bb33"}]}]

result = True


def check_json(src_data, dst_data):
    global result
    try:
        if isinstance(src_data, str):
            result = src_data == dst_data
            # if src_data != dst_data:
            #     result = "fail"
        elif isinstance(src_data, list):
            if len(src_data) != len(dst_data):
                print("{0}和{1}的长度不相等".format(src_data, dst_data))
                # result = "fail"
                result = False
            else:
                for i in range(len(src_data)):
                    check_json(src_data[i], dst_data[i])

        elif isinstance(src_data, dict):
            for key in src_data:
                if key not in dst_data:
                    print("参数{}不存在！".format(key))
                    # result = "fail"
                    result = False
                else:
                    if isinstance(src_data[key], dict) and isinstance(dst_data[key], dict):
                        check_json(src_data[key], dst_data[key])
                    elif isinstance(src_data[key], list) and isinstance(dst_data[key], list):
                        check_json(src_data[key], dst_data[key])
                    elif not isinstance(src_data[key], type(dst_data[key])):
                        print("参数类型不一致 {0}: {1}, {2}: {3}".format(src_data[key], type(src_data[key]), dst_data[key], type(dst_data[key])))
                        # result = "fail"
                        result = False
        else:
            pass
        return result
    except Exception as e:
        return False


print(check_json(data1, data2))
