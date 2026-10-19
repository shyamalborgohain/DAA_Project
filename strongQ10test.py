
import random
import time

from Q10 import optimal_transmitters as fast

RADIUS = 250
TESTS = 10


def cd(a, b, L):
    """Shortest circular distance between positions a and b."""
    d = abs(a - b) % L
    return min(d, L - d)


def brute(posts, L, candidates, r):
    """Return the exact minimum interference using exhaustive search."""
    if not posts:
        return 0

    m = len(candidates)
    n = len(posts)
    best = None

    # Precompute which posts each candidate covers.
    coverage = [
        [cd(p, c, L) <= r for p in posts]
        for c in candidates
    ]

    # Enumerate every nonempty subset of candidates.
    for mask in range(1, 1 << m):
        counts = [0] * n

        for j in range(m):
            if mask & (1 << j):
                for i in range(n):
                    if coverage[j][i]:
                        counts[i] += 1

        # All posts must be covered.
        if all(count >= 1 for count in counts):
            # Count each multiply covered post only once.
            cost = sum(count >= 2 for count in counts)

            if best is None or cost < best:
                best = cost

                # Cannot improve on zero interference.
                if best == 0:
                    return 0

    # None means no subset covers every post.
    return best



def validate(posts, L, candidates, result, expected):
    """Validate feasibility, selected locations, and optimality."""

    # Handle impossible instances first.
    if result is None:
        return expected is None

    # If brute force says no solution exists but the algorithm
    # returns one, the result is incorrect.
    if expected is None:
        return False

    value, locs = result

    # Selected locations must be distinct original candidates.
    if not set(locs) <= set(candidates):
        return False

    if len(locs) != len(set(locs)):
        return False

    # Count coverage of every post.
    counts = [
        sum(cd(p, c, L) <= RADIUS for c in locs)
        for p in posts
    ]

    # Every post must be covered at least once.
    if any(count == 0 for count in counts):
        return False

    actual_interference = sum(count >= 2 for count in counts)

    # Reported cost must match actual interference and optimum.
    return (
        value == actual_interference
        and value == expected
    )



def main():
    random.seed(20261019)
    start_time = time.time()

    print("RANDOMIZED BRUTE-FORCE COMPARISON")
    print(f"Radius: {RADIUS}")
    print(f"Test cases: {TESTS}")
    print(f"Candidates per case: {M}")
    print("Road length range: 1001–2500")
    print("Posts per case: 70–100")
    print()

    header = (
        f"{'Case':<6}"
        f"{'L':<7}"
        f"{'Posts':<8}"
        f"{'Candidates':<12}"
        f"{'Algorithm':<12}"
        f"{'Brute Force':<13}"
        f"{'Status':<8}"
    )

    print(header)
    print("-" * len(header))

    all_passed = True

    for case in range(1, TESTS + 1):
        L = random.randint(1001, 2500)
        n = random.randint(70, min(100, L))
        M = random.randint(13, 21)

        posts = random.sample(range(L), n)
        candidates = random.sample(range(L), M)

        # Include wraparound and exact-radius scenarios.
        # Replace existing entries to keep list lengths unchanged.
        if case % 3 == 0:
            posts[0] = 0
            candidates[0] = L - RADIUS
        elif case % 3 == 1:
            posts[0] = RADIUS
            candidates[0] = 0

        # Exact answer from exhaustive search.
        expected = brute(posts, L, candidates, RADIUS)

        # Answer from the algorithm being tested.
        result = fast(posts, L, candidates, RADIUS)

        valid = validate(
            posts, L, candidates, result, expected
        )

        algorithm_value = (
            result[0] if result is not None else None
        )

        status = "PASS" if valid else "FAIL"

        print(
            f"{case:<6}"
            f"{L:<7}"
            f"{n:<8}"
            f"{M:<12}"
            f"{str(algorithm_value):<12}"
            f"{str(expected):<13}"
            f"{status:<8}"
        )

        if not valid:
            all_passed = False
            print("  Posts:", posts)
            print("  Candidates:", candidates)
            print("  Full algorithm result:", result)

    print("-" * len(header))
    print(
        "Overall result:",
        "ALL TESTS PASSED" if all_passed else "FAILURES FOUND"
    )
    print(f"Total elapsed time: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
