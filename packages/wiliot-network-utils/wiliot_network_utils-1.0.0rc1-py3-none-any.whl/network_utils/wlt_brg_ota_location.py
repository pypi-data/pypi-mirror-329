# before running, pip install these packages:
# > pip install wiliot-deployment-tools binascii

from wiliot_deployment_tools.api.extended_api import ExtendedEdgeClient, ExtendedPlatformClient, EdgeClient, BridgeThroughGatewayAction, GatewayType
import binascii
import json
import time
import random
import argparse
from datetime import datetime
from colorama import init

# Initialize colorama (necessary for Windows)
init(autoreset=True)

# ANSI escape codes for colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

api_key = ''
owner_id = ''
gw_id = '' 
cloud = ''  # 'gcp' or 'aws'  ('us-central1' if cloud=='gcp' else 'us-east-2')  'us-east-2' 
env =  ''  # 'prod' or 'test'
region = ''
desired_app_version = '' 
retries = 50
shuffle_src_brgs = True
api_ver  = '0A'
rssi_threshold = -60
src_brg_id_list =[]
dst_brg_id_list =[]
gw_type = ""
latest_bl = 18
minimal_bl = 12



 #Get Token using API Key
e = []
ec = []



def cur_time():
    current_time = datetime.now()
    
    # Extract only the time components (hours, minutes, seconds)
    time_components = current_time.strftime('%H:%M:%S')
    return time_components


def time_diff_sec(prev_time):
    current_epoch_time = int(time.time())
    return int(current_epoch_time - prev_time/1000)

def is_brg_relevat_as_brg2brg_src_brg(e, brg_id, gw_id):
    is_relevat = False
    brg_dict = e.get_bridge(brg_id)
    brg_id = brg_dict['id']   
            
    for conn in brg_dict['connections']:
        if  'rssi' in conn and conn['rssi'] > -68 and conn['gatewayId'] == gw_id :
            is_relevat = True 
    
    return is_relevat 




def get_brg_modules(e, brg_id, gw_id):
    sq_id =  random.randint(10, 99) 
    packet = (f'1E16C6FC0000ED0709{sq_id}{brg_id}03FE00000000000000000000000000')
    e.send_packet_through_gw(gateway_id=gw_id, raw_packet=packet, is_ota=False, repetitions='3')

def is_brg_ota_secceeded(e, brg_id, desired_app_version, desired_brg_zone):
    upgrade_succeedded = 0   
    brg_test = e.get_bridge(brg_id)
    brg_zone = None
    brg_zone_name = None
    if 'zone' in brg_test:          
        brg_zone = brg_test['zone'] 
        brg_zone_name = brg_zone['name']

    if(brg_test['version'] == desired_app_version):
       upgrade_succeedded = 1
       if(brg_test['bootloaderVersion'] == latest_bl and brg_id not in src_brg_id_list and is_brg_relevat_as_brg2brg_src_brg(e, brg_id, gw_id)):
          src_brg_id_list.append(brg_id)
          upgrade_succeedded = 2
       
    return upgrade_succeedded



def check_brg2brg_ota(e, gw_id, desired_app_version, update_bl, gw_type,desired_brg_zone, brg2brg_only):

    wait_time = 0    
    if GatewayType.WIFI == gw_type or GatewayType.FANSTEL_LAN_V0 == gw_type or brg2brg_only :
        wait_time = 220 if update_bl else 120
    elif  GatewayType.RIGADO == gw_type :
        wait_time = 180 if update_bl else 100    
    else:
        wait_time = 550 if update_bl else 340

    print(BLUE +"[{}] Waiting {} seconds for the OTA upgrade to complete".format(cur_time(), wait_time))
    time.sleep(wait_time) 

   # for dst_brg_id in dst_brg_id_list: 
   #     time.sleep(1) 
   #     get_brg_modules(e, dst_brg_id, gw_id)     
   
    ctr = 0
    time.sleep(1)
    for dst_brg_id in dst_brg_id_list:  
        rc = is_brg_ota_secceeded(e, dst_brg_id, desired_app_version, desired_brg_zone)                               
        if rc ==1 :
            print(GREEN +"[{}] Bridge Id {} - Upgrade succeedded (App only) " .format(cur_time(), dst_brg_id))
            dst_brg_id_list.remove(dst_brg_id)
        elif rc ==2 :   
            print(GREEN +"[{}] Bridge Id {} - Upgrade succeedded (App + Bootloader) " .format(cur_time(), dst_brg_id))
            dst_brg_id_list.remove(dst_brg_id)
        else:
            print(RED +"[{}] Bridge Id {} - Upgrade either failed or didn't start yet".format(cur_time(), dst_brg_id))
        ctr = ctr + 1
        if ctr >= len(src_brg_id_list):
            break   
            

def brg2brg_ota(e,ec, gw_id):
    rc = 0
    random.shuffle(src_brg_id_list)
    random.shuffle(dst_brg_id_list)
    for src_brg_id, dst_brg_id in zip(src_brg_id_list, dst_brg_id_list):
        best_gw_id = gw_id
        best_gw_rssi = -90
        best_gw_rssi_time = 0
        brg_dict = ec.get_bridge(src_brg_id)  
        for conn in brg_dict['connections']:               
                #if 'rssi' in conn and e.check_gw_online([conn['gatewayId']]):
                if 'rssi' in conn:
                    #print(CYAN +"\n[{}] brg_id={} gw_id={} , RSSI={}".format(cur_time(),src_brg_id, conn['gatewayId'], , conn['rssi']))
                    if conn['rssi'] > best_gw_rssi and conn['rssi'] < 0 and  time_diff_sec(conn['rssiUpdatedAt'])<1800: 
                        best_gw_id = conn['gatewayId']
                        best_gw_rssi = conn['rssi']
                        best_gw_rssi_time = conn['rssiUpdatedAt']
        if best_gw_rssi_time == 0 or best_gw_rssi < -68:
            continue

        print(YELLOW +"\n[{}] GW {} received data from Brg {} with RSSI {} (Measured {} seconds ago)".format(cur_time(), gw_id, src_brg_id, best_gw_rssi, time_diff_sec(best_gw_rssi_time)))
        sq_id =  random.randint(10, 99)
        reboot_packet = f'1E16AFFD0000ED0300{sq_id}{dst_brg_id}010000000000000000000000000000'
        packet = (f'1E16AFFD0000ED08{api_ver}{sq_id+1}{src_brg_id}02{dst_brg_id}0000000000000000')            
        e.send_packet_through_gw(gateway_id=gw_id, raw_packet=reboot_packet, is_ota=False, tx_max_duration=300, repetitions=5) 
        print(MAGENTA +"[{}] Starting OTA Bridge {} to Bridge {}".format(cur_time(), src_brg_id, dst_brg_id))   
        e.send_packet_through_gw(gateway_id=best_gw_id, raw_packet=packet, is_ota=False, tx_max_duration = 300, repetitions=5)
        rc = 1
    return rc    

def sync_brg_lists(ec,gw_id, desired_app_version, desired_brg_zone, all_brgs, brg_type):
    return
    if not all_brgs:
        connected_all_brgs = ec.get_bridges_connected_to_gateway(gw_id) 
        all_brgs = connected_all_brgs['connections'] 
    
    for brg_dict in all_brgs:
        brg_id = brg_dict['id']
        brg_bl = brg_dict['bootloaderVersion'] 
        brg_app_version = brg_dict['version'] 
        boardType = brg_dict['boardType']

        if brg_type != boardType: 
            print(YELLOW + "[{}] Bridge {} of type {} differs from required type {} - Not upgrading it".format(cur_time(), brg_id, boardType, brg_type )) 
            continue

        if 'zone' in brg_dict:          
            brg_zone = brg_dict['zone'] 
            brg_zone_name = brg_zone['name']
            
        if(brg_app_version == desired_app_version):
            if(brg_id in dst_brg_id_list):
                dst_brg_id_list.remove(brg_id) 
            if(brg_bl == latest_bl and brg_id not in src_brg_id_list and ((desired_brg_zone == None ) or (desired_brg_zone != None and desired_brg_zone in brg_zone_name)) ):
                src_brg_id_list.append(brg_id) 

def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    
    parser.add_argument('--owner_id', '-oi', required=True, type=str, help='Owner Id')
    parser.add_argument('--api_key', '-ak', required=True, type=str, help='API Key')
    parser.add_argument('--gateway', '-gw', required=False, default=None,type=str, help='Gw to use for OTA')
    parser.add_argument('--cloud', '-cl', required=False, default='aws', choices=['aws', 'gcp'], type=str, help='Cloud Enviorment')
    parser.add_argument('--enviorment', '-env', required=False, default='prod', choices=['prod', 'test', 'dev'], type=str, help='Production/Test Enviorment')
    parser.add_argument('--brg_id', '-bi', required=True, type=str, help='Bridge Id') 
    parser.add_argument('--brg_ver', '-bv', required=True, type=str, help='Bridge Version')
    parser.add_argument('--rssi_threshold', '-rt', required=False, default=-60, type=int, help='rssi threshold')
    parser.add_argument('--app_only', '-ao', required=False, default=False , type=bool, help='Application Only(no Bootloader upgrade)')
    parser.add_argument('--brg_type','-bt', required=True, default=None, type=str, help='Bridge Type: FanstelSingleBandV0 ,ErmV0, etc... ')
    
    args = parser.parse_args()
    print(args.__dict__)
    
    owner_id = args.owner_id
    api_key = args.api_key
    gw_id = None
    all_brgs = []
    cloud = args.cloud
    env = args.enviorment
    first_brg_id = args.brg_id
    desired_app_version = args.brg_ver
    global desired_brg_location
    global desired_brg_zone
    global src_brg_id_list
    rssi_threshold = args.rssi_threshold
    app_only = args.app_only
    global shuffle_src_brgs
    global src_brg_id_list
    global brg_location_name
    shuffle_src_brgs = True
    src_brg_id_list = [] 
    desired_brg_zone = None
    brg_location_name = None
    desired_brg_location = None
    location_id = None
    brg_type = args.brg_type
    
     
    region = 'us-central1' if cloud == 'gcp' else 'us-east-2'

     #Get Token using API Key
    e = ExtendedEdgeClient(api_key, owner_id, env ,region, cloud)   
    ec = EdgeClient(api_key, owner_id, env ,region, cloud)   
    #ep = ExtendedPlatformClient(api_key, owner_id, env ,region, cloud)  
    
    for number in range(retries):
              
        best_gw_rssi = -90 
        best_gw_rssi_time = 0 

        first_brg_dict = ec.get_bridge(first_brg_id)        
        
        if 'location' in first_brg_dict: 
            location = first_brg_dict['location']          
            location_id = location['id'] 
            desired_brg_location = location['name']
        else:
           print(RED +"\n[{}] Bridge {} has no location id - aborting ...".format(cur_time(),first_brg_id))  
           exit
        print(BLUE +"\n[{}] Location {} has location id {}".format(cur_time(), desired_brg_location, location_id))  
        
        if 'zone' in first_brg_dict: 
            zone_dict = first_brg_dict['zone']          
            desired_brg_zone = zone_dict['name']
            print(BLUE +"\n[{}] zone {} ".format(cur_time(), desired_brg_zone))         
        
        #all_brgs_in_location = ec.get_bridges( online=True, params={'locationId': location_id, 'search_query':'4.2.117' })
        all_brgs_in_location = ec.get_bridges( online=True, params={'locationId': location_id})
        print(BLUE +"\n[{}] There are {} bridges at location {}".format(cur_time(), len(all_brgs_in_location), desired_brg_location))             
        for brg_dict in all_brgs_in_location:                    
            brg_id = brg_dict['id']   
            
            for conn in brg_dict['connections']:               
                #if 'rssi' in conn and e.check_gw_online([conn['gatewayId']]):
                if 'rssi' in conn and conn['rssi'] < 0:
                    print(CYAN +"\n[{}] GW {} received data from Brg {} with RSSI {} (Measured {} seconds ago)".format(cur_time(), conn['gatewayId'], brg_id, conn['rssi'], time_diff_sec(conn['rssiUpdatedAt'])))
                    if conn['rssi'] > best_gw_rssi and  conn['rssi'] < 0 and time_diff_sec(conn['rssiUpdatedAt'])<1800:                    
                        gw_id = conn['gatewayId']
                        best_gw_rssi = conn['rssi']
                        best_gw_rssi_time = conn['rssiUpdatedAt'] 
        if gw_id == None:
           print(RED +"\n[{} No GW was available for upgrading bridges at location {}".format(cur_time(),  desired_brg_location)) 
           return 
        else:
            print(YELLOW +"\n[{}] brg_id={} gw_id={} best_gw_rssi={} messured {} seconds ago".format(cur_time(),brg_id, gw_id, best_gw_rssi, time_diff_sec(best_gw_rssi_time)))     

        gw_type = e.get_gateway_type(gw_id)
        print(BLUE +"\n[{}] GW {} ({}) with RSSI {} will be used to upgrade bridges at location {}".format(cur_time(), gw_id,gw_type, best_gw_rssi, desired_brg_location))             
       
        #sync_brg_lists(e, desired_app_version, desired_brg_zone, all_brgs, brg_type)       
        all_brgs = ec.get_bridges_connected_to_gateway(gw_id) 
        #print (all_brgs)
        
        #all_brgs = connected_all_brgs['connections']            

        
        print(BLUE +"\n[{}] There are {} bridges connected to GW {} , {}, BL: Desired {} ,Ver: Desired {}".format(cur_time(), len(all_brgs), gw_id,gw_type, latest_bl, desired_app_version))
        
        #for brg_id in brg_id_list:
        for brg_dict_on_gw in all_brgs: 
            sq_id =  random.randint(10, 99) 
            brg_dict = ec.get_bridge(brg_dict_on_gw['id'])
            if brg_dict['owned'] != True:
                continue

            
            brg_id = brg_dict['id']
            boardType = brg_dict['boardType'] 
            brg_bl = brg_dict['bootloaderVersion'] 
            brg_app_version = brg_dict['version']
            if 'location' in brg_dict:
                location_dict = brg_dict['location']          
                brg_location = location_dict['name']
            else:
                brg_location = None  
            
            if 'zone' in brg_dict:
                zone_dic = brg_dict['zone'] 
                brg_zone = zone_dic['name']
            else:
                brg_zone = None 

            brg_zone = None 
            brg_rssi = -90
            brg_rssi_time = 0
            update_bl = True if (brg_bl < latest_bl) else False


            if brg_type != boardType: 
                print(YELLOW + "[{}] Bridge {} of type {} differs from required type {} - Not upgrading it".format(cur_time(), brg_id, boardType, brg_type )) 
                continue
            if brg_location != desired_brg_location: 
                print(YELLOW + "[{}] Bridge {} location {} differs from required location {} - Not upgrading it".format(cur_time(), brg_id, brg_location, desired_brg_location )) 
                continue
            if brg_zone != None and  brg_zone != desired_brg_zone: 
                print(YELLOW + "[{}] Bridge {} zone {} differs from required zone {} - Not upgrading it".format(cur_time(), brg_id, brg_zone, desired_brg_zone )) 
                continue

            for conn in brg_dict['connections']:
                if conn['gatewayId'] == gw_id  and 'rssi' in conn and conn['rssi'] < 0 :
                    brg_rssi = conn['rssi']
                    brg_rssi_time = conn['rssiUpdatedAt']
                    break

            if brg_dict['claimed'] == False: 
                print(YELLOW + "[{}] Bridge {} is not claimed by account {} ({},{}) - Not upgrading it".format(cur_time(), brg_id, owner_id, cloud, env)) 
                continue 
            
            if 'location' in brg_dict:          
                    brg_location = brg_dict['location'] 
                    brg_location_name = brg_location['name']

            #if time_diff_sec(brg_rssi_time) > 900:
            #   continue      

            #if(brg_bl == latest_bl and brg_app_version == desired_app_version) and brg_rssi < -68:  
            #    continue  
            
            print(("[{}] Brg Id {}, {}, BL version: {} ,App version: {} ,Rssi: {}" .format(cur_time(), brg_id, boardType, brg_bl, brg_app_version, brg_rssi)) ,end="")
            if(brg_bl == latest_bl and brg_app_version == desired_app_version):
                if(brg_id not in src_brg_id_list and (brg_location_name == desired_brg_location)):
                    if shuffle_src_brgs:
                        src_brg_id_list = []
                        shuffle_src_brgs = False 
                    src_brg_id_list.append(brg_id) if brg_id not in src_brg_id_list else None                 
                else:
                    if shuffle_src_brgs and brg_rssi > -60: 
                        src_brg_id_list.append(brg_id) if brg_id not in src_brg_id_list else None 
                print(YELLOW + " - No need to upgrade" )
                continue
            elif(boardType == 'Wiliot-Virtual-MEL' or boardType == 'wifi' ):
                print(YELLOW + " - No need to handle Wiliot-Virtual-MEL")
                continue
            #elif(brg_bl == latest_bl and brg_app_version != desired_app_version and brg_id not in dst_brg_id_list and (len(src_brg_id_list)>0)):
            #    dst_brg_id_list.append(brg_id) 
            #    print(CYAN + " - Adding bridge to Brg2Brg OTA list")
            #    continue
            elif(brg_app_version == desired_app_version and app_only):
                print(CYAN + " - Bridge is already with the latest version (app only flag is set so bootloader is not upgraded)")
                continue
            elif(brg_rssi < rssi_threshold and brg_app_version != desired_app_version): 
                if(brg_id not in dst_brg_id_list):
                    dst_brg_id_list.append(brg_id) if brg_id not in dst_brg_id_list else None         
                print(CYAN + " - Rssi {} dBm is too weak for Gw2Brg OTA (Rssi threshold is {} dBm) - adding bridge to Brg2Brg OTA list" .format(brg_rssi, rssi_threshold)  )
                continue
            elif(brg_app_version == desired_app_version and brg_rssi < 0.0 and brg_rssi < rssi_threshold):
                print(YELLOW + " - No need to upgrade  - Bootloader {} is older than the latest bl but the app version is already updated".format(brg_bl))
                continue
            elif(GatewayType.ERM == gw_type and len(src_brg_id_list)>=len(all_brgs)/4 and brg_app_version != desired_app_version and brg_id not in dst_brg_id_list):
                dst_brg_id_list.append(brg_id) if brg_id not in dst_brg_id_list else None 
                print(CYAN + " - {} Bridges can upgrade this bridge - adding bridge to Brg2Brg OTA list".format(len(src_brg_id_list))  )
                continue    
            else:
                print(MAGENTA +" - About to upgrade (Gw2Brg OTA)")
                
            imageDirUrl = (f'https://api.{region}.{env}.wiliot.cloud/v1/bridge/type/{boardType}/version/{desired_app_version}/binary/') if cloud !='gcp' else  (f'https://api.{region}.{env}.gcp.wiliot.cloud/v1/bridge/type/{brg_type}/version/{desired_app_version}/binary/')    
            
            payload = {
                "action": 1, # Upgrade bridge
                "gatewayId": gw_id, # optional. for the c2c data flows    
                # // Advertise parameters:
                "imageDirUrl":imageDirUrl,
                "upgradeBlSd": update_bl,
                "txPacket": ( f'1E16AFFD0000ED0300{sq_id}{brg_id}010000000000000000000000000000'),
                "txMaxDurationMs": 750,
                "txMaxRetries" : 8,
                "bridgeId": brg_id
            }

            if(brg_id in dst_brg_id_list):
                dst_brg_id_list.remove(brg_id)           
            
            brg2brg_ota(e,ec, gw_id)
            e.send_custom_message_to_gateway(gateway_id=gw_id, custom_message=payload) 
                
            if(brg_id not in dst_brg_id_list):
                dst_brg_id_list.insert(0,brg_id)
                       
            check_brg2brg_ota(e, gw_id, desired_app_version, update_bl, gw_type , desired_brg_zone, brg2brg_only = False)

            sync_brg_lists(ec,gw_id, desired_app_version,desired_brg_zone,[], brg_type)
                
        #Bridge to Bridge OTA
        retry_ctr = 0        
        while(len(src_brg_id_list) and len(dst_brg_id_list) and retry_ctr < (len(src_brg_id_list))):
            print(BLUE + "\n[{}] About to start Brg2Brg OTA cycle {}:".format(cur_time(), retry_ctr))
            print(YELLOW + "[{}] Src Bridge list ({} Bridges) {}".format(cur_time(),len(src_brg_id_list), src_brg_id_list))
            print(CYAN +   "[{}] Dest Bridge list ({} Bridges) {}".format(cur_time(),len(dst_brg_id_list), dst_brg_id_list))
            retry_ctr += 1
            rc = 0 
            rc = brg2brg_ota(e,ec, gw_id)  
            if rc:           
                check_brg2brg_ota(e, gw_id, desired_app_version,False, gw_type, desired_brg_zone, brg2brg_only=True)
            #sync_brg_lists(e, desired_app_version,desired_brg_zone, [], brg_type)    
    print("[{}] Bridge Upgrade Process for Bridges Connected to GW {} is completed".format(cur_time(), gw_id))



if __name__ == "__main__":
    main()

