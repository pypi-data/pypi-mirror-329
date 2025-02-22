from fast_pdf_extract import get_pages_threads


def two_files_threading():
    import concurrent.futures
    import time

    start = time.time()

    files = [
        "/users/Pratyush/Temporary/pnb.pdf",
        "/users/Pratyush/Temporary/pnb.pdf",
        "/users/Pratyush/Temporary/pnb.pdf",
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(get_pages_threads, files)
    for pages in results:
        print("text size", len("\n\n".join(pages)))
    print("time taken threading", time.time() - start)


if __name__ == "__main__":
    two_files_threading()
