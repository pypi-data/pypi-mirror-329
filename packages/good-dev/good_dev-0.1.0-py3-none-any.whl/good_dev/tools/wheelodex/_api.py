# @lru_cache(maxsize=10000)
import asyncio
import collections
import datetime
import itertools
import re
import urllib.parse
from functools import reduce

import httpx
import tqdm
from cashews import cache
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from good_dev.config import CONFIG_DIR, settings
from good_common.utilities import parse_timestamp

Gb = 1073741824
cache.setup(
    f"disk://?directory={CONFIG_DIR.joinpath('cache')}&timeout=1",
    size_limit=1 * Gb,
    shards=12,
)


def _url_ttl(_, url: str, **kwargs):
    # logger.debug(url)
    if "pypi.org" in url:
        return datetime.timedelta(days=7)
    elif "wheelodex.org" in url:
        return datetime.timedelta(days=1)
    elif "github.com" in url:
        return datetime.timedelta(days=7)
    else:
        return datetime.timedelta(days=3)


@cache(ttl=_url_ttl, key="fetch-url:{url}")
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch_proxy_fallback(
    client: httpx.AsyncClient, url: str, raise_for_status: bool = True
):
    """
    Attempt to fetch URL directly. If 403, 429 or 503 is returned, fetch again using proxy API
    """

    SCRAPEDO_API_KEY = settings.secrets.scrapedo

    if not SCRAPEDO_API_KEY or SCRAPEDO_API_KEY == "":
        raise ValueError("SCRAPEDO_API_KEY is not set")

    response = await client.get(url)

    if response.status_code in {403, 429, 503}:
        logger.debug(f"Got {response.status_code} for {url} - retrying with proxy")
        try:
            response = await client.get(
                f"http://api.scrape.do?token={SCRAPEDO_API_KEY}&url={urllib.parse.quote(url)}",
                timeout=15,
            )
        except (httpx.ReadError, httpx.ReadTimeout, httpx.TimeoutException):
            return httpx.Response(500)

    if raise_for_status:
        response.raise_for_status()  # noqa

    return response


async def _get_reverse_dependencies(
    sem: asyncio.Semaphore, client: httpx.AsyncClient, package: str, page: int = 1
) -> tuple[set[str], int]:
    async with sem:
        url = f"https://www.wheelodex.org/json/projects/{package}/rdepends"

        if page > 1:
            url += f"?page={page}"

        # 'https://www.wheelodex.org/json/projects/anyio/rdepends'

        logger.info(f"Fetching {url}")

        # print(f"http://api.scrape.do?token={SCRAPEDO_API_KEY}&url={url}")

        response = await fetch_proxy_fallback(client, url)

        logger.info(f"Got response {response.status_code} for {url}")

        data = response.json()

        total = data.get("total", 0)

        dependencies: list[dict[str, str]] = data.get("items", [])

        return set(
            [item["href"].replace("/json/projects/", "") for item in dependencies]
        ), total


def clean_dependencies_list(dependencies: list[str]) -> list[str]:
    """
    Clean up the dependencies list by removing version constraints
    """
    return list(
        set([re.split(r"[<>=!~\s\[]", dep.split(";")[0])[0] for dep in dependencies])
    )


def _filter_empty(data: dict) -> dict:
    return {k: v for k, v in data.items() if v}


async def _get_package_metadata(sem, client, package):
    async with sem:
        url = f"https://pypi.org/pypi/{package}/json"

        response = await fetch_proxy_fallback(client, url)

        data = response.json()

        info = data.get("info", {})

        dependencies = clean_dependencies_list(
            data.get("info", {}).get("requires_dist", []) or []
        )

        if info.get("project_urls") is None:
            info["project_urls"] = {}

        source_key = [
            k
            for k in info.get("project_urls", {}).keys()
            if "source" in k.lower() or "repo" in k.lower()
        ]

        if not source_key:
            source_key = [
                k for k, v in info.get("project_urls", {}).items() if "git" in v.lower()
            ]

        source = info.get("project_urls", {}).get(source_key[0]) if source_key else None

        current_releases = data.get("releases", {}).get(info.get("version"), [])

        # logger.info(current_releases)

        last_release_timestamp = None
        if current_releases:
            _dates = [
                parse_timestamp(r["upload_time"])
                for r in current_releases
                if r.get("upload_time")
            ]
            _dates = filter(lambda x: x is not None, _dates)
            if _dates:
                last_release_timestamp = max(_dates)

        repo_data = {}
        if source:
            try:
                repo_slug = "/".join(source.split("github.com/")[-1].split("/")[:2])
            except (IndexError, ValueError):
                repo_slug = None

            if repo_slug:
                response = await fetch_proxy_fallback(
                    client,
                    f"https://api.github.com/repos/{repo_slug}",
                    raise_for_status=False,
                )

                if response.status_code == 200:
                    _repo_data = _filter_empty(response.json())

                    hn_threads = []

                    response = await fetch_proxy_fallback(
                        client,
                        f"https://hn.algolia.com/api/v1/search?query=github.com/{repo_slug}&restrictSearchableAttributes=url",
                        raise_for_status=False,
                    )

                    if response.status_code == 200:
                        hn_data = response.json()
                        hn_threads = [
                            {
                                "title": hn_hit.get("title"),
                                "created_at": hn_hit.get("created_at"),
                                "thread": "https://news.ycombinator.com/item?id="
                                + str(hn_hit.get("objectID")),
                                "points": hn_hit.get("points"),
                                "comments": hn_hit.get("num_comments"),
                            }
                            for hn_hit in hn_data.get("hits", [])
                        ]
                        hn_threads = sorted(
                            hn_threads,
                            key=lambda x: parse_timestamp(x.get("created_at")) or 0,
                            reverse=True,
                        )

                    repo_data = {
                        "description": _repo_data.get("description"),
                        "created_at": _repo_data.get("created_at"),
                        "updated_at": _repo_data.get("updated_at"),
                        "pushed_at": _repo_data.get("pushed_at"),
                        "stars": _repo_data.get("stargazers_count"),
                        "forks": _repo_data.get("forks_count"),
                        "watchers": _repo_data.get("watchers_count"),
                        "license": _repo_data.get("license", {}).get("name"),
                        "topics": _repo_data.get("topics"),
                        "open_issues": _repo_data.get("open_issues_count"),
                        "owner": {
                            "url": _repo_data.get("owner", {}).get("html_url"),
                            "type": _repo_data.get("owner", {}).get("type"),
                        },
                        "hn_threads": hn_threads if hn_threads else None,
                    }

        project_data = {
            "name": info.get("name"),
            "summary": info.get("summary"),
            "version": info.get("version"),
            "project_url": info.get("project_url"),
            "documentation": info.get("project_urls", {}).get("Documentation"),
            "homepage": info.get("project_urls", {}).get("Homepage"),
            "source": info.get("project_urls", {}).get(source_key[0])
            if source_key
            else None,
            "repo_data": _filter_empty(repo_data),
            "dependencies": dependencies,
            "last_release": last_release_timestamp,
        }

        return _filter_empty(project_data)


@retry(stop=stop_after_attempt(3))
async def get_package_reverse_dependencies(
    client: httpx.AsyncClient,
    package: str,
    sem: asyncio.Semaphore = None,
    position: int = 1,
) -> set[str]:
    async with sem:
        dependencies, total_dependencies = await _get_reverse_dependencies(
            sem, client, package, 1
        )

        max_pages = total_dependencies // 100

        tqdm.tqdm.write(
            f"Found {total_dependencies} reverse dependencies for {package} - fetch {max_pages} pages"
        )

        pages = [
            _get_reverse_dependencies(sem, client, package, page)
            for page in range(2, max_pages)
        ]

        for page in tqdm.tqdm(
            asyncio.as_completed(pages),
            total=len(pages),
            position=position,
            disable=True,
        ):
            _dependencies, _ = await page
            dependencies.update(_dependencies)

    return dependencies


def _to_int(dt: str | datetime.datetime | int) -> int:
    if isinstance(dt, int):
        return dt
    if isinstance(dt, str):
        dt = datetime.datetime.fromisoformat(dt)
    return int(dt.timestamp())


async def build_dependency_graph(dependency_list: list[str]):
    sem = asyncio.Semaphore(20)
    async with httpx.AsyncClient(
        # limits=httpx.Limits(
        #     max_keepalive_connections=30,
        #     max_connections=30
        # ),
        timeout=httpx.Timeout(20, connect=60.0, pool=120, read=60)
    ) as client:
        package_metadata = await asyncio.gather(
            *[
                _get_package_metadata(sem, client, package)
                for package in dependency_list
            ]
        )

        dependency_graph = {
            package: output
            for package, output in zip(
                dependency_list,
                await asyncio.gather(
                    *[
                        get_package_reverse_dependencies(
                            client, package, sem, position=ix + 1
                        )
                        for ix, package in enumerate(dependency_list)
                    ]
                ),
            )
        }

        _common_dependencies = (
            sorted(
                list(reduce(lambda a, b: a.intersection(b), dependency_graph.values()))
            )
            if dependency_graph
            else []
        )

        jobs = [
            asyncio.create_task(_get_package_metadata(sem, client, package))
            for package in _common_dependencies
        ]

        dependency_metadata = []

        for job in tqdm.tqdm(
            asyncio.as_completed(jobs),
            total=len(jobs),
            position=0,
            disable=False,
            desc="Fetching common dependencies metadata",
        ):
            dependency_metadata.append(await job)

        common_dependencies = sorted(
            dependency_metadata,
            key=lambda x: x.get("repo_data", {}).get("stars", 0)
            + _to_int(datetime.datetime.now())
            if x.get("repo_data")
            else _to_int(x.get("last_release", 0)),
            reverse=True,
        )

        _dep_idx = {
            obj["name"]: set(obj.get("dependencies", []))
            for obj in common_dependencies
            if obj.get("dependencies")
        }

        _most_common = collections.Counter(itertools.chain(*_dep_idx.values()))

        _root_packages = set(dependency_list)

    return {
        "packages": package_metadata,
        "common_dependents": common_dependencies,
        "most_common_other_dependencies": {
            k: _c
            for k, _c in _most_common.most_common()
            if _c > 1 and k not in _root_packages
        },
        "all": {k: list(a) for k, a in dependency_graph.items()},
    }
