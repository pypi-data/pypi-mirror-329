from gevent import monkey
from pydantic import BaseModel

monkey.patch_all()

from fastapi import FastAPI, HTTPException, BackgroundTasks
from starlette.responses import JSONResponse
from playwright.async_api import async_playwright
from playwright_recaptcha import recaptchav3, recaptchav2


class CaptchaRequest(BaseModel):
    site_key: str
    target_url: str


class RecaptchaSolverClient:

    def __init__(self):
        # self.cf_solve = CFTurnstileSolver(site_key, target_url, headless=headless, proxy=proxy)
        self.app = FastAPI()
        self.add_routes()

    def add_routes(self):
        @self.app.get("/")
        def index():
            return {"message": "QGX"}

        @self.app.post("/solve_v3")
        async def solve(background_tasks: BackgroundTasks, captcha_req: CaptchaRequest):
            site_key = captcha_req.site_key
            target_url = captcha_req.target_url
            cf_token = await solve_captcha(site_key, target_url)
            return {"status": "success", "token": cf_token}

        @self.app.post("/solve_v2")
        async def solve(background_tasks: BackgroundTasks, captcha_req: CaptchaRequest):
            site_key = captcha_req.site_key
            target_url = captcha_req.target_url
            cf_token = await solve_captcha(site_key, target_url, "v2")
            return {"status": "success", "token": cf_token}

        @self.app.exception_handler(HTTPException)
        def http_exception_handler(request, exc):
            return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

    def start(self, port=5555):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=port)


async def solve_captcha(site_key: str, target_url: str, version: str = "v3"):
    print(f"[Recaptcha]开始破解: site_key={site_key}, target_url={target_url}")
    if version == "v3":
        async with async_playwright() as playwright:
            browser = await playwright.firefox.launch()
            page = await browser.new_page()
            async with recaptchav3.AsyncSolver(page) as solver:
                await page.goto(target_url)
                token = await solver.solve_recaptcha()
                print(token)
            return token
    else:
        async with async_playwright() as playwright:
            browser = await playwright.firefox.launch()
            page = await browser.new_page()
            async with recaptchav2.AsyncSolver(page) as solver:
                await page.goto(target_url)
                token = await solver.solve_recaptcha()
                print(token)
            return token


if __name__ == '__main__':
    client = RecaptchaSolverClient()
    client.start(port=6666)
