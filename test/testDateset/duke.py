import json
import scipy.io as scio


def duke_open_mat(datafile):
    mat = scio.loadmat(datafile)
    att = mat['duke_attribute']
    all_data = {}

    upper = ["upblack", "upwhite", "upred", "uppurple", "upgray", "upblue", "upgreen", "upbrown"]
    downer = ["downblack", "downwhite", "downred", "downgray", "downblue", "downgreen", "downbrown"]
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
            wq = len(w[0][0]) - 1
            a = [w[0][0][wq][0][j][0]]
            for q in range(len(w[0][0])):
                a.append(w[0][0][q][0][j])
            data = {duke_attribute[i]: a[i] for i in range(len(duke_attribute))}
            out_data = {
                'clothing': ['short upper body clothing']
                if data['top'] == 1
                else ['long upper body clothing']
            }

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
            out_data['headwear'] = "Null" if data["hat"] == 1 else ['hat']
            ue_bag = ["backpack", "bag", "handbag"]
            out_data['bag'] = "Null"
            for bbag in ue_bag:
                if data[bbag] == 2:
                    out_data['bag'] = [bbag]
            out_data['footwear'] = "Null" if data['boots'] == 1 else ['boots']
            all_data[str(data['image_index'])] = out_data
    return json.dumps(all_data)
