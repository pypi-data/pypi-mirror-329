import requests
from playwright.sync_api import sync_playwright
from playwright_recaptcha import recaptchav2


RECAPTCHA_HTML = """
<!DOCTYPE html>
<html>
    <head>
        <script src="https://www.google.com/recaptcha/api.js" async
            defer></script>
    </head>
    <body>
        <div
            class="g-recaptcha"
            data-sitekey="{sitekey}"></div>
    </body>
</html>
"""


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        page = browser.new_page()

        page.goto("https://forms.plumenetwork.xyz/passport", wait_until="commit")

        page.set_content(
            RECAPTCHA_HTML.format(sitekey="6LcU2HEeAAAAAMNAtJ-YLXooPnuQcIrVgtE8LuK8")
        )

        with recaptchav2.SyncSolver(page) as solver:
            token = solver.solve_recaptcha(wait=True)
            print(token)


if __name__ == "__main__":
    main()