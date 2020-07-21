import json
import scipy.io as scio


def peta_open_mat(datafile):
    data = scio.loadmat(datafile)["peta"][0][0]
    # print(len(data))

    # 属性字典
    attributes_dict = {}
    for i in range(len(data[1])):
        attributes_dict[i] = data[1][i][0][0]
    # print(attributes_dict)

    # 晒选列表
    stander_list_upper_wear = ["upperBodyFormal",  "upperBodyJacket","upperBodyLongSleeve", "upperBodyNoSleeve", "upperBodyPlaid", "upperBodyShortSleeve","upperBodyThinStripes", "upperBodySuit", "upperBodySweater", "upperBodyThickStripes","upperBodyTshirt", "upperBodyOther", "upperBodyVNeck"]
    stander_list_lower_wear = ["lowerBodyCasual", "lowerBodyHotPants","lowerBodyJeans","lowerBodyLongSkirt","lowerBodyPlaid",
                               "lowerBodyThinStripes","lowerBodyShorts","lowerBodyShortSkirt","lowerBodySuits","lowerBodyTrousers",]
    stander_list_upperbodycolor = ["upperBodyBlack",
                                   "upperBodyBlue", "upperBodyBrown", "upperBodyGreen", "upperBodyGrey",
                                   "upperBodyOrange",
                                   "upperBodyPink", "upperBodyPurple", "upperBodyRed", "upperBodyWhite",
                                   "upperBodyYellow"]
    stander_list_lowerbodycolor = ["lowerBodyBlack", "lowerBodyBlue", "lowerBodyBrown", "lowerBodyGreen",
                                   "lowerBodyGrey",
                                   "lowerBodyOrange", "lowerBodyPink", "lowerBodyPurple", "lowerBodyRed",
                                   "lowerBodyWhite",
                                   "lowerBodyYellow"]
    stander_list_hat = ["accessoryHat"]
    stander_list_bag = ["HandBag", "ShoulderBag", "carryingMessengerBag", "carryingPlasticBags"]
    stander_list_footwear = ["footwearBoots", "footwearLeatherShoes", "footwearSandals", "footwearShoes",
                             "footwearSneaker", "footwearStocking"]
    # 总图片数 19000 x 109
    # print(len(data[0]))  # 19000
    images_dict = {}
    for idx in range(len(data[0])):  # TODO 去掉范围限制[0:3]
        label_dict = {"clothing": "Null", "upper_color": "Null", "lower_color": "Null", "headwear": "Null", "bag": "Null", "footwear": "Null"}

        # 图片名字
        images_name = '%05d' % (idx + 1)
        images_dict[images_name] = label_dict

        # 图片属性
        label = data[0][idx][4:]
        label_dict["clothing"] = []
        label_dict["upper_color"] = []
        label_dict["lower_color"] = []
        for i in range(len(label)):
            # if label[i] == 1:
            #     print(i, attributes_dict[i])
            # clothing
            if label[i] == 1 and attributes_dict[i] in stander_list_upper_wear + stander_list_lower_wear:
                label_dict["clothing"].append(attributes_dict[i])
            # upper_color
            elif label[i] == 1 and attributes_dict[i] in stander_list_upperbodycolor:
                label_dict["upper_color"].append(attributes_dict[i])
            # lower_color
            elif label[i] == 1 and attributes_dict[i] in stander_list_lowerbodycolor:
                label_dict["lower_color"].append(attributes_dict[i])
            # headwear
            elif label[i] == 1 and attributes_dict[i] in stander_list_hat:
                label_dict["headwear"] = []
                label_dict["headwear"].append(attributes_dict[i])
            # bag
            elif label[i] == 1 and attributes_dict[i] in stander_list_bag:
                label_dict["bag"] = []
                label_dict["bag"].append(attributes_dict[i])
            # footwear
            elif label[i] == 1 and attributes_dict[i] in stander_list_footwear:
                label_dict["footwear"] = []
                label_dict["footwear"].append(attributes_dict[i])

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
