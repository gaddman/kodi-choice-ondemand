# -*- coding: utf-8 -*-
# Module: default
# Author: gaddman
# Created on: 2020-11-24
# License: GPL v.2 https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html
# API information at https://apidocs.shift72.com/services/meta/

import ast
import datetime
import json
import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

videos = []

authtoken = ""

BASE_CATEGORIES = {
    'Genres': {
        "action": "categories"
    },
    # 'Search': {
    #     "action": "search"
    # },
    'Login': {
        "action": "login"
    }
}
GENRES = {
    '- Promoted': {
        "action": "listing",
        "page_id": "133",
        "is_collection": True
    },
    '- New': {
        "action": "listing",
        "page_id": "207",
        "is_collection": True
    },
    '- Popular': {
        "action": "listing",
        "page_id": "206",
        "is_collection": True
    },
    'Movies and Entertainment': {
        "action": "listing",
        "page_id": "782",
        "is_collection": True
    },
    'Food and Cooking': {
        "action": "listing",
        "page_id": "169",
        "is_collection": False
    },
    'Great Outdoors': {
        "action": "listing",
        "page_id": "166",
        "is_collection": False
    },
    'Greener Living': {
        "action": "listing",
        "page_id": "241",
        "is_collection": False
    },
    'Home and Garden': {
        "action": "listing",
        "page_id": "167",
        "is_collection": False
    },
    'Love Nature': {
        "action": "listing",
        "page_id": "168",
        "is_collection": False
    },
    'Property and Design': {
        "action": "listing",
        "page_id": "163",
        "is_collection": False
    },
    'Traders and Collectors': {
        "action": "listing",
        "page_id": "165",
        "is_collection": False
    },
    'Kids': {
        "action": "listing",
        "page_id": "781",
        "is_collection": True
    },
    'Travel and History': {
        "action": "listing",
        "page_id": "164",
        "is_collection": False
    }
}


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: list
    """
    return GENRES.keys()


def get_items():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: list
    """
    return BASE_CATEGORIES.keys()


def set_username_password(username, password):
    url = "https://www.choicetv.co.nz/services/users/auth/sign_in"

    payload = "{\"user\":{\"email\":\"" + username + "\",\"password\":\"" + password + "\",\"remember_me\":true}}"
    headers = {
        'content-type': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if (response.status_code != 200):
        xbmcgui.Dialog().notification("Incorrect Email or Password",
                                      "The email or password you supplied was incorrect", xbmcgui.NOTIFICATION_ERROR)
        xbmc.log("Choice TV Login Debug. Code: " + str(response.status_code) + " Full Response: " + response.text)
    else:
        xbmcgui.Dialog().notification("Login Successful",
                                      "You have successfully logged in", xbmcgui.NOTIFICATION_INFO)
        addon = xbmcaddon.Addon()
        addon.setSetting(id='username', value=str(username))
        addon.setSetting(id='password', value=str(password))
        addon.setSetting(id='auth_token', value=json.loads(response.text)["auth_token"])


def get_videos_dict():
    return videos


def get_login():
    kb = xbmc.Keyboard("", "Enter Email Address", False)
    kb.doModal()
    if (kb.isConfirmed()):
        username = kb.getText()
        kb = xbmc.Keyboard("", "Enter Password", True)
        kb.doModal()
        if (kb.isConfirmed()):
            password = kb.getText()
            set_username_password(username, password)
        else:
            list_items()
    else:
        list_items()


def generate_token():
    addon = xbmcaddon.Addon()

    url = "https://www.choicetv.co.nz/services/users/auth/sign_in"

    payload = "{\"user\":{\"email\":\"" + addon.getSetting('username') + "\",\"password\":\"" + addon.getSetting(
        'password') + "\",\"remember_me\":true}}"
    headers = {
        'content-type': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if (response.status_code != 200):
        xbmcgui.Dialog().notification("A email or password change was detected",
                                      "Please login again with the new credentials", xbmcgui.NOTIFICATION_ERROR)
    else:
        addon.setSetting(id='auth_token', value=json.loads(response.text)["auth_token"])


"""
Search Needs MAJOR reworking, I'm going to remove it for now.
"""


# def get_search():
#     kb = xbmc.Keyboard("", "Enter Search Term", False)
#     kb.doModal()
#     if (kb.isConfirmed()):
#         url = "https://www.choicetv.co.nz/services/meta/v1/search/"
#         querystring = {"page": "1", "query": kb.getText()}
#         response = requests.request("GET", url, params=querystring)
#
#         items = json.loads(response.text)
#
#         films = []
#         tvshows = []
#         for item in items:
#             it = str(item)
#             if it.startswith("/film"):
#                 films.append(item)
#             else:
#                 tvshows.append(item)
#
#         tvShowsUrl = "https://www.choicetv.co.nz/services/meta/v2/tv/season/show_multiple?items="
#         for tvshow in tvshows:
#             tvShowsUrl = tvShowsUrl + tvshow
#             if tvshows.index(tvshow) != len(tvshows) - 1:
#                 tvShowsUrl = tvShowsUrl + ","
#
#         filmsUrl = "https://www.choicetv.co.nz/services/meta/v2/film/"
#         for film in films:
#             haveComma = (films.index(film) != len(films) - 1)
#             film = film.replace("/film/", "")
#             filmsUrl = filmsUrl + film
#             if (haveComma):
#                 filmsUrl = filmsUrl + ","
#
#         global videos
#
#         filmsUrl = filmsUrl + "/show_multiple"
#
#         if len(tvshows) != 0:
#             tvShowsRequest = requests.get(tvShowsUrl)
#             j = json.loads(tvShowsRequest.text)
#             tvepisodes = j["seasons"]
#
#             for tvepisode in tvepisodes:
#                 episode = {
#                     "type": "tvshow",
#                     "tagline": tvepisode["tagline"],
#                     "overview": tvepisode["overview"],
#                     "genres": tvepisode["show_info"]["genres"],
#                     "title": tvepisode["show_info"]["title"],
#                     "portrait": tvepisode["image_urls"]["landscape"],
#                     "background": tvepisode["image_urls"]["carousel"],
#                     "episodes": tvepisode["episodes"],
#                     "premiered": tvepisode['show_info']["release_date"].split("T")[0],
#                     "slug": tvepisode["slug"]
#                 }
#                 videos.append(episode)
#         if len(films) != 0:
#             filmsRequest = requests.get(filmsUrl)
#             films = json.loads(filmsRequest.text)
#
#             for film in films:
#                 episode = {
#                     "type": "movie",
#                     "title": film["title"],
#                     "tagline": film["tagline"],
#                     "overview": film["overview"],
#                     "genres": film["genres"],
#                     "portrait": film["image_urls"]["landscape"],
#                     "background": film["image_urls"]["carousel"],
#                     "premiered": film["release_date"].split("T")[0],
#                     "id": film["id"]
#                 }
#                 videos.append(episode)
#
#                 # Set plugin category. It is displayed in some skins as the name
#             # of the current section.
#             xbmcplugin.setPluginCategory(_handle, "Search Results")
#             # Set plugin content. It allows Kodi to select appropriate views
#             # for this type of content.
#             xbmcplugin.setContent(_handle, 'tvshows')
#
#
#             # Iterate through videos.
#             for video in videos:
#                 # Create a list item with a text label and a thumbnail image.
#                 list_item = xbmcgui.ListItem(label=video['title'])
#
#                 # Set additional info for the list item.
#                 list_item.setInfo('video',
#                                   {'title': video['title'], 'genre': video['genres'][0], 'tagline': video['tagline'],
#                                    'plot': video['overview'], "premiered": video["premiered"]})
#                 # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
#                 # Here we use the same image for all items for simplicity's sake.
#                 # In a real-life plugin you need to set each image accordingly.
#                 list_item.setArt({'thumb': video['portrait'], 'icon': video['portrait'], 'fanart': video['background']})
#                 # Set 'IsPlayable' property to 'true'.
#                 # This is mandatory for playable items!
#                 list_item.setProperty('IsPlayable', 'true')
#                 # Create a URL for a plugin recursive call.
#                 if video['type'] == "movie":
#                     url = get_url(action='play', slug="/film/" + str(video['id']))
#                 else:
#                     list_item.setProperty("TotalEpisodes", str(len(video['episodes'])))
#                     url = get_url(action='episodes', index=number, category=category)
#                 # Add the list item to a virtual Kodi folder.
#                 # is_folder = False means that this item won't open any sub-list.
#                 is_folder = False
#                 # Add our item to the Kodi virtual folder listing.
#                 xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
#             # Add a sort method for the virtual folder items (alphabetically, ignore articles)
#             xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
#             # Finish creating a virtual folder.
#             xbmc.executebuiltin('Container.SetViewMode(512)')
#
#             xbmcplugin.endOfDirectory(_handle)
#     else:
#         list_items()


def get_videos(category):
    """
    Gets the videos for a specific category
    """
    genre = GENRES[category]

    global videos

    if genre["is_collection"]:
        url = "https://www.choicetv.co.nz/services/meta/v4/featured/" + genre["page_id"]
        r = requests.get(url)
        data = r.json()
        items = data["items"]
    else:
        url = "https://www.choicetv.co.nz/services/meta/v1/pages/" + genre["page_id"] + "/detail"
        r = requests.get(url)
        data = r.json()
        items = data["page_features"][0]["items"]

    films = []
    tvshows = []
    for item in items:
        it = str(item)
        if it.startswith("/film"):
            films.append(item)
        else:
            tvshows.append(item)

    tvShowsUrl = "https://www.choicetv.co.nz/services/meta/v2/tv/season/show_multiple?items="
    for tvshow in tvshows:
        tvShowsUrl = tvShowsUrl + tvshow
        if tvshows.index(tvshow) != len(tvshows) - 1:
            tvShowsUrl = tvShowsUrl + ","

    filmsUrl = "https://www.choicetv.co.nz/services/meta/v2/film/"
    for film in films:
        haveComma = (films.index(film) != len(films) - 1)
        film = film.replace("/film/", "")
        filmsUrl = filmsUrl + film
        if (haveComma):
            filmsUrl = filmsUrl + ","

    filmsUrl = filmsUrl + "/show_multiple"

    if len(tvshows) != 0:
        tvShowsRequest = requests.get(tvShowsUrl)
        j = json.loads(tvShowsRequest.text)
        tvepisodes = j["seasons"]

        for tvepisode in tvepisodes:
            if "release_date" in tvepisode['show_info']:
                premiered = tvepisode['show_info']["release_date"]
                if premiered != "":
                    premiered = premiered.split("T")[0]
            else:
                premiered = ""
            episode = {
                "type": "tvshow",
                "tagline": tvepisode.get("tagline"),
                "overview": tvepisode.get("overview"),
                "genres": tvepisode["show_info"].get("genres"),
                "title": tvepisode["show_info"].get("title"),
                "portrait": tvepisode["image_urls"].get("landscape"),
                "background": tvepisode["image_urls"].get("carousel"),
                "episodes": tvepisode["episodes"],
                "slug": tvepisode["slug"],
                "premiered": premiered
            }
            videos.append(episode)
        if len(films) != 0:
            filmsRequest = requests.get(filmsUrl)
            films = json.loads(filmsRequest.text)

            for film in films:

                if "release_date" in film:
                    premiered = film["release_date"]
                    if premiered != "":
                        premiered = premiered.split("T")[0]
                else:
                    premiered = ""
                episode = {
                    "type": "movie",
                    "tagline": film.get("tagline"),
                    "overview": film.get("overview"),
                    "genres": film.get("genres"),
                    "title": film.get("title"),
                    "portrait": film["image_urls"].get("landscape"),
                    "background": film["image_urls"].get("carousel"),
                    "id": film["id"],
                    "premiered": premiered
                }
                videos.append(episode)

    return videos


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, 'My Video Collection')

    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)

        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category, 'genre': category})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    xbmcplugin.setPluginCategory(_handle, category)
    xbmcplugin.setContent(_handle, 'tvshows')
    global videos
    videos = get_videos(category)
    number = 0
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['title'])
        list_item.setInfo('video', {'title': video.get('title'), 'tagline': video.get('tagline'),
                                    'plot': video.get('overview'), "premiered": video.get("premiered")})
        list_item.setArt(
            {'thumb': video.get('portrait'), 'icon': video.get('portrait'), 'fanart': video.get('background')})
        list_item.setProperty('IsPlayable', 'true')
        if video['type'] == "movie":
            url = get_url(action='play', slug="/film/" + str(video['id']))
            is_folder = False
        else:
            list_item.setProperty("TotalEpisodes", str(len(video['episodes'])))
            url = get_url(action='episodes', index=number, category=category)
            is_folder = True

        number = number + 1

        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def list_episodes(index, category):
    index = int(index)
    videos = get_videos(category)
    xbmc.log(str(videos), xbmc.LOGINFO)
    video = videos[index]
    xbmcplugin.setPluginCategory(_handle, video['title'])
    xbmcplugin.setContent(_handle, 'episodes')

    availabilities = json.loads(
        requests.get("https://www.choicetv.co.nz/services/content/v1/availabilities?items=" + video['slug']).text)
    is_avaliable = {}
    for avaliable in availabilities:
        can_use = True
        if avaliable['ms_from'] is None or avaliable['ms_from'] != 0:
            can_use = False
        if avaliable['ms_to'] is None or avaliable['ms_to'] == 0:
            can_use = False
        is_avaliable[avaliable['slug']] = can_use

    for episode in video['episodes']:
        if is_avaliable[video['slug'] + "/episode/" + str(episode['episode_number'])]:
            list_item = xbmcgui.ListItem(label=episode['title'])
            list_item.setInfo('video',
                              {'title': episode['title'], 'episode': episode['episode_number'],
                               'plot': episode['overview']})
            list_item.setArt({'thumb': episode['image_urls']['landscape'], 'icon': episode['image_urls']['landscape'],
                              'fanart': episode['image_urls']['landscape']})

            list_item.setProperty('IsPlayable', 'true')

            url = get_url(action='play', slug=video['slug'] + '/episode/' + str(episode['episode_number']))

            is_folder = False

            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.endOfDirectory(_handle)


def play_video(slug):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    addon = xbmcaddon.Addon()
    authtoken = addon.getSetting("auth_token")
    if authtoken != "":
        url = "https://www.choicetv.co.nz/services/content/v4/media_content/play" + slug

        querystring = {"encoding_type": "mp4", "drm": "none"}

        headers = {
            'x-auth-token': authtoken,
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code != 200:
            generate_token()
            url = "https://www.choicetv.co.nz/services/content/v4/media_content/play" + slug

            querystring = {"encoding_type": "mp4", "drm": "none"}

            headers = {
                'x-auth-token': authtoken,
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            url = json.loads(response.text)['streams'][0]['url']
            # Create a playable item with a path to play.
            play_item = xbmcgui.ListItem(path=url)
            # Pass the item to the Kodi player.
            xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

        else:
            streams = json.loads(response.text)['streams']
            if len(streams) == 0:
                xbmcgui.Dialog().ok(xbmcaddon.Addon().getAddonInfo('name'),
                                    "Error: This file is DRM protected. DRM playback is not currently supported.")
            else:
                url = streams[0]['url']
                # Create a playable item with a path to play.
                play_item = xbmcgui.ListItem(path=url)
                # Pass the item to the Kodi player.
                xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


    else:
        get_login()


def list_items():
    xbmcplugin.setPluginCategory(_handle, 'ChoiceTV OnDemand')
    xbmcplugin.setContent(_handle, 'videos')
    # Get video categories
    items = get_items()
    # Iterate through categories
    for item in items:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=item)

        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': item, 'genre': item})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action=BASE_CATEGORIES[item]["action"])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['slug'])
        elif params['action'] == "categories":
            list_categories()
        elif params['action'] == "login":
            get_login()
        # elif params['action'] == "search":
        #     get_search()
        elif params['action'] == 'episodes':
            list_episodes(params['index'], params['category'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of items
        list_items()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
