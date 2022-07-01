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
    upper = ["upblack", "upwhite", "upred", "uppurple", "upyellow", "upgray", "upblue", "upgreen"]
    downer = ["downblack", "downwhite", "downpink", "downpurple", "downyellow", "downgray", "downblue",
              "downgreen", "downbrown"]
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
            wq = len(w[0][0]) - 1
            a = [w[0][0][wq][0][j][0]]
            for q in range(len(w[0][0]) - 1):
                #
                a.append(w[0][0][q][0][j])
            data = {market_attribute[i]: a[i] for i in range(len(market_attribute))}
            out_data = {'clothing': "Null"}
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
            upper_dic = {"upblack": 'black', "upwhite": 'white', "upred": 'red', "uppurple": 'purple',
                         "upyellow": 'yellow', "upgray": 'gray', "upblue": 'blue', "upgreen": 'green'}
            out_data['upper_color'] = "Null"
            for up in upper:
                out_data['upper_color'] = [upper_dic[up]] if data[up] == 2 else ["Null"]
            downer_dic = {"downblack": 'black', "downwhite": 'white', "downpink": 'pink', "downpurple": 'purple',
                          "downyellow": 'yellow', "downgray": 'gray', "downblue": 'blue', "downgreen": 'green',
                          "downbrown": 'brown'}
            out_data['lower_color'] = "Null"
            for down in downer:
                if data[down] == 2:
                    out_data['lower_color'] = [downer_dic[down]]
            out_data['headwear'] = "Null" if data["hat"] == 1 else ['hat']
            ue_bag = ["backpack", "bag", "handbag"]
            out_data['bag'] = "Null"
            for bbag in ue_bag:
                if data[bbag] == 2:
                    out_data['bag'] = [bbag]
            out_data['footwear'] = "Null"
            all_data[str(data['image_index'])] = out_data
    return json.dumps(all_data)
