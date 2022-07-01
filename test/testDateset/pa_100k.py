import json
import scipy.io as scio


def pa_out(name_data, label_data, attributes_dict):
    # 筛选列表
    stander_list_upper_wear = ["ShortSleeve", "LongSleeve", "LongCoat"]
    stander_list_lower_wear = ["Trousers", "Shorts", "Skirt&Dress"]
    stander_list_upperbodycolor = []
    stander_list_lowerbodycolor = []
    stander_list_hat = ["Hat"]
    stander_list_bag = ["HandBag", "ShoulderBag"]
    stander_list_footwear = ["boots"]

    images_dict = {}
    for i in range(len(name_data)):  # TODO 去掉范围限制[0:3]
        label_dict = {"clothing": "Null", "upper_color": "Null", "lower_color": "Null", "headwear": "Null", "bag": "Null", "footwear": "Null"}

        # 图片名字
        images_name = name_data[i][0][0][:-4]
        images_dict[images_name] = label_dict

        # 图片属性
        label = label_data[i]
        label_dict["clothing"] = []
        for i in range(len(label)):
            # if label[i] == 1:
            #     print(i, attributes_dict[i])
            # clothing
            if label[i] == 1:
                if (
                    attributes_dict[i]
                    in stander_list_upper_wear + stander_list_lower_wear
                ):
                    label_dict["clothing"].append(attributes_dict[i])
                elif attributes_dict[i] in stander_list_upperbodycolor:
                    label_dict["upper_color"] = [attributes_dict[i]]
                elif attributes_dict[i] in stander_list_lowerbodycolor:
                    label_dict["lower_color"] = [attributes_dict[i]]
                elif attributes_dict[i] in stander_list_hat:
                    label_dict["headwear"] = [attributes_dict[i]]
                elif attributes_dict[i] in stander_list_bag:
                    label_dict["bag"] = [attributes_dict[i]]
                elif attributes_dict[i] in stander_list_footwear:
                    label_dict["footwear"] = [attributes_dict[i]]
        # label_dict
        # print(label_dict)
        for lab in label_dict["clothing"]:
            if lab in stander_list_upper_wear:
                break
            else:
                label_dict["clothing"].append("upper_wear_null")
            if lab in stander_list_lower_wear:
                break
            else:
                label_dict["clothing"].append("lower_wear_null")
    # print(images_list)
    return images_dict


def pa_open_mat(datafile):
    data = scio.loadmat(datafile)
    # print(data.keys())

    # 属性字典
    attributes_dict = {
        i: data["attributes"][i][0][0] for i in range(len(data["attributes"]))
    }

    # print(attributes_dict)

    # test_images
    name_data = data["test_images_name"]
    label_data = data["test_label"]
    test_images_dict = pa_out(name_data, label_data, attributes_dict)

    # train_images
    name_data = data["train_images_name"]
    label_data = data["train_label"]
    train_images_dict = pa_out(name_data, label_data, attributes_dict)

    # val_images
    name_data = data["val_images_name"]
    label_data = data["val_label"]
    val_images_dict = pa_out(name_data, label_data, attributes_dict)

    # 结果(为了输出顺序)
    images_dict = {}
    images_dict |= train_images_dict
    images_dict.update(val_images_dict)
    images_dict.update(test_images_dict)
    # print(images_list)
    images_dict = json.dumps(images_dict)
    return images_dict
