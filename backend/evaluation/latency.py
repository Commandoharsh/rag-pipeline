import time
from statistics import mean


class LatencyTimer:

    def measure(self, function, *args, **kwargs):

        start = time.perf_counter()

        result = function(
            *args,
            **kwargs
        )

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        return result, elapsed

    def benchmark(
        self,
        function,
        inputs,
        repeats: int = 1,
    ):

        measurements = []

        for item in inputs:

            for _ in range(repeats):

                _, elapsed = self.measure(
                    function,
                    item,
                )

                measurements.append(
                    elapsed
                )

        if not measurements:
            return {
                "count": 0,
                "average_ms": 0.0,
                "p95_ms": 0.0,
            }

        ordered = sorted(measurements)

        p95_index = min(
            len(ordered) - 1,
            int(len(ordered) * 0.95),
        )

        return {
            "count": len(measurements),
            "average_ms": mean(measurements),
            "p95_ms": ordered[p95_index],
            "min_ms": min(measurements),
            "max_ms": max(measurements),
        }