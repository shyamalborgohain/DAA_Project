
from itertools import combinations
from Q10 import optimal_transmitters as fast


def cd(a, b, L):
    d = abs(a - b) % L
    return min(d, L - d)


def brute(posts, L, candidates, r):
    if not posts:
        return 0

    best = None
    m = len(candidates)

    for mask in range(1, 1 << m):
        counts = [
            sum(
                1 for j in range(m)
                if mask & (1 << j)
                and cd(p, candidates[j], L) <= r
            )
            for p in posts
        ]

        if all(x >= 1 for x in counts):
            cost = sum(x >= 2 for x in counts)
            if best is None or cost < best:
                best = cost

    return best


def check_case(posts, L, candidates, r):
    expected = brute(posts, L, candidates, r)
    result = fast(posts, L, candidates, r)

    if result is None:
        actual = None
        valid = expected is None
    else:
        actual, locs = result

        # Check that returned locations are distinct original candidates.
        valid = (
            all(x in candidates for x in locs)
            and len(locs) == len(set(locs))
        )

        counts = [
            sum(cd(p, x, L) <= r for x in locs)
            for p in posts
        ]

        # Check coverage and recompute the reported objective.
        if posts:
            valid = valid and all(x >= 1 for x in counts)

        actual_cost = sum(x >= 2 for x in counts)
        valid = valid and actual == actual_cost

    if actual != expected or not valid:
        print("MISMATCH")
        print("L =", L, "radius =", r)
        print("posts =", posts)
        print("candidates =", candidates)
        print("fast result =", result)
        print("brute result =", expected)
        return False

    return True


def exhaustive_tests():
    tested = 0

    # Exhaustively enumerate small circles.
    for L in range(3, 8):
        positions = list(range(L))

        for r in range(1, L // 2 + 1):
            # Keep instances small enough for exhaustive subset search.
            for np in range(1, min(L, 3) + 1):
                for posts in combinations(positions, np):
                    for nc in range(1, min(L, 4) + 1):
                        for candidates in combinations(positions, nc):
                            if not check_case(
                                list(posts), L, list(candidates), r
                            ):
                                return

                            tested += 1

    print("Exhaustive tests passed:", tested)


def boundary_tests():
    cases = [
        # Coverage exactly at the radius.
        ([0, 2], 10, [1], 1),

        # Wraparound coverage near position 0.
        ([0, 9], 10, [9], 1),

        # A candidate covers no posts.
        ([0, 5], 10, [2, 0], 0),

        # One transmitter covers all posts.
        ([0, 2, 4], 10, [2], 5),

        # No candidates.
        ([0, 3], 10, [], 1),

        # Empty posts.
        ([], 10, [], 1),

        # Multiple candidates at identical physical locations.
        ([0, 4], 10, [1, 1, 7], 2),
    ]

    for posts, L, candidates, r in cases:
        if not check_case(posts, L, candidates, r):
            return

    print("Boundary tests passed:", len(cases))


if __name__ == "__main__":
    exhaustive_tests()
    boundary_tests()
