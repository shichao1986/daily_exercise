# -*- coding: utf-8 -*-
"""
时间: 2019/8/12 10:25

作者: shichao

更改记录:

重要说明:
"""
# -*- coding: UTF-8 -*-
#
import requests
import logging
import json

USER_RO = [
    {
        'name':'asset',
        'password': 'asset'
    }
]
USER_RW = [
    {
        'name': 'iot',
        'password': 'iot'
    }
]
registry_url = 'registry.iot.cyai.com'

logger = logging.getLogger('registry')

def check_auth( username, password, op):
    for user in USER_RO:
        if user['name'] == username and user['password'] == password:
           return True if op == 'R' else False

    for user in USER_RW:
        if user['name'] == username and user['password'] == password:
           return True
    return False

def fetch_all_images(user, password):
    if not check_auth(user, password, 'R'):
        logger.critical('registry request forbidden!!! {}, {}'.format(user, password))
        return None

    resp = requests.get('https://{}:{}@{}/v2/_catalog'.format(user, password, registry_url), verify=False)
    if resp.status_code != requests.codes.ok:
        logger.error('query registry failed {}'.format(resp.reason))
        return None

    logger.debug('registry response {}'.format(resp.text))
    return resp.json()['repositories']

def fetch_image_tags(user, password, image):
    if not check_auth(user, password, 'R'):
        logger.critical('registry request forbidden!!! {} {}'.format(user, password))
        return None

    resp = requests.get('https://{}:{}@{}/v2/{}/tags/list'.format(user, password, registry_url, image), verify=False)
    if resp.status_code != requests.codes.ok:
        logger.error('query registry failed {}'.format(resp.reason))
        return None

    logger.debug('registry response {}'.format(resp.text))
    return resp.json()['tags']

def delete_image_tag(user, password, image, tag):
    if not check_auth(user, password, 'W'):
        logger.critical('registry request forbidden!!! {} {}'.format(user, password))
        return False

    get_digest_url = 'https://{0}:{1}@{2}/v2/{3}/manifests/{4}'.format(user,
                                                                       password,
                                                                       registry_url,
                                                                       image,
                                                                       tag)
    headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
    digest_resp = requests.get(get_digest_url, headers=headers, verify=False)
    digest = digest_resp.headers.get('Etag', None)
    if not digest:
        logger.error('invalid image {}:{}'.format(image, tag))
        return False

    del_url = 'https://{}:{}@{}/v2/{}/manifests/{}'.format(user,
                                                           password,
                                                           registry_url,
                                                           image,
                                                           json.loads(digest))
    resp = requests.delete(del_url, verify=False)
    if resp.status_code != requests.codes.accepted:
        logger.error('delete registry failed {}'.format(resp.reason))
        return False

    logger.debug('delete registry image success.{}'.format(resp.text))
    return True

def main():
    print(fetch_all_images('asset', 'asset'))
    print(fetch_image_tags('asset', 'asset', 'cy/mcube/agent'))
    # print(fetch_image_tags('asset', 'asset', '32555478-5e4a-11e8-90fb-000c29b36efa/cy/agent_armhf_raspbian'))
    # print(fetch_image_tags('asset', 'asset', 'fccdc588-bdb1-11e9-bc56-08002740a1cd/cy/agent_armhf_agent'))
    # print(fetch_image_tags('asset', 'asset', '917aa14c-e329-11e8-930b-f48e389f5020/bjtest/serapp_demo'))
    # print(fetch_image_tags('asset', 'asset', '917aa14c-e329-11e8-930b-f48e389f5020/bjtest/fpc_bus_armhf_raspbian'))
    print(fetch_image_tags('asset', 'asset', '917aa14c-e329-11e8-930b-f48e389f5020/bjtest/printer_pc'))

    # print(fetch_image_tags('asset', 'asset', 'cy/mcube/agent'))
    #delete_image_tag('iot', 'iot', 'hello', 'v1')

if __name__ == '__main__':
    main()

