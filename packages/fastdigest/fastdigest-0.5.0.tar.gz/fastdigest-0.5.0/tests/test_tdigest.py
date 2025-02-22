import pytest
import math
import pickle
from copy import copy, deepcopy
from fastdigest import TDigest, merge_all


def check_tdigest_equality(
        original: TDigest,
        new: TDigest,
        rel_tol: float=1e-9
    ):
    # Sanity checks
    assert isinstance(new, TDigest), (
        f"Expected TDigest, got {type(new).__name__}"
    )
    assert new.max_centroids == original.max_centroids, (
        f"Expected max_centroids={original.max_centroids}, got {new.max_centroids}"
    )
    assert new.n_values == original.n_values, (
        f"Expected {original.n_values} values, got {new.n_values}"
    )
    assert new.n_centroids == original.n_centroids, (
        f"Expected {original.n_centroids} centroids, "
        f"got {new.n_centroids}"
    )

    # Verify that quantile estimates match within a reasonable tolerance
    for q in [0.25, 0.5, 0.75]:
        orig_val = original.quantile(q)
        new_val = new.quantile(q)
        assert math.isclose(orig_val, new_val, rel_tol=rel_tol), (
            f"Quantile {q} mismatch: original {orig_val} vs new {new_val}"
        )


def test_init():
    # Test proper initialization with a non-empty list
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    digest = TDigest(values)
    assert digest.max_centroids is None
    assert digest.n_values == 5
    assert digest.n_centroids == 5

    digest = TDigest(values, max_centroids=3)
    assert digest.max_centroids == 3
    assert digest.n_values == 5
    assert digest.n_centroids == 3

    # Test that an empty list raises ValueError
    with pytest.raises(ValueError):
        TDigest([])

def test_n_values():
    digest = TDigest([1.0, 2.0, 3.0])
    n_values = digest.n_values
    assert isinstance(n_values, int), (
        f"Expected int, got {type(n_values).__name__}"
    )
    assert n_values == 3, f"Expected 3, got {n_values}"

def test_n_centroids():
    digest = TDigest([1.0, 2.0, 3.0])
    n_centroids = digest.n_centroids
    assert isinstance(n_centroids, int), (
        f"Expected int, got {type(n_centroids).__name__}"
    )
    assert n_centroids == 3, f"Expected 3, got {n_centroids}"

def test_compress():
    digest = TDigest(range(1, 101))
    # Compress the digest to at most 5 centroids. Note that for N values
    # ingested, it will never go below min(N, 3) centroids.
    digest.compress(5)
    compressed_centroids = len(digest)
    assert 3 <= compressed_centroids <= 5, (
        f"Expected between 3 and 5 centroids, got {compressed_centroids}"
    )
    # Check that quantile estimates remain plausible after compression
    quantile_est = digest.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )

def test_merge():
    # Create two TDigest instances from non-overlapping ranges
    digest1 = TDigest(range(1, 51))
    digest2 = TDigest(range(51, 101))
    merged = digest1.merge(digest2)
    # The median of the merged data should be around 50.5
    quantile_est = merged.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )
    assert len(merged) == 100, (
        f"Expected 100 centroids, got {len(merged)}"
    )
    digest1.max_centroids = 3
    merged = digest1.merge(digest2)
    assert len(merged) == 100, (
        f"Expected 100 centroids, got {len(merged)}"
    )
    digest2.max_centroids = 50
    merged = digest1.merge(digest2)
    assert 3 < len(merged) <= 50, (
        f"Expected between 4 and 50 centroids, got {len(merged)}"
    )
    digest2.max_centroids = 3
    merged = digest1.merge(digest2)
    assert len(merged) == 3, (
        f"Expected 3 centroids, got {len(merged)}"
    )

def test_merge_inplace():
    # Create two TDigest instances from non-overlapping ranges
    digest1 = TDigest(range(1, 51))
    digest2 = TDigest(range(51, 101))
    digest1.merge_inplace(digest2)
    # The median of the merged data should be around 50.5
    quantile_est = digest1.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )
    assert len(digest1) == 100, (
        f"Expected 100 centroids, got {len(digest1)}"
    )
    digest1.max_centroids = 3
    digest1.merge_inplace(digest2)
    assert len(digest1) == 3, (
        f"Expected 3 centroids, got {len(digest1)}"
    )
    digest2.max_centroids = 50
    digest1.merge_inplace(digest2)
    assert len(digest1) == 3, (
        f"Expected 3 centroids, got {len(digest1)}"
    )

def test_batch_update():
    digest = TDigest(range(1, 51))
    digest.batch_update(range(51, 101))
    # The median of the merged data should be around 50.5
    quantile_est = digest.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )
    assert len(digest) == 100, (
        f"Expected 100 centroids, got {len(digest)}"
    )
    digest = TDigest(range(1, 51), max_centroids=3)
    digest.batch_update(range(51, 101))
    quantile_est = digest.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )
    assert len(digest) == 3, (
        f"Expected 3 centroids, got {len(digest)}"
    )

def test_update():
    digest = TDigest(range(1, 100))
    digest.update(100)
    # The median of the merged data should be around 50.5
    quantile_est = digest.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )
    assert len(digest) == 100, (
        f"Expected 100 centroids, got {len(digest)}"
    )
    digest = TDigest(range(1, 100), max_centroids=3)
    digest.update(100)
    quantile_est = digest.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )
    assert len(digest) == 3, (
        f"Expected 3 centroids, got {len(digest)}"
    )

def test_quantile():
    # Create a digest from 1..100
    digest = TDigest(range(1, 101))
    # For a uniformly distributed dataset, the median should be near 50.5
    q = 0.5
    quantile_est = digest.quantile(q)
    expected = 1 + q * (100 - 1)  # 1 + 0.5*99 = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected ~{expected}, got {quantile_est}"
    )

def test_percentile():
    # Create a digest from 1..100
    digest = TDigest(range(1, 101))
    # For a uniformly distributed dataset, the median should be near 50.5
    p = 50
    quantile_est = digest.percentile(p)
    expected = 1 + (p / 100) * (100 - 1)  # 1 + 0.5*99 = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected ~{expected}, got {quantile_est}"
    )

def test_rank():
    digest = TDigest(range(1, 101))
    x = 50
    rank_est = digest.rank(x)
    # For uniform data, expected rank is (x - min)/(max - min)
    expected = (50 - 1) / (100 - 1)
    assert 0 <= rank_est <= 1, "Rank should be between 0 and 1"
    assert math.isclose(rank_est, expected, rel_tol=1e-3), (
        f"Expected ~{expected}, got {rank_est}"
    )

def test_trimmed_mean():
    values = list(range(101))
    values.append(10_000)
    digest = TDigest(values)
    # 1st percentile is 1.01, 99th percentile is 99.99. (2 + 99) / 2 = 50.5
    trimmed = digest.trimmed_mean(0.01, 0.99)
    expected = 50.5
    assert math.isclose(trimmed, expected, rel_tol=1e-3), (
        f"Expected trimmed mean ~{expected}, got {trimmed}"
    )
    # Ensure that providing invalid quantiles raises a ValueError.
    with pytest.raises(ValueError):
        digest.trimmed_mean(0.9, 0.1)

def test_to_from_dict():
    original = TDigest([1.0, 2.0, 3.0])
    digest_dict = original.to_dict()
    assert isinstance(digest_dict, dict), (
        f"Expected dict, got {type(digest_dict).__name__}"
    )
    new = TDigest.from_dict(digest_dict)
    check_tdigest_equality(original, new)
    original = TDigest(range(1, 101), max_centroids=3)
    digest_dict = original.to_dict()
    new = TDigest.from_dict(digest_dict)
    check_tdigest_equality(original, new)

def test_copy():
    digest = TDigest([1.0, 2.0, 3.0])
    digest_copy = digest.copy()
    check_tdigest_equality(digest, digest_copy)
    assert id(digest_copy) != id(digest), (
        "The copy should be a separate instance."
    )

def test_copy_magic():
    digest = TDigest([1.0, 2.0, 3.0])
    digest_copy = copy(digest)
    check_tdigest_equality(digest, digest_copy)
    assert id(digest_copy) != id(digest), (
        "The copy should be a separate instance."
    )

def test_deepcopy():
    digest = TDigest([1.0, 2.0, 3.0])
    digest_copy = deepcopy(digest)
    check_tdigest_equality(digest, digest_copy)
    assert id(digest_copy) != id(digest), (
        "The copy should be a separate instance."
    )

def test_pickle_unpickle():
    original = TDigest([1.0, 2.0, 3.0])
    dumped = pickle.dumps(original)
    unpickled = pickle.loads(dumped)
    check_tdigest_equality(original, unpickled)
    original = TDigest(range(1, 101), max_centroids=3)
    dumped = pickle.dumps(original)
    unpickled = pickle.loads(dumped)
    check_tdigest_equality(original, unpickled)

def test_len():
    digest = TDigest([1.0, 2.0, 3.0])
    length = len(digest)
    assert isinstance(length, int), (
        f"Expected int, got {type(length).__name__}"
    )
    assert length == 3, f"Expected 3, got {length}"

def test_eq():
    digest1 = TDigest([1.0, 2.0, 3.0])
    digest2 = TDigest([1.0, 2.0, 3.0])
    digest3 = TDigest([1.0, 2.0, 3.1])
    digest4 = TDigest([1.0, 2.0, 3.0], max_centroids=3)
    assert digest1 == digest2
    assert not digest1 == digest3
    assert not digest1 == digest4

def test_ne():
    digest1 = TDigest([1.0, 2.0, 3.0])
    digest2 = TDigest([1.0, 2.0, 3.0])
    digest3 = TDigest([1.0, 2.0, 3.1])
    digest4 = TDigest([1.0, 2.0, 3.0], max_centroids=3)
    assert not digest1 != digest2
    assert digest1 != digest3
    assert digest1 != digest4

def test_repr():
    digest = TDigest([1.0, 2.0, 3.0])
    rep = repr(digest)
    assert rep == "TDigest(max_centroids=None)", (
        f"__repr__ output unexpected: {rep}"
    )
    digest = TDigest([1.0, 2.0, 3.0], max_centroids=100)
    rep = repr(digest)
    assert rep == "TDigest(max_centroids=100)", (
        f"__repr__ output unexpected: {rep}"
    )

def test_add():
    # Create two TDigest instances from non-overlapping ranges
    digest1 = TDigest(range(1, 51))
    digest2 = TDigest(range(51, 101))
    merged = digest1 + digest2
    # The median of the merged data should be around 50.5
    quantile_est = merged.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )

def test_iadd():
    # Create two TDigest instances from non-overlapping ranges
    digest1 = TDigest(range(1, 51))
    digest2 = TDigest(range(51, 101))
    digest1 += digest2
    # The median of the merged data should be around 50.5
    quantile_est = digest1.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )

def test_merge_all():
    digests = [TDigest(range(i, i+10)) for i in range(1, 100, 10)]
    assert len(digests) == 10
    merged = merge_all(digests)
    # The median of the merged data should be around 50.5
    quantile_est = merged.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )
    assert len(merged) == 100, (
        f"Expected 100 centroids, got {len(merged)}"
    )
    merged = merge_all(digests, max_centroids=3)
    quantile_est = merged.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )
    assert len(merged) == 3, (
        f"Expected 3 centroids, got {len(merged)}"
    )
    for i, digest in enumerate(digests[:-1]):
        digest.max_centroids = 3 + i
    digests[-1].max_centroids = 50
    merged = merge_all(digests)
    quantile_est = merged.quantile(0.5)
    expected = 50.5
    assert math.isclose(quantile_est, expected, rel_tol=1e-3), (
        f"Expected median ~{expected}, got {quantile_est}"
    )
    assert 11 < len(merged) <= 50, (
        f"Expected between 12 and 29 centroids, got {len(merged)}"
    )


if __name__ == "__main__":
    test_init()
    test_n_values()
    test_n_centroids()
    test_merge()
    test_merge_inplace()
    test_compress()
    test_batch_update()
    test_update()
    test_quantile()
    test_percentile()
    test_rank()
    test_trimmed_mean()
    test_to_from_dict()
    test_copy()
    test_copy_magic()
    test_deepcopy()
    test_pickle_unpickle()
    test_len()
    test_eq()
    test_ne()
    test_repr()
    test_add()
    test_iadd()
    test_merge_all()
