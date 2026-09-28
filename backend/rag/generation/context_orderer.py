class ContextOrderer:

    def order(self, results):

        return sorted(
            results,
            key=lambda result: result.score,
            reverse=True
        )