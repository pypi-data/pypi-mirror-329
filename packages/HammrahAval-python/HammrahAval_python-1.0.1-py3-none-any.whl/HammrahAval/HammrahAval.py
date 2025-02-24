from .config import *

from dataclasses import dataclass

import aiofiles, inspect, httpx, json, re, os

class DynamicResponse(dict):
    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)
    
    def __setitem__(self, key, value):
        return self.__dict__.__setitem__(key, value)
    
    def __delitem__(self, key):
        return self.__dict__.__delitem__(key)
    
    def get(self, key, default=None):
        return self.__dict__.get(key, default)

@dataclass
class GetMeDR(DynamicResponse):
    FirstName: str
    LastName: str
    Gender: str
    NationalCode: str
    ChristianBirthDate: str
    FatherName: str
    ThisSIMActivationDateChristian: str

@dataclass
class GetMyBalanceDR(DynamicResponse):
    Normal: int
    WOW: int
    Ladies: int
    Loyalty: int
    FirstGift: int
    Total: int

@dataclass
class GetMyPackagesDR(DynamicResponse):
    @dataclass
    class DataDR(DynamicResponse):
        Total: int
        Remaining: int
        ServiceName: str
        Type: str
        Unit: str
    Data: list[DataDR]
    PackageCode: str
    Title: str
    @dataclass
    class InfoDR(DynamicResponse):
        PackageCategory: str
        PackageType: str
        DurationType: str
        Duration: int
        DurationStr: str
        DurationTypeStr: str
        @dataclass
        class PackageContentsDR(DynamicResponse):
            PrimaryService: str
            UsageCategory: str
            Volume: int
            Unit: str
        PackageContents: list[PackageContentsDR]
        ActivationType: str
        Renewal: bool
        Reservable: bool
        Activable: bool
        Purchasable: bool
    Info: InfoDR
    Unlimited: bool
    Status: str
    Renewal: str
    Recursive: bool
    EffectiveTime: str
    ExpiryTime: str

@dataclass
class GetMyScoreDR(DynamicResponse): Score: int

@dataclass
class GetMySIMCardsDR(DynamicResponse):
    PhoneNumber: str
    ID: str
    Status: str

class Client:
    def __init__(self, PhoneNumber: str) -> None:
        try:
            if not isinstance(PhoneNumber, str): raise ValueError("PhoneNumber must be a string ( str type ) !")
            
            if re.search(r"^9\d{9}$", PhoneNumber): ...
            elif re.search(r"^09\d{9}$", PhoneNumber): PhoneNumber = PhoneNumber[1:]
            elif re.search(r"^989\d{9}$", PhoneNumber): PhoneNumber = PhoneNumber[2:]
            elif re.search(r"^\+989\d{9}$", PhoneNumber): PhoneNumber = PhoneNumber[3:]
            elif re.search(r"^00989\d{9}$", PhoneNumber): PhoneNumber = PhoneNumber[4:]
            else: raise ValueError("PhoneNumber is not valid !")
            
            self.path = os.getcwd().replace("\\", "/")
            self.PhoneNumber = PhoneNumber
        
        except Exception as e: print(f"Error in {Client.__name__}.{inspect.currentframe().f_code.co_name} : {e}")
    
    async def __aenter__(self):
        try:
            self.client = httpx.AsyncClient()
            if os.path.exists(f"{self.path}/{self.PhoneNumber}.json"): return self
            
            Curl = f"{HOST}/services/auth/v1.0/otp"
            Cheaders = {
                "Accept-Encoding": "gzip",
                "clientId": ClientID,
                "Connection": "Keep-Alive",
                "Content-Type": "application/json; charset=UTF-8",
                "Host": HOST_NAME,
                "User-Agent": "okhttp/3.12.12"
            }
            Cjson = {
                "appcode": AppCode,
                "msisdn": self.PhoneNumber
            }
            if (await self.client.post(Curl, json=Cjson, headers=Cheaders)).json()["status"]["code"] != 200: raise SystemError("Server response invalid !")
            
            NumberOfTry = 0
            while NumberOfTry < 3:
                try:
                    if re.search(r"\d{4}", code := input("Inter the 4 digit code : ")):
                        NumberOfTry += 1
                        Lurl = f"{HOST}/services/auth/v1.0/user/login/otp/{code}?mcisubs=true"
                        Lheaders = {
                            "Accept-Encoding": "gzip",
                            "clientId": ClientID,
                            "clientSecret": "mymci",
                            "Connection": "Keep-Alive",
                            "deviceId": DeviceID,
                            "Host": HOST_NAME,
                            "scope": "mymciGroup",
                            "User-Agent": "okhttp/3.12.12",
                            "username": self.PhoneNumber
                        }
                        Lreq = (await self.client.get(Lurl, headers=Lheaders)).json()["result"]["data"]
                        
                        if Lreq != None: break
                    raise ValueError
                except ValueError: print("Invalid code !")
                except KeyboardInterrupt: 
                    print("Bye !")
                    exit()
            else: raise SystemError("Invalid code ! The code was expired !")
        
            async with aiofiles.open(f"{self.path}/{self.PhoneNumber}.json", "w+") as file: await file.write(json.dumps({"ID": [i["id"] for i in Lreq["acl"] if i["msisdn"] == self.PhoneNumber][0], "Token": Lreq["token"], "RefreshToken": Lreq["refreshToken"]}, indent=4, ensure_ascii=False))
            return self
        
        except Exception as e: print(f"Error in {Client.__name__}.{inspect.currentframe().f_code.co_name} : {e}")
    
    async def __aexit__(self, *args):
        try: 
            self.Token, self.RefreshToken, self.ID
            async with aiofiles.open(f"{self.path}/{self.PhoneNumber}.json", "w+") as file: await file.write(json.dumps({"ID": self.ID, "Token": self.Token, "RefreshToken": self.RefreshToken}, indent=4, ensure_ascii=False))
            await self.client.aclose()
        except AttributeError: ...
        except Exception as e: print(f"Error in {Client.__name__}.{inspect.currentframe().f_code.co_name} : {e}")
    
    async def GetToken(self, aclcheck: bool = True) -> str | None:
        try:
            if os.path.exists(f"{self.path}/{self.PhoneNumber}.json"):
                try: self.Token, self.RefreshToken, self.ID
                except AttributeError: 
                    async with aiofiles.open(f"{self.path}/{self.PhoneNumber}.json", "r+") as file: Tjson = json.loads(await file.read())
                    self.Token, self.RefreshToken, self.ID = Tjson["Token"], Tjson["RefreshToken"], Tjson["ID"]
                
                Turl = f"{HOST}/services/auth/v1.0/token/refresh/{self.RefreshToken}"
                Theaders = {
                    "Accept-Encoding": "gzip",
                    "Authorization": f"Bearer {self.Token}",
                    "Connection": "Keep-Alive",
                    "Host": HOST_NAME,
                    "User-Agent": "okhttp/3.12.12"
                }
                if aclcheck: Theaders["aclcheck"] = "true"
                Treq = (await self.client.get(Turl, headers=Theaders)).json()["result"]["data"]
                
                self.Token, self.RefreshToken, self.ID = Treq["token"], Treq["refreshToken"], [i["id"] for i in Treq["acl"] if i["msisdn"] == self.PhoneNumber][0]
                
                if aclcheck: del Theaders["aclcheck"]
                Theaders["Authorization"] = f"Bearer {Treq['token']}"
                self.Headers = Theaders
                
                return Treq["token"]
            
            raise SystemError("Server response invalid !")
        except Exception as e: print(f"Error in {Client.__name__}.{inspect.currentframe().f_code.co_name} : {e}")
    
    async def GetMe(self) -> GetMeDR | None:
        try:
            Iurl = f"{HOST}/services/user/v1.0/profile"
            await self.GetToken()
            Ireq = (await self.client.get(Iurl, headers=self.Headers)).json()["result"]["data"]
            
            return GetMeDR(Ireq["firstname"], Ireq["lastname"], Ireq["attributes"]["gender"], Ireq["attributes"]["nationalCode"], Ireq["attributes"]["birthDate"], Ireq["attributes"]["fathername"], Ireq["createdts"])
            
        except Exception as e: print(f"Error in {Client.__name__}.{inspect.currentframe().f_code.co_name} : {e}")
    
    async def GetMySIMCards(self) -> list[GetMySIMCardsDR] | None:
        try:
            SIMurl = f"{HOST}/services/mci/subscriber/v1.0/usim/all"
            await self.GetToken()
            SIMreq = (await self.client.get(SIMurl, headers=self.Headers)).json()["result"]["data"]
            
            return [GetMySIMCardsDR(*i.values()) for i in SIMreq]
        
        except Exception as e: print(f"Error in {Client.__name__}.{inspect.currentframe().f_code.co_name} : {e}")
    
    async def GetMyBalance(self, PhoneNumber: str|None = None) -> GetMyBalanceDR | None:
        try:
            await self.GetToken()
            Burl = f"{HOST}/services/mci/subscriber/v1.0/{self.ID if not PhoneNumber or PhoneNumber == self.PhoneNumber else [i.ID for i in await self.GetMySIMCards() if i.PhoneNumber == PhoneNumber][0]}/balance/details"
            Breq = (await self.client.get(Burl, headers=self.Headers)).json()["result"]["data"]
            if Breq == {}: return None
            
            return GetMyBalanceDR(*Breq.values())
        
        except Exception as e: print(f"Error in {Client.__name__}.{inspect.currentframe().f_code.co_name} : {e}")
    
    async def GetMyPackages(self, PhoneNumber: str|None = None) -> list[GetMyPackagesDR] | None:
        try:
            await self.GetToken()
            Purl = f"{HOST}/services/mci/subscriber/v1.0/{self.ID if not PhoneNumber or PhoneNumber == self.PhoneNumber else [i.ID for i in await self.GetMySIMCards() if i.PhoneNumber == PhoneNumber][0]}/packages/active"
            Preq = (await self.client.get(Purl, headers=self.Headers)).json()["result"]["data"]
            
            return [GetMyPackagesDR([GetMyPackagesDR.DataDR(i["initial"], i["current"], i["serviceName"], i["type"], i["unit"]) for i in i["data"]], i["packageCode"], i["title"], GetMyPackagesDR.InfoDR(i["info"]["packageCategory"], i["info"]["packageType"], i["info"]["durationType"], i["info"]["duration"], i["info"]["durationStr"], i["info"]["durationTypeStr"], [GetMyPackagesDR.InfoDR.PackageContentsDR(*i.values()) for i in i["info"]["packageContents"]], i["info"]["activationType"], i["info"]["renewal"], i["info"]["reservable"], i["info"]["activable"], i["info"]["purchasable"]), i["unlimited"], i["status"], i["renewal"], i["recursive"], i["effectiveTime"], i["expiryTime"]) for i in Preq]

        except Exception as e: print(f"Error in {Client.__name__}.{inspect.currentframe().f_code.co_name} : {e}")
    
    async def GetMyScore(self, PhoneNumber: str|None = None) -> GetMyScoreDR | None:
        try:
            await self.GetToken()
            Surl = f"{HOST}/services/mci/subscriber/v1.0/{self.ID if not PhoneNumber or PhoneNumber == self.PhoneNumber else [i.ID for i in await self.GetMySIMCards() if i.PhoneNumber == PhoneNumber][0]}/loyaltyscore"
            Sreq = (await self.client.get(Surl, headers=self.Headers)).json()["result"]["data"]
            
            return GetMyScoreDR(*Sreq.values())
        
        except Exception as e: print(f"Error in {Client.__name__}.{inspect.currentframe().f_code.co_name} : {e}")