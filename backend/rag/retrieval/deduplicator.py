class ResultDeduplicator:

    def deduplicate(self, results):

        unique_results = []
        seen = set()

        for result in results:

            if result.chunk_id in seen:
                continue

            seen.add(result.chunk_id)
            unique_results.append(result)

        return unique_results