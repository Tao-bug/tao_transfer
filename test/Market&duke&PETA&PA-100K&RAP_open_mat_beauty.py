import os
import json
import scipy.io as scio


def market_open_mat(datafile):
    mat = scio.loadmat(datafile)
    att = mat['market_attribute']
    # print(att)

    market_attribute = ['image_index', 'age', "backpack", "bag", "handbag", "clothes", "down", "up",
                        "hair", "hat", "gender", "upblack", "upwhite", "upred", "uppurple", "upyellow",
                        "upgray", "upblue", "upgreen", "downblack", "downwhite", "downpink", "downpurple", "downyellow",
                        "downgray", "downblue", "downgreen", "downbrown"]
    all_data = {}
    for i in range(len(att[0][0])):
        if i == 0:
            market_attribute = ['image_index', 'age', 'backpack', 'bag', 'handbag', 'clothes', 'down', 'up', 'hair',
                                'hat', 'gender', 'upblack', 'upwhite', 'upred', 'uppurple', 'upyellow', 'upgray',
                                'upblue', 'upgreen', 'downblack', 'downwhite', 'downpink', 'downpurple', 'downyellow',
                                'downgray', 'downblue', 'downgreen', 'downbrown']
        else:
            market_attribute = ['image_index', 'age', 'backpack', 'bag', 'handbag', 'downblack', 'downblue',
                                'downbrown', 'downgray', 'downgreen', 'downpink', 'downpurple', 'downwhite',
                                'downyellow', 'upblack', 'upblue', 'upgreen', 'upgray', 'uppurple', 'upred', 'upwhite',
                                'upyellow', 'clothes', 'down', 'up', 'hair', 'hat', 'gender']
        w = att[0][0][i]

        for j in range(len(w[0][0][0][0])):
            a = []
            data = {}
            out_data = {}
            wq = len(w[0][0]) - 1
            a.append(w[0][0][wq][0][j][0])
            for q in range(len(w[0][0]) - 1):
                #
                a.append(w[0][0][q][0][j])
            for i in range(len(market_attribute)):
                data[market_attribute[i]] = a[i]
            # print(a)
            # print(data)
            # out_data['image_index'] = data['image_index']
            out_data['clothing'] = "Null"
            clothing = []
            if data["clothes"] == 1:
                clothing.append("dress")
            else:
                clothing.append("pants")
            if data['up'] == 1:
                clothing.append('long sleeve')
            else:
                clothing.append('short sleeve')
            out_data['clothing'] = clothing
            upper = ["upblack", "upwhite", "upred", "uppurple", "upyellow", "upgray", "upblue", "upgreen"]
            upper_dic = {"upblack": 'black', "upwhite": 'white', "upred": 'red', "uppurple": 'purple',
                         "upyellow": 'yellow', "upgray": 'gray', "upblue": 'blue', "upgreen": 'green'}
            out_data['upper_color'] = "Null"
            for up in upper:
                if data[up] == 2:
                    out_data['upper_color'] = [upper_dic[up]]
                else:
                    out_data['upper_color'] = ["Null"]
            downer = ["downblack", "downwhite", "downpink", "downpurple", "downyellow", "downgray", "downblue",
                      "downgreen", "downbrown"]
            downer_dic = {"downblack": 'black', "downwhite": 'white', "downpink": 'pink', "downpurple": 'purple',
                          "downyellow": 'yellow', "downgray": 'gray', "downblue": 'blue', "downgreen": 'green',
                          "downbrown": 'brown'}
            out_data['lower_color'] = "Null"
            for down in downer:
                if data[down] == 2:
                    out_data['lower_color'] = [downer_dic[down]]
            if data["hat"] == 1:
                out_data['headwear'] = "Null"
            else:
                out_data['headwear'] = ['hat']
            ue_bag = ["backpack", "bag", "handbag"]
            out_data['bag'] = "Null"
            for bbag in ue_bag:
                if data[bbag] == 2:
                    out_data['bag'] = [bbag]
            out_data['footwear'] = "Null"
            all_data[str(data['image_index'])] = out_data
    # print(len(all_data))
    # print(all_data.keys())
    result_dict = json.dumps(all_data)
    return result_dict


def duke_open_mat(datafile):
    mat = scio.loadmat(datafile)
    att = mat['duke_attribute']
    all_data = {}

    for i in range(len(att[0][0])):
        if i == 0:
            duke_attribute = ['image_index', 'backpack', 'bag', 'handbag', 'boots', 'gender',
                              'hat', 'shoes', 'top', 'downblack', 'downwhite',
                              'downred', 'downgray', 'downblue', 'downgreen',
                              'downbrown', 'upblack', 'upwhite', 'upred', 'uppurple', 'upgray', 'upblue', 'upgreen',
                              'upbrown']
        else:
            duke_attribute = ['image_index', 'boots', 'shoes', 'top', 'gender', 'hat', 'backpack', 'bag', 'handbag',
                              'downblack', 'downwhite', 'downred', 'downgray', 'downblue', 'downgreen', 'downbrown',
                              'upblack', 'upwhite', 'upred', 'upgray', 'upblue', 'upgreen', 'uppurple', 'upbrown']
        w = att[0][0][i]
        for j in range(len(w[0][0][0][0])):
            a = []
            data = {}
            out_data = {}
            wq = len(w[0][0]) - 1
            a.append(w[0][0][wq][0][j][0])
            for q in range(len(w[0][0])):
                a.append(w[0][0][q][0][j])
            for i in range(len(duke_attribute)):
                data[duke_attribute[i]] = a[i]
            # out_data['image_index'] = data['image_index']
            out_data['clothing'] = "Null"
            if data['top'] == 1:
                out_data['clothing'] = ['short upper body clothing']
            else:
                out_data['clothing'] = ['long upper body clothing']
            upper = ["upblack", "upwhite", "upred", "uppurple", "upgray", "upblue", "upgreen", "upbrown"]
            downer = ["downblack", "downwhite", "downred", "downgray", "downblue", "downgreen", "downbrown"]
            upper_dic = {"upblack": 'black', "upwhite": 'white', "upred": 'red', "uppurple": 'purple', "upgray": 'gray',
                         "upblue": 'blue', "upgreen": 'green', "upbrown": 'brown'}
            downer_dic = {"downblack": 'black', "downwhite": 'white', "downred": 'red', "downgray": 'gray',
                          "downblue": 'blue', "downgreen": 'green', "downbrown": 'brown'}
            out_data['upper_color'] = "Null"
            for up in upper:
                if data[up] == 2:
                    out_data['upper_color'] = [upper_dic[up]]
            out_data['lower_color'] = "Null"
            for down in downer:
                if data[down] == 2:
                    out_data['lower_color'] = [downer_dic[down]]
            if data["hat"] == 1:
                out_data['headwear'] = "Null"
            else:
                out_data['headwear'] = ['hat']
            ue_bag = ["backpack", "bag", "handbag"]
            out_data['bag'] = "Null"
            for bbag in ue_bag:
                if data[bbag] == 2:
                    out_data['bag'] = [bbag]
            if data['boots'] == 1:
                out_data['footwear'] = "Null"
            else:
                out_data['footwear'] = ['boots']
            all_data[str(data['image_index'])] = out_data
    # print(len(all_data))
    # print(all_data)
    result_dict = json.dumps(all_data)
    return result_dict


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
            if label[i] == 1 and attributes_dict[i] in stander_list_upper_wear + stander_list_lower_wear:
                label_dict["clothing"].append(attributes_dict[i])
            # upper_color
            elif label[i] == 1 and attributes_dict[i] in stander_list_upperbodycolor:
                label_dict["upper_color"] = []
                label_dict["upper_color"].append(attributes_dict[i])
            # lower_color
            elif label[i] == 1 and attributes_dict[i] in stander_list_lowerbodycolor:
                label_dict["lower_color"] = []
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
    # print(images_list)
    return images_dict


def pa_open_mat(datafile):
    data = scio.loadmat(datafile)
    # print(data.keys())

    # 属性字典
    attributes_dict = {}
    for i in range(len(data["attributes"])):
        attributes_dict[i] = data["attributes"][i][0][0]
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
    images_dict.update(train_images_dict)
    images_dict.update(val_images_dict)
    images_dict.update(test_images_dict)
    # print(images_list)
    images_dict = json.dumps(images_dict)
    return images_dict


def rap_open_mat(datafile):
    data = scio.loadmat(datafile)["RAP_annotation"][0][0]
    # 图片数 84928  attribute  152
    # print(len(data), type(data))

    # 属性字典
    attributes_dict = {}
    for i in range(len(data[2])):
        attributes_dict[i] = data[2][i][0][0]
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


def dataset_main(dataset, datafile):
    if dataset.lower() == "market":
        images_dict = market_open_mat(datafile)
    elif dataset.lower() == "duke":
        images_dict = duke_open_mat(datafile)
    elif dataset.lower() == "peta":
        images_dict = peta_open_mat(datafile)
    elif dataset.lower() == "pa-100k":
        images_dict = pa_open_mat(datafile)
    elif dataset.lower() == "rap":
        images_dict = rap_open_mat(datafile)
    else:
        images_dict = [{'total_num': 0}, {"err": "输入有误"}]
        # print("输入有误")
    return images_dict


def look_up(path, dataset_name, datafile):
    """
    在数据集中的属性中查询图片属性
    :param path: 图片路径
    :param dataset_name: 数据集名字
    :param datafile: 属性记录文件
    :return:
    """
    # 数据集全部图片及属性
    # 从json文件读取
    # json_path = "/Users/tao/Desktop/test/dataset_json/" + dataset_name + "_mat.json"
    # with open(json_path, "r") as f:
    #     result_dict = f.read()
    # 从原mat文件读取
    result_dict = dataset_main(dataset_name, datafile)
    images_dict = json.loads(result_dict)
    # print(result_dict, type(result_dict))

    # 查询属性
    path = os.path.join(path, dataset_name.lower())
    file_list = os.listdir(path)
    if ".DS_Store" in file_list:
        file_list.remove(".DS_Store")
    file_list.sort()
    # print(file_list)  # 图片名字
    image_label = {}
    for img in file_list[:3]:  # TODO [:3]
        if dataset_name.lower() in ["market", "duke"]:
            image_index = img.split("_")[0]
        else:
            image_index = img.split(".")[0]
        # print(image_index)
        image_label[image_index] = images_dict[image_index]
        # print(image_lab)
    image_label = json.dumps(image_label)
    return image_label


def attribute_map(images_dict):
    """属性映射"""
    images_dict = json.loads(images_dict)
    # 属性值为空列表，代表不具备该属性
    # 属性映射
    # upper_wear_stander_dict = {"长袖", "短袖", "连衣裙"}
    upper_wear_stander_dict = {"Null": "未知", "upper_wear_null":"未知","ub-Shirt":"短袖", "ub-Sweater":"长袖", "ub-Vest":"短袖","ub-TShirt":"短袖","ub-Cotton":"长袖","ub-Jacket":"长袖","ub-SuitUp":"长袖","ub-Tight":"长袖","ub-ShortSleeve":"短袖","ub-Others":"未知", "lb-Dress":"连衣裙",
                               "upperBodyFormal":"长袖","upperBodyJacket":"长袖","upperBodyLongSleeve":"长袖", "upperBodyNoSleeve":"短袖","upperBodyPlaid":"长袖","upperBodyShortSleeve":"短袖","upperBodyThinStripes":"长袖","upperBodySuit":"长袖","upperBodySweater":"长袖",
                               "upperBodyThickStripes":"长袖","upperBodyTshirt":"短袖","upperBodyOther":"未知","upperBodyVNeck":"短袖","ShortSleeve":"短袖","LongSleeve":"长袖","LongCoat":"长袖","long upper body clothing":"长袖","short upper body clothing":"短袖","dress":"连衣裙",
                               "long sleeve":"长袖","short sleeve":"短袖",}
    # lower_wear_stander_dict = {"长裤", "短裤", "短裙"}
    lower_wear_stander_dict = {"Null": "未知","lower_wear_null":"未知","lb-LongTrousers": "长裤", "lb-Shorts": "短裤", "lb-Skirt": "短裙","lb-ShortSkirt": "短裙","lb-LongSkirt": "短裙", "lb-Jeans": "长裤","lb-TightTrousers": "长裤",
                               "lowerBodyCasual":"长裤","lowerBodyHotPants":"短裤","lowerBodyJeans":"长裤","lowerBodyLongSkirt": "短裙","lowerBodyPlaid":"长裤","lowerBodyThinStripes":"长裤","lowerBodyShorts": "短裤","lowerBodyShortSkirt": "短裤",
                               "lowerBodySuits": "长裤","lowerBodyTrousers":"长裤","Trousers":"长裤","Shorts": "短裤","Skirt&Dress":"短裙","pants":"长裤",}
    # color_stander_dict = {"红", "橙", "黄", "绿", "蓝", "紫", "粉", "黑", "白", "灰", "棕", "未知"}
    color_stander_dict = {"Null": "未知","up-ColorRed": "红", "ub-ColorOrange":"橙", "ub-ColorYellow":"黄", "ub-ColorGreen":"绿", "ub-ColorBlue":"蓝", "ub-ColorPurple":"紫", "ub-ColorPink":"粉", "ub-ColorBlack":"黑", "ub-ColorWhite":"白", "ub-ColorGray":"灰", "ub-ColorSilver":"灰", "ub-ColorBrown":"棕", "ub-ColorMixture":"未知", "ub-ColorOther":"未知", "lb-ColorMixture":"未知","lb-ColorOther":"未知","lb-ColorBlack":"黑", "lb-ColorWhite":"白", "lb-ColorRed":"红", "lb-ColorGreen":"绿","lb-ColorBlue":"蓝", "lb-ColorYellow":"黄", "lb-ColorGray":"灰", "lb-ColorSilver":"灰","lb-ColorBrown":"棕","lb-ColorPurple":"紫", "lb-ColorPink":"粉","lb-ColorOrange":"橙","Black": "黑","Brown":"棕","Pink":"粉","White": "白", "Red": "红", "Green": "绿", "Blue": "蓝", "Yellow": "黄", "Grey": "灰", "Purple": "紫", "Orange": "橙",
                          "black":"黑","white":"白", "red":"红","purple":"紫","gray":"灰","blue":"蓝","green":"绿","brown":"棕","pink":"粉",}
    # bag_stander_dict = {"有", "无"}
    bag_stander_dict = {"Null":"无", "attachment-Backpack":"有", "attachment-ShoulderBag":"有", "attachment-HandBag":"有", "attachment-WaistBag":"有","attachment-PlasticBag":"有","attachment-PaperBag":"有","attachment-Other":"有","HandBag":"有","ShoulderBag":"有","carryingMessengerBag":"有","carryingPlasticBags":"有","ackpack":"有","backpack":"有",}
    # headwear_stander_dict = {"有", "无"}
    headwear_stander_dict = {"Null":"无", "hs-Hat":"有", "accessoryHat":"有","Hat":"有","hat":"有"}

    # 原有属性==>映射
    for img_idx in images_dict.keys():
        # clothing
        if images_dict[img_idx]["clothing"] != "Null":
            clothing_list = images_dict[img_idx].pop("clothing")
            images_dict[img_idx]["upper_wear"] = []
            images_dict[img_idx]["lower_wear"] = []
            for i in clothing_list:
                # upper_wear
                if i in upper_wear_stander_dict.keys():
                    images_dict[img_idx]["upper_wear"].append(upper_wear_stander_dict[i])
                # lower_wear
                elif i in lower_wear_stander_dict.keys():
                    images_dict[img_idx]["lower_wear"].append(lower_wear_stander_dict[i])
        # upper_color
        if images_dict[img_idx]["upper_color"] != "Null":
            upper_color_list = images_dict[img_idx]["upper_color"]
            images_dict[img_idx]["upper_color"] = []
            for i in upper_color_list:
                if i in color_stander_dict.keys():
                    images_dict[img_idx]["upper_color"].append(color_stander_dict[i])
        # lower_color
        if images_dict[img_idx]["lower_color"] != "Null":
            lower_color_list = images_dict[img_idx]["lower_color"]
            images_dict[img_idx]["lower_color"] = []
            for i in lower_color_list:
                if i in color_stander_dict.keys():
                    images_dict[img_idx]["lower_color"].append(color_stander_dict[i])
        # bag
        if images_dict[img_idx]["bag"] != "Null":
            images_dict[img_idx]["bag"] = ["有"]
        else:
            images_dict[img_idx]["bag"] = ["无"]
        # headwear
        if images_dict[img_idx]["headwear"] != "Null":
            images_dict[img_idx]["headwear"] = ["有"]
        else:
            images_dict[img_idx]["headwear"] = ["无"]
        # footwear
        if data_set != "market":
            if images_dict[img_idx]["footwear"] != "Null":
                images_dict[img_idx]["footwear"] = ["有"]
            else:
                images_dict[img_idx]["footwear"] = ["无"]
    images_dict = json.dumps(images_dict, ensure_ascii=False)  # ensure_ascii=False不转译汉字
    return images_dict


def save_json(images_json, dataset_name, save_json_path):
    """
    把mat记录的属性保存为文件，方便读取
    :param images_json: json数据
    :param dataset_name: 数据集名字
    :param save_json_path: 结果保存的路径
    :return: None
    """
    # save_mat_path = "/Users/tao/Desktop/test/dataset_mat_json/"
    # 保存数据集mat分析结果
    file_name = dataset_name + "_mat.json"
    save_path = os.path.join(save_json_path, file_name)
    with open(save_path, "w") as f:
        f.write(images_json)
    print("完美完成")


def main():
    pass
    # 数据集全部图片及属性
    # 从json文件读取
    # json_path = "/Users/tao/Desktop/test/dataset_json/" + dataset_name + "_mat.json"
    # with open(json_path, "r") as f:
    #     result_dict = f.read()
    # 从原mat文件读取
    # result_dict = dataset_main(dataset_name, datafile)
    # images_dict = json.loads(result_dict)


if __name__ == '__main__':
    # 数据集名字
    # data_set = "market"
    # 数据集mat文件
    # data_file = "/Users/tao/Desktop/Person-Attribute-Recognition-MarketDuke/dataset/Market-1501/attribute/market_attribute.mat"

    data_set = "duke"
    data_file = "/Users/tao/Desktop/Person-Attribute-Recognition-MarketDuke/dataset/DukeMTMC-reID/attribute/duke_attribute.mat"

    # data_set = "peta"
    # data_file = "/Users/tao/Desktop/pedestrian-attribute-recognition-pytorch/dataset/peta/PETA.mat"

    # data_set = "pa-100k"
    # data_file = "/Users/tao/Desktop/pedestrian-attribute-recognition-pytorch/dataset/pa100k/annotation/annotation.mat"

    # data_set = "rap"
    # data_file = "/Users/tao/Desktop/pedestrian-attribute-recognition-pytorch/dataset/rap2/RAP_annotation/RAP_annotation.mat"

    # 数据集全部图片及属性
    # 从json文件读取
    # json_path = "/Users/tao/Desktop/test/dataset_json_old/" + data_set + "_mat.json"
    # with open(json_path, "r") as f:
    #     result_dict = f.read()
    # 从原mat文件读取
    result_dict = dataset_main(data_set, data_file)

    save_path_old = "/Users/tao/Desktop/test/dataset_json_old/"
    save_json(result_dict, data_set, save_path_old)

    # 属性映射
    result_dict = attribute_map(result_dict)
    print(len(json.loads(result_dict)))

    # 保存数据集分析结果
    save_path = "/Users/tao/Desktop/test/dataset_json/"
    save_json(result_dict, data_set, save_path)
