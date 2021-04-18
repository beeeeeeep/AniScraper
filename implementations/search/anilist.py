from data_scraping.api import APIParser, JSONSelector
from data_scraping.datasource import APISource
from service_classes.search import Search

query = '''
query($page: Int = 1 $id: Int $type: MediaType $isAdult: Boolean = false $search: String $format: [MediaFormat] $status: MediaStatus $countryOfOrigin: CountryCode $source: MediaSource $season: MediaSeason $seasonYear: Int $year: String $onList: Boolean $yearLesser: FuzzyDateInt $yearGreater: FuzzyDateInt $episodeLesser: Int $episodeGreater: Int $durationLesser: Int $durationGreater: Int $chapterLesser: Int $chapterGreater: Int $volumeLesser: Int $volumeGreater: Int $licensedBy: [String] $genres: [String] $excludedGenres: [String] $tags: [String] $excludedTags: [String] $minimumTagRank: Int $sort: [MediaSort] = [POPULARITY_DESC, SCORE_DESC]) {
    Page(page: $page, perPage: 20) {
        pageInfo {
            total perPage currentPage lastPage hasNextPage
        }
        media(id: $id type: $type season: $season format_in: $format status: $status countryOfOrigin: $countryOfOrigin source: $source search: $search onList: $onList seasonYear: $seasonYear startDate_like: $year startDate_lesser: $yearLesser startDate_greater: $yearGreater episodes_lesser: $episodeLesser episodes_greater: $episodeGreater duration_lesser: $durationLesser duration_greater: $durationGreater chapters_lesser: $chapterLesser chapters_greater: $chapterGreater volumes_lesser: $volumeLesser volumes_greater: $volumeGreater licensedBy_in: $licensedBy genre_in: $genres genre_not_in: $excludedGenres tag_in: $tags tag_not_in: $excludedTags minimumTagRank: $minimumTagRank sort: $sort isAdult: $isAdult) {
            id seasonYear title {
                romaji
                english
            }
        }
    }
}
'''

query_formatter = lambda x, kwargs: {
    "query": query,
    "variables": {
        "page": 1,
        "search": x,
        "sort": "SEARCH_MATCH" if kwargs.get("sort") is None else kwargs["sort"],
        "type": "ANIME"
    }
}

search = Search(
    APISource(
        url="https://graphql.anilist.co",
        request_type="POST",
        query_formatter=query_formatter,
        request_parser=APIParser(
            [
                JSONSelector(["data", "Page", "media", 0, "id"]),
                JSONSelector(["data", "Page", "media", 0, "seasonYear"]),
                JSONSelector(["data", "Page", "media", 0, "title", "romaji"]),
                JSONSelector(["data", "Page", "media", 0, "title", "english"])
            ], postprocess=lambda x: x)
    )
)
