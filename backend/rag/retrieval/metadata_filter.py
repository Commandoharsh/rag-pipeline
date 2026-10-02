class MetadataFilter:

    def filter(
        self,
        results,
        metadata: dict | None = None,
    ):

        if not metadata:
            return results

        filtered = []

        for result in results:

            result_metadata = result.metadata

            matches = True

            for key, expected_value in metadata.items():

                if result_metadata.get(key) != expected_value:
                    matches = False
                    break

            if matches:
                filtered.append(result)

        return filtered