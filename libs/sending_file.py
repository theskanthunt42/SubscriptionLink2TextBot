"This will sending the desire file to the user"
"The relationship between this and get_latest.py is like Airbus A350 and its Rolls-Royce Trent XWB(But only have one)"
"So u might see this is very simillar to get_latest.py"

import json

def main(command_string):
    command_split = command_string.split(' ')
    file_loca = ''
    argu_list = ['v2rayng', 'shadowsocks-android', 'shadowsocks-win', 'shadowsocks-qt5',
                 'v2ray-core-win32', 'v2ray-core-linux-amd64',  'v2ray-core-linux-arm32']
    if len(command_split) != 2:
        reply_text = 'Use /help {command} to see how to use this!'
    else:
        file_loca_json = json.loads('libs/info.json')
        if command_split[1] not in argu_list:
            reply_text = 'Please give a correct argument\nLike: /get_softwares v2rayng'
        else:
            try:
                if command_split[1] is argu_list[0]:
                    file_loca = file_loca_json[command_split[1]]
                elif command_split[1] is argu_list[1]:
                    file_loca = file_loca_json[command_split[1]]
                elif command_split[1] is argu_list[2]:
                    file_loca = file_loca_json[command_split[1]]
                elif command_split[1] is argu_list[3]:
                    file_loca = file_loca_json[command_split[1]]
                elif command_split[1] is argu_list[4]:
                    file_loca = 'Downloads/v2ray-windows-32.zip'
                elif command_split[1] is argu_list[5]:
                    file_loca = 'Downloads/v2ray-linux-64.zip'
                elif command_split[1] is argu_list[6]:
                    file_loca = 'Downloads/v2ray-linux-arm32-v7a.zip'
                reply_text = f"Sending {file_loca.split('/')[-1]}"
            except Exception as feedback:
                print(feedback)
                reply_text = feedback
    return reply_text, file_loca