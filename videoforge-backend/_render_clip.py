import sys, time, shutil, os
from pathlib import Path
html_path = Path(sys.argv[1])
duration = float(sys.argv[2])
width = int(sys.argv[3])
height = int(sys.argv[4])
record_dir = Path(sys.argv[5])
try:
    from playwright.sync_api import sync_playwright
    record_duration = duration + 0.6
    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=["--disable-web-security", "--no-sandbox", "--disable-dev-shm-usage",
                  "--autoplay-policy=no-user-gesture-required"],
        )
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
            record_video_dir=str(record_dir),
            record_video_size={"width": width, "height": height},
        )
        page = context.new_page()
        page.goto(f"file:///{html_path.resolve().as_posix()}", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(350)
        start_time = time.time()
        while time.time() - start_time < record_duration:
            page.wait_for_timeout(50)
        video = page.video
        page.close()
        final_path = record_dir / "output.webm"
        video.save_as(str(final_path))
        context.close()
        browser.close()
    print("OK")
except Exception as e:
    import traceback
    traceback.print_exc(file=sys.stderr)
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
