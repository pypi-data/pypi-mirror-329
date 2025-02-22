from airflow.models.baseoperator import BaseOperator

PAGE_SIZE = 3

class AlfrescoSearchOperator(BaseOperator):
    """
    Simple operator that uses the Alfresco search API.
    """
    from requests import Response

    def __init__(self, query, *args, **kwargs):
        from airflow.providers.http.hooks.http import HttpHook
        super().__init__(*args, **kwargs)
        self.http_hook = HttpHook(method="POST", http_conn_id="alfresco_api")
        self.query = query

    def execute(self, context):
        self.log.debug(f"search query={self.query}")

        self.data = {
            "query": {
                "query": self.query,
            },
            "paging": {
                "maxItems": PAGE_SIZE,
                "skipCount": 0
            },
            "include": ["path", "aspectNames", "properties"],
            "sort": [{"type": "FIELD", "field": "cm:created", "ascending": False}]
        }

        results = self.fetch_results(self.query)

        self.log.debug("--search results--")
        for result in results:
            self.log.debug(result)

        return results

    def fetch_results(self, query):
        entries = []

        response = self.http_hook.run(
            endpoint="/alfresco/api/-default-/public/search/versions/1/search",
            json=self.data,
        )
        all_responses = [response]
        while True:
            next_page_params = self.paginate(response)
            if not next_page_params:
                break
            self.log.info(f"Load next page with skipCount={next_page_params['skipCount']}")
            self.data["paging"]["skipCount"] = next_page_params["skipCount"]
            response = self.http_hook.run(
                endpoint="/alfresco/api/-default-/public/search/versions/1/search",
                json=self.data,
            )
            all_responses.append(response)

        for raw_resp in all_responses:
            resp_json = raw_resp.json()
            for e in resp_json["list"]["entries"]:
                entries.append(e["entry"])

        return entries

    def paginate(self, response: Response) -> dict:
        content = response.json()

        pagination = content['list']['pagination']
        count = pagination['count']
        skip_count = pagination['skipCount']
        max_items = pagination['maxItems']
        self.log.debug(f"Request Alfresco pagination {count}/{max_items} ")

        if pagination['hasMoreItems']:
            return {"skipCount": skip_count + PAGE_SIZE}
        else:
            return None
