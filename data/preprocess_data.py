from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

app = client.app

location_dict = app.feature_locations.find_one()

def flatten_data(game,data):
    if(game=='league'):
        flattened_champ = {}

        #print 'game is league'

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

            feature_dict[feature_name] = feature_val

        flattened_champ['features'] = feature_dict

        return flattened_champ

    elif(game=='overwatch'):
        print 'game is overwatch'
        print data['name']

        flattened_hero = {}

        flattened_hero['name'] = data['name']
        flattened_hero['shield'] = data['shield']
        flattened_hero['armour'] = data['armour']
        flattened_hero['health'] = data['health']
        flattened_hero['difficulty'] = data['difficulty']
        abilities = data['abilities']
        #print abilities
        attack_features = ['projectile','damage','rate_of_fire','ammo_usage','reload','headshot','dps','heal','buff']
        for feature in attack_features:
            flattened_hero['primary_'+feature] = ''
            flattened_hero['secondary_'+feature]=''

        num = 0
        ability_features = ['mobility','control','damage','heal','buff_offense','buff_defense','cooldown']

        for ability in abilities:
            if ability['is_ultimate']:
                total_string = 'ultimate_ability'
            else:

                total_string = 'basic_ability_'+str(num)

            if(num):
                flattened_hero[total_string+'_name'] = ability['name']
                for feature in ability_features:
                    flattened_hero[total_string+'_'+feature] = ''

            num+=1

        return flattened_hero
    else:
        print 'game not recognized'

        return {}
