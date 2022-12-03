#!/usr/bin/env python
# coding: utf-8

# In[31]:


from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import numpy as np
from scipy import stats
from IPython.display import display, HTML, Markdown, Javascript
import json


# In[45]:


# Select your transport with a defined url endpoint
deviceID = "<get your device ID from the web developer tools in your browser>"
token = "Bearer","<get your token from the web developer tools in your browser>"
transport = RequestsHTTPTransport(
    url="https://apis.justwatch.com/graphql",
    headers={'content-type': 'application/json','DEVICE-ID': deviceID,"Authorization": token}
)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=False)
# Provide a GraphQL query
query = gql(
    """
query GetTitleList($country: Country!, $titleListFilter: TitleFilter, $titleListSortBy: TitleListSorting! = POPULAR, $objectType: TitleListObjectType!, $titleListType: TitleListType!, $titleListAfterCursor: String, $watchNowFilter: WatchNowOfferFilter!, $first: Int! = 10, $language: Language!, $sortRandomSeed: Int! = 0, $profile: PosterProfile, $backdropProfile: BackdropProfile, $format: ImageFormat, $platform: Platform! = WEB, $includeUnreleasedEpisodes: Boolean = false, $includeOffers: Boolean = false) {\n  titleList(\n    after: $titleListAfterCursor\n    country: $country\n    filter: $titleListFilter\n    sortBy: $titleListSortBy\n    first: $first\n    objectType: $objectType\n    titleListType: $titleListType\n    sortRandomSeed: $sortRandomSeed\n  ) {\n    totalCount\n    pageInfo {\n      startCursor\n      endCursor\n      hasPreviousPage\n      hasNextPage\n      __typename\n    }\n    edges {\n      ...WatchlistTitleGraphql\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WatchlistTitleGraphql on TitleListEdge {\n  cursor\n  subheading {\n    ... on WatchNextSubheading {\n      watchNextSubheadingTechnicalName: technicalName\n      translatable\n      __typename\n    }\n    ... on CaughtUpSubheading {\n      caughtUpSubheadingTechnicalName: technicalName\n      translatable\n      __typename\n    }\n    __typename\n  }\n  node {\n    id\n    objectId\n    objectType\n    offerCount(country: $country, platform: $platform)\n    offers(country: $country, platform: $platform) @include(if: $includeOffers) {\n      id\n      presentationType\n      monetizationType\n      retailPrice(language: $language)\n      type\n      package {\n        packageId\n        clearName\n        __typename\n      }\n      standardWebURL\n      elementCount\n      deeplinkRoku: deeplinkURL(platform: ROKU_OS)\n      __typename\n    }\n    content(country: $country, language: $language) {\n      title\n      fullPath\n      originalReleaseYear\n      shortDescription\n      scoring {\n        imdbScore\n        imdbVotes\n        tmdbScore\n        tmdbPopularity\n        __typename\n      }\n      posterUrl(profile: $profile, format: $format)\n      backdrops(profile: $backdropProfile, format: $format) {\n        backdropUrl\n        __typename\n      }\n      upcomingReleases(releaseTypes: [DIGITAL]) {\n        releaseDate\n        __typename\n      }\n      __typename\n    }\n    likelistEntry {\n      createdAt\n      __typename\n    }\n    dislikelistEntry {\n      createdAt\n      __typename\n    }\n    watchlistEntry {\n      createdAt\n      __typename\n    }\n    watchNowOffer(country: $country, platform: $platform, filter: $watchNowFilter) {\n      id\n      standardWebURL\n      package {\n        packageId\n        clearName\n        __typename\n      }\n      retailPrice(language: $language)\n      retailPriceValue\n      currency\n      lastChangeRetailPriceValue\n      presentationType\n      monetizationType\n      availableTo\n      __typename\n    }\n    ... on Movie {\n      seenlistEntry {\n        createdAt\n        __typename\n      }\n      __typename\n    }\n    ... on Show {\n      totalSeasonCount\n      seenState(country: $country) {\n        seenEpisodeCount\n        releasedEpisodeCount\n        progress\n        caughtUp\n        lastSeenEpisodeNumber\n        lastSeenSeasonNumber\n        __typename\n      }\n      watchNextEpisode(\n        country: $country\n        includeUnreleasedEpisodes: $includeUnreleasedEpisodes\n      ) {\n        id\n        objectId\n        objectType\n        offerCount(country: $country, platform: $platform)\n        season {\n          content(country: $country, language: $language) {\n            fullPath\n            posterUrl\n            __typename\n          }\n          seenState(country: $country) {\n            releasedEpisodeCount\n            seenEpisodeCount\n            progress\n            __typename\n          }\n          __typename\n        }\n        season {\n          content(country: $country, language: $language) {\n            posterUrl\n            __typename\n          }\n          __typename\n        }\n        content(country: $country, language: $language) {\n          title\n          episodeNumber\n          seasonNumber\n          upcomingReleases(releaseTypes: [DIGITAL]) @include(if: $includeUnreleasedEpisodes) {\n            releaseDate\n            label\n            __typename\n          }\n          __typename\n        }\n        watchNowOffer(country: $country, platform: $platform, filter: $watchNowFilter) {\n          id\n          standardWebURL\n          package {\n            packageId\n            clearName\n            __typename\n          }\n          retailPrice(language: $language)\n          retailPriceValue\n          currency\n          lastChangeRetailPriceValue\n          presentationType\n          monetizationType\n          availableTo\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n
"""
)
# for stuff you have seen, titleListType = CAUGHT_UP
# for your watch list, titleListType = WATCH_NEXT
def queryConstructor(ref):
    params = {"titleListSortBy":"RELEVANCE","first":20,"sortRandomSeed":0,"platform":"WEB","includeUnreleasedEpisodes":True,"includeOffers":False,"titleListFilter":{"ageCertifications":[],"excludeGenres":[],"excludeProductionCountries":[],"genres":[],"objectTypes":["MOVIE"],"productionCountries":[],"packages":[],"excludeIrrelevantTitles":False,"presentationTypes":[],"monetizationTypes":[]},"watchNowFilter":{"packages":["nfx","amp","dnp","atp","hlu","hbm","amz","yot","ash","hop","vdu","crc","sho","pbs","sdn","mhz"],"monetizationTypes":[]},"language":"en","country":"US","objectType":"MOVIE","titleListType":"CAUGHT_UP","titleListAfterCursor":ref}
    return params

def dewit(client):
    edges = []
    nextCursor = ""
    hasNextPage = True

    while hasNextPage:
        params = queryConstructor(nextCursor)
        # Execute the query on the transport
        result = client.execute(query, variable_values=params)

        edges += result['titleList']['edges']
        nextCursor = result['titleList']['pageInfo']['endCursor']
        hasNextPage = result['titleList']['pageInfo']['hasNextPage']
    
    return edges

test = dewit(client)


# In[53]:


result = pd.json_normalize(test)
seenlist = pd.DataFrame(result)

# for a seenlist, use node.seenListEntry.createdAt to get the date added to your watched-list
# for a watchlist, it will be node.watchListEntry.createdAt
list_to_export = seenlist.filter(items=['node.content.title', 'node.content.originalReleaseYear', 'node.seenlistEntry.createdAt'])

list_to_export['Date'] = pd.to_datetime(list_to_export['node.seenlistEntry.createdAt']).dt.date
list_to_export['Name'] = list_to_export['node.content.title']
list_to_export['Year'] = list_to_export['node.content.originalReleaseYear']
list_to_export = list_to_export.filter(items=['Date', 'Name', 'Year'])


# In[54]:


list_to_export.to_csv('seenlist-import.csv', index=False)


# In[ ]:




