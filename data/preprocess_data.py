from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

app = client.app

location_dict = app.feature_locations.find_one()

def flatten_data(game,data):
    if(game=='league'):
        flattened_champ = {}

        #print 'game is league'

        db = client.league_of_legends

        feature_locations = location_dict[game]
        feature_list = feature_locations['stats']#gotta get this from mongo


        flattened_champ['name'] = data['name']

        feature_dict = {}

        for feature in feature_list:
            working_data = data
            feature_name = feature['feature']
            #print feature['feature']
            location_nest = feature['location'].split('.')

            depth = len(location_nest)
            for i in range(0,depth-1):
                key = location_nest[i]
                #print working_data
                working_data=working_data[key]

            feature_val = working_data[location_nest[depth-1]]

            flattened_champ[feature_name] = feature_val

        flattened_champ['features'] = feature_dict

        return flattened_champ

    elif(game=='overwatch'):
        print 'game is overwatch'

        return {}
    else:
        print 'game not recognized'

        return {}
