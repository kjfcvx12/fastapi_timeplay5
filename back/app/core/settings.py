from pydantic_settings import BaseSettings
from pydantic import Field
from datetime import timedelta

#BaseSettings 환경변수 기반 설정 관리 클래스(DB, API키, 환경관련설정)
#alias로 환경변수값이 있는지 확인->해당 값으로 필드 채움
class Settings(BaseSettings):
    db_user:str=Field(..., alias="DB_USER")
    db_password:str=Field(..., alias="DB_PASSWORD")
    db_host:str=Field("localhost", alias="DB_HOST")
    db_port:str=Field("3306", alias="DB_PORT")
    db_name:str=Field(..., alias="DB_NAME")

    secret_key:str=Field(..., alias="SECRET_KEY")
    jwt_algorithm:str=Field(..., alias="JWT_ALGORITHM")
    access_token_expire_seconds:int = Field(900, alias="ACCESS_TOKEN_EXPIRE")
    refresh_token_expire_seconds:int = Field(604800, alias="REFRESH_TOKEN_EXPIRE")

    class Config:
        env_file=".env"
        case_sensitive=True
        extra="allow"
        populate_by_name=True

    #동적 프로퍼티
    #@property -> 메소드를 속성으로 접근가능
    #settings.db_url
    @property
    def tmp_db(self) -> str:
        return f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def db_url(self) -> str:
        return f"mysql+asyncmy://{self.tmp_db}"
    
    @property
    def sync_db_url(self) -> str:
        return f"mysql+pymysql://{self.tmp_db}"
    
    # 초단위->timedelta 객체로 변환
    @property
    def access_token_expire(self)->timedelta:
        return timedelta(seconds=self.access_token_expire_seconds)
    
    @property
    def refresh_token_expire(self)->timedelta:
        return timedelta(seconds=self.refresh_token_expire_seconds)


#전역 설정
settings=Settings()

