# src/benchmarks.py
# Performance benchmarking for ANITS Campus Assistant

import os
import sys
import time
import json
import statistics
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)


# ══════════════════════════════════════════
# TEST QUESTIONS
# ══════════════════════════════════════════
TEST_QUESTIONS = [
    # Locations
    ("Where is the canteen?", "locations"),
    ("Where is the placement cell?", "locations"),
    ("Where is the library?", "locations"),

    # Contacts
    ("Who is the HOD of CSE?", "contacts"),
    ("What is the TPO email?", "contacts"),

    # Placements
    ("What companies visit ANITS?", "placements"),
    ("What is the average placement package?", "placements"),

    # Clubs
    ("What clubs are available in ANITS?", "clubs"),
    ("How to join the Robotics club?", "clubs"),
    ("When is TechNova fest?", "clubs"),

    # Academics
    ("What departments are available in ANITS?", "academics"),
    ("When does odd semester begin?", "academics"),

    # Procedures
    ("How to apply for hostel admission?", "general"),
    ("How to get bonafide certificate?", "general"),
]


# ══════════════════════════════════════════
# BENCHMARK VECTOR SEARCH
# ══════════════════════════════════════════
def benchmark_vector_search() -> dict:
    """Measures FAISS search performance"""
    print("\n📊 Benchmarking Vector Search...")
    print("-" * 40)

    from src.vector_store import load_vector_store
    vector_store = load_vector_store()

    if not vector_store:
        return {"error": "Vector store not found!"}

    times = []
    results = []

    for question, category in TEST_QUESTIONS:
        start = time.time()
        docs = vector_store.similarity_search(question, k=5)
        elapsed = (time.time() - start) * 1000  # ms

        times.append(elapsed)
        results.append({
            "question": question,
            "category": category,
            "time_ms": round(elapsed, 2),
            "chunks_found": len(docs),
            "top_chunk_preview": docs[0].page_content[:80] + "..." if docs else "None"
        })

        print(f"  ✓ {question[:40]:<40} {elapsed:.1f}ms")

    return {
        "test": "Vector Search",
        "total_questions": len(TEST_QUESTIONS),
        "avg_time_ms": round(statistics.mean(times), 2),
        "min_time_ms": round(min(times), 2),
        "max_time_ms": round(max(times), 2),
        "std_dev_ms": round(statistics.stdev(times), 2),
        "results": results
    }


# ══════════════════════════════════════════
# BENCHMARK FULL PIPELINE
# ══════════════════════════════════════════
def benchmark_full_pipeline() -> dict:
    """Measures end-to-end response time"""
    print("\n📊 Benchmarking Full Pipeline...")
    print("-" * 40)

    from src.agent import build_agent, get_response
    chain = build_agent()

    if not chain:
        return {"error": "Agent not available!"}

    times = []
    results = []
    errors = 0

    # Test subset of questions
    test_subset = TEST_QUESTIONS[:6]

    for question, category in test_subset:
        start = time.time()
        answer = get_response(chain, question)
        elapsed = time.time() - start

        times.append(elapsed)
        success = "error" not in answer.lower() and len(answer) > 20

        if not success:
            errors += 1

        results.append({
            "question": question,
            "time_seconds": round(elapsed, 2),
            "answer_length": len(answer),
            "success": success,
            "answer_preview": answer[:100] + "..."
        })

        status = "✓" if success else "✗"
        print(f"  {status} {question[:40]:<40} {elapsed:.2f}s")

    return {
        "test": "Full Pipeline",
        "total_questions": len(test_subset),
        "successful": len(test_subset) - errors,
        "failed": errors,
        "success_rate": f"{round(((len(test_subset)-errors)/len(test_subset))*100, 1)}%",
        "avg_time_seconds": round(statistics.mean(times), 2),
        "min_time_seconds": round(min(times), 2),
        "max_time_seconds": round(max(times), 2),
        "results": results
    }


# ══════════════════════════════════════════
# BENCHMARK CACHE
# ══════════════════════════════════════════
def benchmark_cache() -> dict:
    """Measures cache speedup"""
    print("\n📊 Benchmarking Cache Performance...")
    print("-" * 40)

    from src.cache import save_to_cache, get_cached_response, clear_cache

    clear_cache()

    test_queries = [
        ("Where is the canteen?", "locations"),
        ("Who is the TPO?", "contacts"),
        ("When is TechNova?", "clubs"),
    ]

    # Simulate saving to cache
    for q, cat in test_queries:
        save_to_cache(q, f"Sample answer for: {q}", cat)

    # Benchmark cache hits
    cache_times = []
    for q, cat in test_queries:
        start = time.time()
        result = get_cached_response(q, cat)
        elapsed = (time.time() - start) * 1000
        cache_times.append(elapsed)
        print(f"  ✓ Cache hit: {q[:40]:<40} {elapsed:.3f}ms")

    # Compare with estimate of AI response time
    avg_ai_time = 3000  # 3 seconds average
    avg_cache_time = statistics.mean(cache_times)
    speedup = round(avg_ai_time / avg_cache_time, 0)

    return {
        "test": "Cache Performance",
        "avg_cache_time_ms": round(avg_cache_time, 3),
        "estimated_ai_time_ms": avg_ai_time,
        "speedup": f"{speedup}x faster",
        "cache_hit_times_ms": [round(t, 3) for t in cache_times]
    }


# ══════════════════════════════════════════
# BENCHMARK CATEGORY DETECTION
# ══════════════════════════════════════════
def benchmark_category_detection() -> dict:
    """Measures category detection accuracy"""
    print("\n📊 Benchmarking Category Detection...")
    print("-" * 40)

    sys.path.insert(0, os.path.join(PROJECT_ROOT, 'backend'))
    from backend.routes.search import detect_category

    correct = 0
    results = []

    for question, expected_category in TEST_QUESTIONS:
        start = time.time()
        detected = detect_category(question)
        elapsed = (time.time() - start) * 1000

        is_correct = detected == expected_category
        if is_correct:
            correct += 1

        results.append({
            "question": question,
            "expected": expected_category,
            "detected": detected,
            "correct": is_correct,
            "time_ms": round(elapsed, 3)
        })

        status = "✓" if is_correct else "✗"
        print(f"  {status} {question[:35]:<35} Expected: {expected_category:<12} Got: {detected}")

    accuracy = round((correct / len(TEST_QUESTIONS)) * 100, 1)

    return {
        "test": "Category Detection",
        "total": len(TEST_QUESTIONS),
        "correct": correct,
        "accuracy": f"{accuracy}%",
        "results": results
    }


# ══════════════════════════════════════════
# RUN ALL BENCHMARKS
# ══════════════════════════════════════════
def run_all_benchmarks() -> dict:
    """Runs complete benchmark suite"""
    print("\n" + "=" * 55)
    print("  ANITS Campus Assistant — Performance Benchmarks")
    print("=" * 55)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    report = {
        "generated_at": datetime.now().isoformat(),
        "benchmarks": {}
    }

    # 1. Vector Search
    report["benchmarks"]["vector_search"] = benchmark_vector_search()

    # 2. Cache Performance
    report["benchmarks"]["cache"] = benchmark_cache()

    # 3. Category Detection
    report["benchmarks"]["category_detection"] = benchmark_category_detection()

    # 4. Full Pipeline (takes longer — Groq API calls)
    print("\n⚠️  Full pipeline benchmark makes real API calls...")
    print("    This will take 1-2 minutes...")
    run_full = input("\n    Run full pipeline benchmark? (y/n): ").lower()
    if run_full == 'y':
        report["benchmarks"]["full_pipeline"] = benchmark_full_pipeline()
    else:
        print("    Skipping full pipeline benchmark.")

    # Print Summary
    print("\n" + "=" * 55)
    print("  BENCHMARK SUMMARY")
    print("=" * 55)

    vs = report["benchmarks"].get("vector_search", {})
    cache = report["benchmarks"].get("cache", {})
    cat = report["benchmarks"].get("category_detection", {})
    pipeline = report["benchmarks"].get("full_pipeline", {})

    print(f"\n  Vector Search:")
    print(f"    Average time: {vs.get('avg_time_ms', 'N/A')} ms")
    print(f"    Min time:     {vs.get('min_time_ms', 'N/A')} ms")
    print(f"    Max time:     {vs.get('max_time_ms', 'N/A')} ms")

    print(f"\n  Cache Performance:")
    print(f"    Average hit time: {cache.get('avg_cache_time_ms', 'N/A')} ms")
    print(f"    Speedup vs AI:    {cache.get('speedup', 'N/A')}")

    print(f"\n  Category Detection:")
    print(f"    Accuracy: {cat.get('accuracy', 'N/A')}")
    print(f"    Correct:  {cat.get('correct', 'N/A')}/{cat.get('total', 'N/A')}")

    if pipeline:
        print(f"\n  Full Pipeline:")
        print(f"    Success rate:  {pipeline.get('success_rate', 'N/A')}")
        print(f"    Average time:  {pipeline.get('avg_time_seconds', 'N/A')}s")

    # Save report
    report_path = os.path.join(PROJECT_ROOT, "benchmark_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n  ✅ Full report saved to: benchmark_report.json")
    print("=" * 55)

    return report


# ══════════════════════════════════════════
# TEST
# ══════════════════════════════════════════
if __name__ == "__main__":
    run_all_benchmarks()