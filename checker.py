# Android/Termux adaptation
# Batch processing + resumable progress

from config import (
    os,
    Fore,
    cloudscraper,
    time,
    threading,
    ThreadPoolExecutor,
    as_completed,
    random,
    TiktokUsernameChecker
)


BATCH_SIZE = 50
PROGRESS_FILE = os.path.join(
    TiktokUsernameChecker.directory,
    "output",
    "progress.txt"
)

AVAILABLE_FILE = os.path.join(
    TiktokUsernameChecker.directory,
    "output",
    "available_usernames.txt"
)


thread_local = threading.local()


def get_scraper():
    """
    Reuse one Cloudscraper session per worker thread.
    """

    if not hasattr(thread_local, "scraper"):
        thread_local.scraper = cloudscraper.create_scraper()

    return thread_local.scraper


def load_progress():
    """
    Return the number of usernames already processed.
    """

    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            value = f.read().strip()

        if value.isdigit():
            return int(value)

    except FileNotFoundError:
        pass
    except Exception:
        pass

    return 0


def save_progress(position):
    """
    Save progress atomically.
    """

    temporary = PROGRESS_FILE + ".tmp"

    with open(temporary, "w", encoding="utf-8") as f:
        f.write(str(position))

    os.replace(temporary, PROGRESS_FILE)


def checker_main():

    usernames = list(TiktokUsernameChecker.usernames)

    if not usernames:
        print(Fore.RED + "\nNo usernames found.")
        return

    start = load_progress()

    if start >= len(usernames):
        print(
            Fore.GREEN +
            "\nAll usernames have already been processed."
        )
        print(
            "Delete output/progress.txt if you want to start again."
        )
        return

    remaining = len(usernames) - start

    print(
        Fore.CYAN +
        f"\nLoaded {len(usernames)} usernames."
    )

    print(
        Fore.YELLOW +
        f"Already processed: {start}"
    )

    print(
        Fore.YELLOW +
        f"Remaining: {remaining}"
    )

    print(
        Fore.YELLOW +
        f"Threads: {TiktokUsernameChecker.threads}"
    )

    print(
        Fore.CYAN +
        "\nPress Ctrl+C to stop safely.\n"
    )

    TiktokUsernameChecker.stop_event.clear()

    while True:
        show_unavailable = input(
            "\n[1] Show unavailable usernames\n[2] Hide unavailable usernames\n\n"
            "Your choice: "
        ).strip()

        if show_unavailable in ("1", "2"):
            TiktokUsernameChecker.show_unavailable = (show_unavailable == "1")
            break

        print(Fore.RED + "\nChoose either 1 or 2.\n")


    position = start

    try:

        while position < len(usernames):

            if TiktokUsernameChecker.stop_event.is_set():
                break

            batch_end = min(
                position + BATCH_SIZE,
                len(usernames)
            )

            batch = usernames[position:batch_end]

            print(
                Fore.CYAN +
                f"\nBatch {position + 1}-{batch_end} / {len(usernames)}"
            )

            with ThreadPoolExecutor(
                max_workers=TiktokUsernameChecker.threads
            ) as executor:

                futures = {
                    executor.submit(checker, username): username
                    for username in batch
                }

                for future in as_completed(futures):

                    if TiktokUsernameChecker.stop_event.is_set():
                        break

                    username = futures[future]

                    try:
                        future.result()

                    except Exception as e:
                        print(
                            Fore.RED +
                            f"[Error] {username}: {e}"
                        )

            if TiktokUsernameChecker.stop_event.is_set():
                break

            position = batch_end
            save_progress(position)

            print(
                Fore.CYAN +
                f"Progress saved: {position}/{len(usernames)}"
            )

    except KeyboardInterrupt:

        TiktokUsernameChecker.stop_event.set()

        save_progress(position)

        print(
            Fore.YELLOW +
            f"\n[Stopped] Progress saved at {position}/{len(usernames)}"
        )

    finally:

        TiktokUsernameChecker.stop_event.set()

        print(
            Fore.CYAN +
            "\nChecker stopped."
        )

        print(
            f"Processed this run: "
            f"{TiktokUsernameChecker.available + TiktokUsernameChecker.unavailable}"
        )

        print(
            f"Available/Banned: "
            f"{TiktokUsernameChecker.available}"
        )

        print(
            f"Unavailable: "
            f"{TiktokUsernameChecker.unavailable}"
        )


def checker(username):

    if TiktokUsernameChecker.stop_event.is_set():
        return

    endpoint = TiktokUsernameChecker.endpoint + username

    try:

        scraper = get_scraper()

        response = scraper.get(
            endpoint,
            timeout=15,
            allow_redirects=True
        )

        status = response.status_code

        if status == 200:

            with TiktokUsernameChecker.lock:
                TiktokUsernameChecker.unavailable += 1

            if TiktokUsernameChecker.show_unavailable:
                print(
                    Fore.RED +
                    f"[Unavailable]      {endpoint}"
                )

        elif status in (404, 410):

            with TiktokUsernameChecker.lock:
                TiktokUsernameChecker.available += 1

            print(
                Fore.GREEN +
                f"[Available/Banned] {endpoint}"
            )

            save_available(username)

        elif status == 429:

            print(
                Fore.YELLOW +
                f"[Rate limited]     {endpoint}"
            )

            time.sleep(
                random.uniform(5, 10)
            )

        else:

            print(
                Fore.YELLOW +
                f"[HTTP {status}]       {endpoint}"
            )

    except KeyboardInterrupt:

        TiktokUsernameChecker.stop_event.set()

    except Exception as e:

        print(
            Fore.RED +
            f"[Error] {username}: {e}"
        )


def save_available(username):

    try:

        os.makedirs(
            os.path.dirname(AVAILABLE_FILE),
            exist_ok=True
        )

        with TiktokUsernameChecker.lock:

            with open(
                AVAILABLE_FILE,
                "a",
                encoding="utf-8"
            ) as f:

                f.write(username + "\n")

    except Exception as e:

        print(
            Fore.RED +
            f"[Save error] {username}: {e}"
        )
