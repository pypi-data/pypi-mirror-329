from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    base_url: str = "https://svgl.app/api/"
    svgs_url: str =  base_url + "svgs/"
    categories_url: str = base_url + "categories/"
    type_logo: str = ""
    color: str = ""
    extention: str = "svg"
    output: str = ""