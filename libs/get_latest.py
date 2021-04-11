"This will download the latest release of those software from github"
import requests
import json

def main(command_string):
    command_split = command_string.split(' ')
    #List of stuff that is pretty useful and common
    argu_list = ['v2rayng', 'shadowsocks-android', 'shadowsocks-win', 'shadowsocks-qt5',
                 'v2ray-core-win32', 'v2ray-core-linux-amd64',  'v2ray-core-linux-arm32']
    if len(command_split) != 2:
        reply_text = 'Use /help {command} to see how to use this!'
    else:
        api_url = ''
        download_url = ''
        require_api = False
        v2core_type = ''
        if command_split[1] not in argu_list:
            reply_text = 'Please give a correct argument\nLike: /update v2rayng'
        else:
            if command_split[1] is argu_list[0]:
                require_api = True
                api_url = 'https://api.github.com/repos/2dust/v2rayNG/releases/latest'
            elif command_split[1] is argu_list[1]:
                require_api = True
                api_url = 'https://api.github.com/repos/shadowsocks/shadowsocks-android/releases/latest'
            elif command_split[1] is argu_list[2]:
                require_api = True
                api_url = 'https://api.github.com/repos/shadowsocks/shadowsocks-windows/releases/latest'
            elif command_split[1] is argu_list[3]:
                #This repo is already begin archive so no need to use github's api, I don't want owe them for that
                require_api = False
                download_url = 'https://github.com/shadowsocks/shadowsocks-qt5/releases/download/v3.0.1/Shadowsocks-Qt5-3.0.1-x86_64.AppImage'
            elif command_split[1] is argu_list[4] or argu_list[5] or argu_list[6]:
                require_api = True
                api_url = 'https://api.github.com/repos/v2fly/v2ray-core/releases/latest'
                if command_split[1] is argu_list[4]:
                    v2core_type = 'v2ray-windows-32'
                elif command_split[1] is argu_list[5]:
                    v2core_type = 'v2ray-linux-64'
                elif command_split[1] is argu_list[6]:
                    v2core_type = ' v2ray-linux-arm32-v7a'
            try:
                if require_api:
                    api_result = requests.get(api_url).json()
                    if v2core_type is '' or None:
                        download_url = api_result['assets'][1]['browser_download_url']
                    elif v2core_type == 'v2ray-linux-64':
                        download_url = api_result['assets'][14]['browser_download_url']
                    elif v2core_type == ' v2ray-linux-arm32-v7a':
                        download_url = api_result['assets'][20]['browser_download_url']
                    elif v2core_type == 'v2ray-windows-32':
                        download_url = api_result['assets'][42]['browser_download_url']
                else:
                    pass
                #Download the files to Downloads
                print(download_url)
                print('Holds up till L56')
                download_target = requests.get(download_url)
                filename = download_url.split('/')[-1]
                file_loca = f'Downloads/{filename}'
                save_file_loca = json.load('libs/info.json')
                print(save_file_loca)
                save_file_loca[command_split[1]] = file_loca
                dumped_text = json.dumps(save_file_loca)
                with open('libs/info.json', 'w') as f:
                    f.write(dumped_text)
                with open(file_loca, 'wb') as f:
                    f.write(download_target.content)
                reply_text = f'Successfully download the latest of {filename}'
            except Exception as feedback:
                print(feedback)
                reply_text = feedback
    return reply_text