from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.config import PathsConfig, PageNamesConfig

from src.auth.config import RouterConfig, URLPathsConfig, URLNamesConfig
from src.core.utils import generate_html_context

router = APIRouter(
    prefix=RouterConfig.PREFIX,
    tags=RouterConfig.tags_list(),
)

# Mounts:
templates = Jinja2Templates(directory=PathsConfig.TEMPLATES.__str__())


@router.get(path=URLPathsConfig.REGISTER, response_class=HTMLResponse, name=URLNamesConfig.REGISTER)
async def register(request: Request):
    return templates.TemplateResponse(
        name=PathsConfig.REGISTER_PAGE.__str__(),
        request=request,
        context=generate_html_context(
            title=PageNamesConfig.REGISTER_PAGE
        )
    )


@router.get(path=URLPathsConfig.LOGIN, response_class=HTMLResponse, name=URLNamesConfig.LOGIN)
async def login(request: Request):
    return templates.TemplateResponse(
        name=PathsConfig.LOGIN_PAGE.__str__(),
        request=request,
        context=generate_html_context(
            title=PageNamesConfig.LOGIN_PAGE
        )
    )
