
import random
import time

from Q10 import optimal_transmitters as fast

RADIUS = 250
TESTS = 10


def cd(a, b, L):
    """Shortest circular distance between two positions."""
    d = abs(a - b) % L
    return min(d, L - d)


def brute(posts, L, candidates, radius):
    """Return the exact minimum interference by exhaustive search."""
    if not posts:
        return 0

    n = len(posts)
    m = len(candidates)
    best = None

    coverage = [
        [cd(p, c, L) <= radius for p in posts]
        for c in candidates
    ]

    for mask in range(1, 1 << m):
        counts = [0] * n

        for j in range(m):
            if mask & (1 << j):
                for i in range(n):
                    if coverage[j][i]:
                        counts[i] += 1

        if all(count >= 1 for count in counts):
            cost = sum(count >= 2 for count in counts)

            if best is None or cost < best:
                best = cost

                if best == 0:
                    return 0

    return best


def inspect_solution(posts, L, candidates, result, radius):
    """Validate the returned locations and recompute interference."""
    if result is None:
        # Necessary condition for impossibility: some post cannot
        # be covered by any candidate.
        impossible_posts = [
            p for p in posts
            if not any(cd(p, c, L) <= radius for c in candidates)
        ]

        return {
            "valid": bool(impossible_posts),
            "locations": None,
            "counts": [],
            "interference": None,
            "uncovered": impossible_posts,
            "invalid_locations": [],
            "duplicates": [],
            "reported_cost_matches": False,
        }

    reported_cost, locations = result

    invalid_locations = [
        c for c in locations if c not in candidates
    ]

    duplicates = sorted({
        c for c in locations if locations.count(c) > 1
    })

    counts = [
        sum(cd(p, c, L) <= radius for c in locations)
        for p in posts
    ]

    uncovered = [
        p for p, count in zip(posts, counts)
        if count == 0
    ]

    interference = sum(count >= 2 for count in counts)
    reported_cost_matches = reported_cost == interference

    valid = (
        not invalid_locations
        and not duplicates
        and not uncovered
        and reported_cost_matches
    )

    return {
        "valid": valid,
        "locations": locations,
        "counts": counts,
        "interference": interference,
        "uncovered": uncovered,
        "invalid_locations": invalid_locations,
        "duplicates": duplicates,
        "reported_cost_matches": reported_cost_matches,
    }


def main():
    random.seed(20261019)
    started = time.time()
    all_passed = True

    for case in range(1, TESTS + 1):
        L = random.randint(1001, 3500)
        n = random.randint(70, 120)
        M = random.randint(13, 21)

        posts = random.sample(range(L), n)
        candidates = random.sample(range(L), M)

        # Include wraparound and exact-radius situations.
        # Keep candidates distinct after modification.
        if case % 3 == 0:
            posts[0] = 0
            candidates[0] = L - RADIUS
        elif case % 3 == 1:
            posts[0] = RADIUS
            candidates[0] = 0

        print("\n" + "=" * 78)
        print(f"TEST CASE {case}/{TESTS}")
        print("=" * 78)
        print(f"L = {L}")
        print(f"Radius = {RADIUS}")
        print(f"Number of posts = {len(posts)}")
        print(f"Number of candidates = {len(candidates)}")
        print("Posts:", posts)
        print("Candidate transmitter locations:", candidates)

        t0 = time.time()
        expected = brute(posts, L, candidates, RADIUS)
        brute_time = time.time() - t0

        t0 = time.time()
        result = fast(posts, L, candidates, RADIUS)
        algo_time = time.time() - t0

        print("\nAlgorithm output:", result)
        print("Brute-force optimum:", expected)

        details = inspect_solution(
            posts, L, candidates, result, RADIUS
        )

        if result is not None:
            print("Selected transmitter locations:", result[1])
            print("Reported interference:", result[0])
            print("Recounted interference:", details["interference"])
            print("Posts uncovered:", details["uncovered"])
            print("Invalid selected locations:", details["invalid_locations"])
            print("Duplicate selected locations:", details["duplicates"])
            print(
                "Reported count matches recount:",
                details["reported_cost_matches"],
            )
        else:
            print("No solution returned.")
            print(
                "Posts that cannot be covered individually:",
                details["uncovered"],
            )

        # If the algorithm says None but brute force found a solution,
        # it is a failure. If brute force says None but the algorithm
        # returned a solution, that is also a failure.
        if result is None or expected is None:
            optimality_matches = result is None and expected is None
        else:
            optimality_matches = result[0] == expected

        if result is None and expected is None:
            # A None result is correct if brute force independently
            # confirms no feasible subset exists.
            passed = True
            print("Selected locations valid: N/A (no solution exists)")
        else:
            passed = details["valid"] and optimality_matches
            print("Selected locations valid:", details["valid"])
            print("Every post covered:", not details["uncovered"])

        passed = passed and optimality_matches

        print("Optimality matches brute force:", optimality_matches)
        print(f"Algorithm time: {algo_time:.3f} seconds")
        print(f"Brute-force time: {brute_time:.3f} seconds")
        print("CASE RESULT:", "PASS" if passed else "FAIL")

        if not passed:
            all_passed = False
            print("\nFailure details:")
            print("Full algorithm result:", result)
            print("Brute-force optimum:", expected)

    print("\n" + "=" * 78)
    print(
        "FINAL RESULT:",
        "ALL TESTS PASSED" if all_passed else "FAILURES FOUND"
    )
    print(f"Total elapsed time: {time.time() - started:.2f} seconds")


if __name__ == "__main__":
    main()
