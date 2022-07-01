import json
import scipy.io as scio


def rap_open_mat(datafile):
    data = scio.loadmat(datafile)["RAP_annotation"][0][0]
    # 图片数 84928  attribute  152
    # print(len(data), type(data))

    # 属性字典
    attributes_dict = {i: data[2][i][0][0] for i in range(len(data[2]))}
    # print(attributes_dict.values())

    # 筛选列表
    stander_list_upper_wear = ["ub-Shirt", "ub-Sweater", "ub-Vest", "ub-TShirt", "ub-Cotton", "ub-Jacket", "ub-SuitUp",
                               "ub-Tight", "ub-ShortSleeve", "ub-Others"]
    stander_list_lower_wear = ["lb-LongTrousers", "lb-Shorts", "lb-Skirt", "lb-ShortSkirt", "lb-LongSkirt", "lb-Dress",
                               "lb-Jeans", "lb-TightTrousers"]
    stander_list_upperbodycolor = ["ub-ColorBlack", "ub-ColorWhite", "ub-ColorGray", "up-ColorRed", "ub-ColorGreen",
                                   "ub-ColorBlue", "ub-ColorSilver", "ub-ColorYellow", "ub-ColorBrown",
                                   "ub-ColorPurple", "ub-ColorPink", "ub-ColorOrange", "ub-ColorMixture",
                                   "ub-ColorOther"]
    stander_list_lowerbodycolor = ["lb-ColorBlack", "lb-ColorWhite", "lb-ColorGray", "lp-ColorRed", "lb-ColorGreen",
                                   "lb-ColorBlue", "lb-ColorSilver", "lb-ColorYellow", "lb-ColorBrown",
                                   "lb-ColorPurple", "lb-ColorPink", "lb-ColorOrange", "lb-ColorMixture",
                                   "lb-ColorOther"]
    stander_list_hat = ["hs-Hat"]
    stander_list_bag = ["attachment-Backpack", "attachment-ShoulderBag", "attachment-HandBag", "attachment-WaistBag",
                        "attachment-PlasticBag", "attachment-PaperBag", "attachment-Other"]
    stander_list_footwear = ["shoes-Leather", "shoes-Sports", "shoes-Boots", "shoes-Cloth", "shoes-Sandals",
                             "shoes-Casual", "shoes-Other"]

    # 图片数 84928
    images_dict = {}
    for idx in range(len(data[0][:])):  # TODO [:3]
        label_dict = {"clothing": "Null", "upper_color": "Null", "lower_color": "Null", "headwear": "Null", "bag": "Null", "footwear": "Null"}

        # 图片名字
        images_name = data[0][idx][0][0].split(".")[0]
        # print(images_name)
        images_dict[images_name] = label_dict

        # 图片属性
        label = data[1][idx]
        # print(len(label))  # 152
        label_dict["clothing"] = []
        label_dict["upper_color"] = []
        label_dict["lower_color"] = []
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
                    label_dict["upper_color"].append(attributes_dict[i])
                elif attributes_dict[i] in stander_list_lowerbodycolor:
                    label_dict["lower_color"].append(attributes_dict[i])
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
    # print(images_dict)
    images_dict = json.dumps(images_dict)
    return images_dict
